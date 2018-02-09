import inro.emme.desktop.app as _app
import inro.modeller as _m

emme_desktop = _app.start_dedicated(
    project="C:\Helmet\HELMET_KEHI_31\sijoittelu\sijoittelu.emp", 
    visible=False, 
    user_initials="HSL"
)
emme_modeller = _m.Modeller(emme_desktop)
emme_bank = emme_modeller.emmebank
netcalc = emme_modeller.tool(
    "inro.emme.network_calculation.network_calculator"
)
create_matrix = emme_modeller.tool(
    "inro.emme.data.matrix.create_matrix"
)
transit_assignment = emme_modeller.tool(
    "inro.emme.transit_assignment.extended_transit_assignment"
)
mat_results = emme_modeller.tool(
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
transit_assignment_modes = transit_modes + aux_modes
transitions = []
for mode in transit_modes:
    transitions.append({
        "mode": mode,
        "next_journey_level": 1
    })
	
def trass_run (scen_id, demand_mat_id, result_mat_id):
    netw_specs = []
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=b"
        },
        "expression": "10",
        "result": "ut3",
        "aggregation": None,
    })
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=g"
        },
        "expression": "8",
        "result": "ut3",
        "aggregation": None,
    })
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=de"
        },
        "expression": "10",
        "result": "ut3",
        "aggregation": None,
    })
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=rj"
        },
        "expression": "5",
        "result": "ut3",
        "aggregation": None,
    })
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "transit_line": "mode=mtpw"
        },
        "expression": "0",
        "result": "ut3",
        "aggregation": None,
    })
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "link": "all",
			"transit_line": "mode=bgde"
        },
        "expression": "0.1*index2",
        "result": "us3",
        "aggregation": None,
    })
    netcalc(netw_specs, emme_bank.scenario(scen_id))
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
                        "perception_factor": 1
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
                    "on_segments": None
                },
                "boarding_cost": {
                    "global": {
                        "penalty": 3,
                        "perception_factor": 1,
                    },
                    "at_nodes": None,
                    "on_lines": None,
                    "on_segments": {
                        "penalty": "us3",
                        "perception_factor": 1
                    },                    
                },
                "waiting_time": None
            }
        ],
        "performance_settings": {
            "number_of_processors": "max"
        },
    }
    transit_assignment(trass_spec, emme_bank.scenario(scen_id))

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
    mat_results(result_spec, emme_bank.scenario(scen_id))
    print "Transit assignment performed for scenario " + str(scen_id)

trass_run(21, "mf4", "2")
trass_run(22, "mf6", "3")
trass_run(23, "mf5", "4")