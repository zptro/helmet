transit_modes = [
    'b',
    'd',
    'e',
    'g',
    'j',
    'm',
    'p',
    'r',
    't',
    'w',
]
aux_modes = [
    'a',
    's',
]
    
def transit_ass (emme_modeller, scen_id, demand_mat_id, result_mat_id):
    """Perform transit assignment for one scenario."""
    emmebank = emme_modeller.emmebank
    scenario = emmebank.scenario(scen_id)
    network = scenario.get_network()
    
    # Calculation of cumulative line segment travel time
    for line in network.transit_lines():
        # cumulative_length = 0
        cumulative_time = 0
        for segment in line.segments():
            # cumulative_length += segment.link.length
            # Travel time for buses in mixed traffic
            if segment.transit_time_func == 1:
                cumulative_time += ( segment.data2 * segment.link.length
                                   # + segment.link["@timau"]
                                   + segment.link.auto_time
                                   + segment.dwell_time
                )
            # Travel time for buses on bus lanes
            if segment.transit_time_func == 2:
                cumulative_time += ( segment.data2 * segment.link.length
                                   + segment.dwell_time
                )
            # Travel time for trams AHT
            if segment.transit_time_func == 3:
                speedstr = str(segment.link.data1)
                if len(speedstr) < 8:
                    speed = int(speedstr[0])
                else:
                    speed = int(speedstr[0:2])
                cumulative_time += ( segment.link.length
                                   / speed
                                   * 60
                                   + segment.dwell_time
                )
            # Travel time for trams PT
            if segment.transit_time_func == 4:
                speedstr = str(segment.link.data1)
                if len(speedstr) < 8:
                    speed = int(speedstr[1:3])
                else:
                    speed = int(speedstr[2:4])
                cumulative_time += ( segment.link.length
                                   / speed
                                   * 60
                                   + segment.dwell_time
                )
            # Travel time for trams IHT
            if segment.transit_time_func == 5:
                speedstr = str(segment.link.data1)
                if len(speedstr) < 8:
                    speed = int(speedstr[3:5])
                else:
                    speed = int(speedstr[4:6])
                cumulative_time += ( segment.link.length
                                   / speed
                                   * 60
                                   + segment.dwell_time
                )
            # The estimated waiting time deviation caused by travel time
            # segment.data3 = 0.044 * cumulative_time
            segment["@wait_time_dev"] = 0.044 * cumulative_time
    scenario.publish_network(network)
    # values = network.get_attribute_values("TRANSIT_SEGMENT", "data3")
    # scenario.set_attribute_values("TRANSIT_SEGMENT", "data3", values)
    print "Cumulative travel times calculated for scenario "  + str(scen_id)
    # Definition of line specific boarding penalties
    netw_specs = []
    # Bus
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=b",
        },
        "expression": "8",
        "result": "ut3",
        "aggregation": None,
    })
    # Trunk bus
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=g",
        },
        "expression": "6",
        "result": "ut3",
        "aggregation": None,
    })
    # Long-distance and express buses
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=de",
        },
        "expression": "10",
        "result": "ut3",
        "aggregation": None,
    })
    # Train
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=rj",
        },
        "expression": "5",
        "result": "ut3",
        "aggregation": None,
    })
    # Metro and ferry
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=mw",
        },
        "expression": "0",
        "result": "ut3",
        "aggregation": None,
    })
    # Tram and light rail
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=tp",
        },
        "expression": "0",
        "result": "ut3",
        "aggregation": None,
    })
    # netw_specs.append({
        # "type": "NETWORK_CALCULATION",
        # "selections": {
            # "link": "all",
            # "transit_line": "mode=bgde",
        # },
        # "expression": "0.1*index2",
        # "result": "us3",
        # "aggregation": None,
    # })
    netcalc = emme_modeller.tool(
        "inro.emme.network_calculation.network_calculator")
    netcalc(netw_specs, scenario)
    
    # Definition of transition rules: all modes are allowed
    transitions = []
    for mode in transit_modes:
        transitions.append({
            "mode": mode,
            "next_journey_level": 1
        })
    transit_assignment_modes = transit_modes + aux_modes
    
    # Specification of the transit assignment
    trass_spec = {
        "type": "EXTENDED_TRANSIT_ASSIGNMENT",
        "modes": transit_assignment_modes,
        "demand": demand_mat_id,
        "waiting_time": {
            "headway_fraction": 0.5,
            "effective_headways": "hdw",
            "spread_factor": 1,
            "perception_factor": 2.5
        },
        # Boarding time is defined for each journey level separately,
        # so here we just set the default to zero.
        "boarding_time": {
            "global": {
                "penalty": 0,
                "perception_factor": 1,
            },
            "at_nodes": None,
            "on_lines": None,
            "on_segments": None,
        },
        "boarding_cost": {
            "global": {
                "penalty": 0,
                "perception_factor": 1,
            },
            "at_nodes": None,
            "on_lines": None,
            "on_segments": None,
        },
        "in_vehicle_time": {
            "perception_factor": 1
        },
        "in_vehicle_cost": None,
        "aux_transit_time": {
            "perception_factor": 1.7
        },
        "aux_transit_cost": None,
        "flow_distribution_at_origins": {
            "choices_at_origins": "OPTIMAL_STRATEGY",
            "fixed_proportions_on_connectors": None
        },
        "flow_distribution_at_regular_nodes_with_aux_transit_choices": {
            "choices_at_regular_nodes": "OPTIMAL_STRATEGY"
        },
        "flow_distribution_between_lines": {
            "consider_total_impedance": False
        },
        "connector_to_connector_path_prohibition": None,
        "od_results": {
            "total_impedance": None
        },
        # The two journey levels are identical, except that at the second
        # level an extra boarding penalty is implemented,
        # hence a transfer penalty. Walk only trips are not allowed.
        "journey_levels": [
            {
                "description": "Not boarded yet",
                "destinations_reachable": False,
                "transition_rules": transitions,
                "boarding_time": {
                    "global": None,
                    "at_nodes": None,
                    "on_lines": {
                        "penalty": "ut3",
                        "perception_factor": 1
                    },
                    "on_segments": {
                        "penalty": "@wait_time_dev",
                        "perception_factor": 2.5
                    },
                },
                "boarding_cost": None,
                "waiting_time": None
            },
            {
                "description": "Boarded at least once",
                "destinations_reachable": True,
                "transition_rules": transitions,
                "boarding_time": {
                    "global": None,
                    "at_nodes": None,
                    "on_lines": {
                        "penalty": "ut3",
                        "perception_factor": 1
                    },
                    "on_segments": {
                        "penalty": "@wait_time_dev",
                        "perception_factor": 2.5
                    }
                },
                "boarding_cost": {
                    "global": {
                        "penalty": 5,
                        "perception_factor": 1,
                    },
                    "at_nodes": None,
                    "on_lines": None,
                    "on_segments": None,                    
                },
                "waiting_time": None
            }
        ],
        "performance_settings": {
            "number_of_processors": "max"
        },
    }
    func = {
        "type": "BPR",
        "weight": 0.53,
        "exponent": 2,
        "assignment_period": 1,
        "orig_func": False,
        "congestion_attribute": "us3",
    }
    # func = {
        # "type": "CUSTOM",
        # "assignment_period": 1,
        # "orig_func": False,
        # "congestion_attribute": "us3",
        # "python_function": """def calc_segment_cost(transit_volume, capacity, segment):
                                # return 0.53 * ((transit_volume / capacity) ** 2)"""
    # }
    stop = {
        "max_iterations": 10,
        "normalized_gap": 0.01,
        "relative_gap": 0.001
    }
    print "Transit assignment started..."
    transit_assignment = emme_modeller.tool(
        "inro.emme.transit_assignment.extended_transit_assignment")
    congested_assignment = emme_modeller.tool(
        "inro.emme.transit_assignment.congested_transit_assignment")
    # transit_assignment(trass_spec, scenario)
    congested_assignment(transit_assignment_spec=trass_spec, 
                         congestion_function=func,
                         stopping_criteria=stop, 
                         log_worksheets=False, 
                         scenario=scenario)
    
    tottim_id = "mf" + result_mat_id + "0"
    inveht_id = "mf" + result_mat_id + "1"
    auxtim_id = "mf" + result_mat_id + "2"
    twtime_id = "mf" + result_mat_id + "3"
    fwtime_id = "mf" + result_mat_id + "4"
    boatim_id = "mf" + result_mat_id + "5"
    noboa_id = "mf" + result_mat_id + "6"
    invlen_id = "mf" + result_mat_id + "7"
    create_matrix = emme_modeller.tool(
        "inro.emme.data.matrix.create_matrix")
    create_matrix(matrix_id=tottim_id,
                  matrix_name="tottim",
                  matrix_description="total time s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    create_matrix(matrix_id=inveht_id,
                  matrix_name="inveht",
                  matrix_description="in veh time s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    create_matrix(matrix_id=auxtim_id,
                  matrix_name="auxtim",
                  matrix_description="aux time s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    create_matrix(matrix_id=twtime_id,
                  matrix_name="twtime",
                  matrix_description="tot wait time s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    create_matrix(matrix_id=fwtime_id,
                  matrix_name="fwtime",
                  matrix_description="first wait time s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    create_matrix(matrix_id=boatim_id,
                  matrix_name="boatim",
                  matrix_description="board time s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    create_matrix(matrix_id=noboa_id,
                  matrix_name="noboa",
                  matrix_description="no of board s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    create_matrix(matrix_id=invlen_id,
                  matrix_name="invlen",
                  matrix_description="in veh lenght s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    result_spec = {
        "type": "EXTENDED_TRANSIT_MATRIX_RESULTS",
        "total_impedance": tottim_id,
        "actual_first_waiting_times": fwtime_id,
        "actual_total_waiting_times": twtime_id,
        "by_mode_subset": {
            "modes": transit_modes,
            "distance": invlen_id,
            "avg_boardings": noboa_id,
            "actual_total_boarding_times": boatim_id,
            "actual_in_vehicle_times": inveht_id,
            "actual_aux_transit_times": auxtim_id,
        },
    }
    matrix_results = emme_modeller.tool(
        "inro.emme.transit_assignment.extended.matrix_results")
    matrix_results(result_spec, scenario)
    print "Transit assignment performed for scenario " + str(scen_id)