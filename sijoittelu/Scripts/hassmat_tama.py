import parameters as param

def traffic_ass (emme_modeller, scen_id, stopping_criteria, mtx_id):
    """Perform car traffic assignment for one scenario."""
    emmebank = emme_modeller.emmebank
    scenario = emmebank.scenario(scen_id)
    create_matrix = emme_modeller.tool(
        "inro.emme.data.matrix.create_matrix")
    create_matrix(matrix_id=mtx_id["car_time"],
                  matrix_name="hatim",
                  matrix_description="ha-aikamatr s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    create_matrix(matrix_id=mtx_id["car_dist"],
                  matrix_name="halen",
                  matrix_description="ha-pituusmatr s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    create_matrix(matrix_id=mtx_id["car_cost"],
                  matrix_name="ruma",
                  matrix_description="ruuhkamaksumatr s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    print "Matrices created."
    spec = {
        "type": "SOLA_TRAFFIC_ASSIGNMENT",
        "classes": [
            {
                "mode": "c",
                "demand": mtx_id["car_demand"],
                "generalized_cost": {
                    "link_costs": "@rumsi",
                    "perception_factor": param.vot_inv,
                },
                "results": {
                    "link_volumes": None,
                    "turn_volumes": None,
                    "od_travel_times": {
                        "shortest_paths": mtx_id["car_time"]
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
                            "od_values": mtx_id["car_dist"],
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
                            "od_values": mtx_id["car_cost"],
                        },
                    },
                ]
            },
            {
                "mode": "y",
                "demand": mtx_id["trailer_truck_demand"],
                "generalized_cost": {
                    "link_costs": "length",
                    "perception_factor": 0.2,
                },
                "results": {
                    "link_volumes": "@yhd",
                    "turn_volumes": None,
                    "od_travel_times": {
                        "shortest_paths": None
                    }
                },
                "path_analyses": []
            },
            {
                "mode": "k",
                "demand": mtx_id["truck_demand"],
                "generalized_cost": {
                    "link_costs": "length",
                    "perception_factor": 0.2,
                },
                "results": {
                    "link_volumes": "@ka",
                    "turn_volumes": None,
                    "od_travel_times": {
                        "shortest_paths": None
                    }
                },
                "path_analyses": []
            },
            {
                "mode": "v",
                "demand": mtx_id["van_demand"],
                "generalized_cost": {
                    "link_costs": "length",
                    "perception_factor": 0.2,
                },
                "results": {
                    "link_volumes": "@pa",
                    "turn_volumes": None,
                    "od_travel_times": {
                        "shortest_paths": None
                    }
                },
                "path_analyses": []
            },
        ],
        "background_traffic": None,
        "performance_settings": {
            "number_of_processors": "max"
        },
        "stopping_criteria": stopping_criteria,
    }
    print "Traffic assignment started..."
    car_assignment = emme_modeller.tool(
        "inro.emme.traffic_assignment.sola_traffic_assignment")
    car_assignment(spec, scenario)
    print "Traffic assignment performed for scenario " + str(scen_id)
    
    # Traffic assignment produces a generalized cost matrix.
    # To get travel time, monetary cost is removed from generalized cost.
    matrix_spec = {
        "type": "MATRIX_CALCULATION",
        "expression": mtx_id["car_time"]
                      +"-"+str(param.vot_inv)+"*("+mtx_id["car_cost"]
                      +"+"+str(param.dist_cost)+"*"+mtx_id["car_dist"]+")",
        "result": mtx_id["car_time"],
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
        "inro.emme.matrix_calculation.matrix_calculator")
    matcalc(matrix_spec, scenario)
    print "Time matrix extracted from generalized cost"