import parameters

def traffic_ass (emme_modeller, scen_id, stopping_criteria, demand_mat_id, 
              time_mat_id, length_mat_id, cost_mat_id):
    """Perform car traffic assignment for one scenario."""
    emmebank = emme_modeller.emmebank
    scenario = emmebank.scenario(scen_id)
    create_matrix = emme_modeller.tool(
        "inro.emme.data.matrix.create_matrix")
    create_matrix(matrix_id=time_mat_id,
                  matrix_name="hatim",
                  matrix_description="ha-aikamatr s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    create_matrix(matrix_id=length_mat_id,
                  matrix_name="halen",
                  matrix_description="ha-pituusmatr s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
    create_matrix(matrix_id=cost_mat_id,
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
                "demand": demand_mat_id,
                "generalized_cost": {
                    "link_costs": "@rumsi",
                    "perception_factor": parameters.length_weight,
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
        "expression": time_mat_id
                      +"-"+str(parameters.length_weight)+"*"+length_mat_id
                      +"-"+"6"+"*"+cost_mat_id,
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
        "inro.emme.matrix_calculation.matrix_calculator")
    matcalc(matrix_spec, scenario)
    print "Time matrix extracted from generalized cost"