def hass_run (emme_modeller, scen_id, demand_mat_id):
    """Perform car assignment for one scenario."""
    emmebank = emme_modeller.emmebank
    scenario = emmebank.scenario(scen_id)
    spec = {
        "type": "SOLA_TRAFFIC_ASSIGNMENT",
        "classes": [
            {
                "mode": "c",
                "demand": "mf1",
                "generalized_cost": {
                    "link_costs": "@rumsi",
                    "perception_factor": 0.2
                },
                "results": {
                    "link_volumes": None,
                    "turn_volumes": None,
                    "od_travel_times": {
                        "shortest_paths": "mf380"
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
                            "od_values": "mf381",
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
                            "od_values": "mf370",
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
    car_assignment = emme_modeller.tool(
        "inro.emme.traffic_assignment.sola_traffic_assignment"
    )
    car_assignment(spec)