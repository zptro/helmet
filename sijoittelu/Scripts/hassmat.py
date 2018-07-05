def hass_run (emme_modeller, scen_id, demand_mat_id, time_mat_id, length_mat_id, cost_mat_id):
    """Perform car assignment for one scenario."""
    emmebank = emme_modeller.emmebank
    scenario = emmebank.scenario(scen_id)
    # create_matrix(matrix_id=time_mat_id,
                  # matrix_name="hatim",
                  # matrix_description="ha-aikamatr s="+str(scen_id),
                  # default_value=0)
    # create_matrix(matrix_id=length_mat_id,
                  # matrix_name="halen",
                  # matrix_description="ha-pituusmatr s="+str(scen_id),
                  # default_value=0)
    # create_matrix(matrix_id=cost_mat_id,
                  # matrix_name="ruma",
                  # matrix_description="ruuhkamaksumatr s="+str(scen_id),
                  # default_value=0)
    spec = {
        "type": "SOLA_TRAFFIC_ASSIGNMENT",
        "classes": [
            {
                "mode": "c",
                "demand": demand_mat_id,
                "generalized_cost": {
                    "link_costs": "@rumsi",
                    "perception_factor": 0.2
                },
                "results": {
                    "link_volumes": None,
                    "turn_volumes": None,
                    "od_travel_times": {
                        "shortest_paths": time_mat_id
                    }
                },
                "path_analyses": [
                    {
                        "link_component": "length",
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
                        "analyzed_demand": None,
                        "results": {
                            "selected_link_volumes": None,
                            "selected_turn_volumes": None,
                            "od_values": length_mat_id,
                        },
                    },
                    {
                        "link_component": "@ruma",
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
                                "path_value": True
                            }
                        },
                        "analyzed_demand": None,
                        "results": {
                            "selected_link_volumes": None,
                            "selected_turn_volumes": None,
                            "od_values": cost_mat_id,
                        },
                    },
                ]
            }
        ],
        "performance_settings": {
            "number_of_processors": "max"
        },
        "background_traffic": None,
        "stopping_criteria": {
            "max_iterations": 100,
            "relative_gap": 0.0001,
            "best_relative_gap": 0.01,
            "normalized_gap": 0.005
        }
    }
    print "Traffic assignment started..."
    car_assignment = emme_modeller.tool(
        "inro.emme.traffic_assignment.sola_traffic_assignment"
    )
    car_assignment(spec, scenario)
    print "Traffic assignment performed for scenario " + str(scen_id)
    matrix_spec = {
        "type": "MATRIX_CALCULATION",
        "expression": time_mat_id+"-0.2*"+length_mat_id+"-6*"+cost_mat_id,
        "result": time_mat_id,
        "constraint": {
            "by_value": None,
            "by_zone": None,
        },
        "aggregation": {
            "origins": None,
            "destinations": None,
        },
    }
    matcalc = emme_modeller.tool(
        "inro.emme.matrix_calculation.matrix_calculator"
    )
    matcalc(matrix_spec, scenario)
	print "Generalized cost transformed to time"