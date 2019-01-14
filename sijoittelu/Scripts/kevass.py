

def bike_ass (emme_modeller, scen_id, demand_mat_id, time_mat_id, length_mat_id, length_for_links, link_vol):
    """Perform bike traffic assignment for one scenario."""
    emmebank = emme_modeller.emmebank
    scen = emmebank.scenario(scen_id)
    create_matrix = emme_modeller.tool(
        "inro.emme.data.matrix.create_matrix")
    create_matrix(matrix_id=time_mat_id,
                  matrix_name="pptim",
                  matrix_description="pyoraily aika s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    create_matrix(matrix_id=length_mat_id,
                  matrix_name="pppit",
                  matrix_description="pyoraily etaisyys s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    netcalc = emme_modeller.tool(
        "inro.emme.network_calculation.network_calculator")
    # Reset ul3 to zero
    netw_spec = {
        "type": "NETWORK_CALCULATION",
        "selections": {
            "link": "all",
        },
        "expression": "0",
        "result": "ul3",
        "aggregation": None,
    }
    netcalc(netw_spec, scen)
    # Define for which links to calculate length and save in ul3
    netw_spec = {
        "type": "NETWORK_CALCULATION",
        "selections": {
            "link": length_for_links,
        },
        "expression": "length",
        "result": "ul3",
        "aggregation": None,
    }
    netcalc(netw_spec, scen)
    spec = {
        "type": "STANDARD_TRAFFIC_ASSIGNMENT",
        "classes": [ 
            {
                "mode": "f",
                "demand": demand_mat_id,
                "generalized_cost": None,
                "results": {
                     "od_travel_times": {
                         "shortest_paths": time_mat_id,
                     },
                     "link_volumes": link_vol,
                     "turn_volumes": None,
                },
                "analysis": {
                    "analyzed_demand": None,
                    "results": {
                        "od_values": length_mat_id,
                        "selected_link_volumes": None,
                        "selected_turn_volumes": None,
                    },
                },
            }
        ],
        "path_analysis": {
            "link_component": "ul3",
            "turn_component": None,
            "operator": "+",
            "selection_threshold": {
                "lower": None,
                "upper": None,
            },
            "path_to_od_composition": {
                "considered_paths": "ALL",
                "multiply_path_proportions_by": {
                    "analyzed_demand": False,
                    "path_value": True,
                }
            },
        },
        "background_traffic": None,
        "stopping_criteria": {
            "max_iterations": 1,
            "best_relative_gap": 1,
            "relative_gap": 1,
            "normalized_gap": 1,
        },
        "performance_settings": {
            "number_of_processors": "max"
        }
    }  
    dist = {
        "type": "UNIFORM", 
        "A": 0.5, 
        "B": 1.5,
    }
    print "Bike assignment started..."
    bike_assignment = emme_modeller.tool(
        "inro.emme.traffic_assignment.standard_traffic_assignment")
    bike_assignment(specification=spec,  
                    scenario=scen)
    stoch_bike_assignment = emme_modeller.tool(
        "inro.emme.traffic_assignment.stochastic_traffic_assignment")
    # stoch_bike_assignment(traffic_assignment_spec=spec, 
                    # dist_par=dist, 
                    # replications=10, 
                    # scenario=scen)
    print "Bike assignment performed for scenario " + str(scen_id)
