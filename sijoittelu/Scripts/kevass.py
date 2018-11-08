

def bike_ass (emme_modeller, scen_id, demand_mat_id, result_mat_id):
    """Perform bike traffic assignment for one scenario."""
    emmebank = emme_modeller.emmebank
    scen = emmebank.scenario(scen_id)
    create_matrix = emme_modeller.tool(
        "inro.emme.data.matrix.create_matrix")
    create_matrix(matrix_id=result_mat_id,
                  matrix_name="pptim",
                  matrix_description="pyoraily aika s="+str(scen_id),
                  default_value=0,
                  overwrite=True)
	spec = {
		"type": "STANDARD_TRAFFIC_ASSIGNMENT",
		"classes": [ 
			{
				"mode": "f",
				"demand": demand_mat_id,
				"generalized_cost": None,
				"results": {
					 "od_travel_times": {
						 "shortest_paths": result_mat_id,
					 },
					 "link_volumes": None,
					 "turn_volumes": None,
				},
				"analysis": None,
			}
		],
		"background_traffic": None,
		"path_analysis": None,
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
		"A": 0.9, 
		"B": 1.1,
	}
    print "Bike assignment started..."
    bike_assignment = emme_modeller.tool(
        "inro.emme.traffic_assignment.stochastic_traffic_assignment")
    bike_assignment(traffic_assignment_spec=spec, 
	                dist_par=dist, 
					replications=10, 
					scenario=scen)
    print "Bike assignment performed for scenario " + str(scen_id)
