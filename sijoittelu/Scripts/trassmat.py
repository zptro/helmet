import inro.emme.desktop.app as _app
import inro.modeller as _m

emme_desktop = _app.start_dedicated(
    project="C:\Helmet\HELMET_KEHI_31\sijoittelu\sijoittelu.emp", 
    visible=False, 
    user_initials="HSL"
)
emme_modeller = _m.Modeller(emme_desktop)
emmebank = emme_modeller.emmebank
netcalc = emme_modeller.tool(
    "inro.emme.network_calculation.network_calculator"
)
create_matrix = emme_modeller.tool(
    "inro.emme.data.matrix.create_matrix"
)
transit_assignment = emme_modeller.tool(
    "inro.emme.transit_assignment.extended_transit_assignment"
)
matrix_results = emme_modeller.tool(
    "inro.emme.transit_assignment.extended.matrix_results"
)
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

# Function for performing transit assignment for one scenario    
def trass_run (scen_id, demand_mat_id, result_mat_id):
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
                                   + segment.link["@timau"]
                                   # + segment.link.auto_time
                                   + segment.dwell_time
				)
            # Travel time for buses on buses lanes
            if segment.transit_time_func == 2:
                cumulative_time += ( segment.data2 * segment.link.length
                                   + segment.dwell_time
				)
            # The estimated waiting time deviation caused by bus travel time
            segment.data3 = 0.044 * cumulative_time
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
        "expression": "2",
        "result": "ut3",
        "aggregation": None,
    })
    # Trunk bus
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=g",
        },
        "expression": "1",
        "result": "ut3",
        "aggregation": None,
    })
    # Long-distance and express buses
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=de",
        },
        "expression": "2",
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
    # Metro and light rail
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=mtpw",
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
            "perception_factor": 1.5
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
            "perception_factor": 1.5
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
                        "penalty": "us3",
                        "perception_factor": 1.5
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
                        "penalty": "us3",
                        "perception_factor": 1.5
                    }
                },
                "boarding_cost": {
                    "global": {
                        "penalty": 3,
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
    print "Transit assignment started..."
    transit_assignment(trass_spec, scenario)
    tottim_id = "mf" + result_mat_id + "0"
    noboa_id = "mf" + result_mat_id + "6"
    # create_matrix(matrix_id=tottim_id,
                  # matrix_name="tottim",
                  # matrix_description="total time s= ah,tayd",
                  # default_value=0)
    # create_matrix(matrix_id=noboa_id,
                  # matrix_name="noboa",
                  # matrix_description="no of board s= ah,tayd",
                  # default_value=0)
    result_spec = {
        "type": "EXTENDED_TRANSIT_MATRIX_RESULTS",
        "total_impedance": tottim_id,
        "by_mode_subset": {
            "modes": transit_modes,
            "avg_boardings": noboa_id,
        },
    }
    matrix_results(result_spec, scenario)
    print "Transit assignment performed for scenario " + str(scen_id)

trass_run(21, "mf4", "2")
trass_run(22, "mf6", "3")
trass_run(23, "mf5", "4")