import parameters

def calc_road_cost (emme_modeller, scen_id):
    """Calculate road charges and driving costs for one scenario."""
    emmebank = emme_modeller.emmebank
    scenario = emmebank.scenario(scen_id)
	
    netw_specs = []
    # Link cost [eur]
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "link": "all",
        },
        "expression": "@hinta*length",
        "result": "@ruma",
        "aggregation": None,
    })
    # Driving cost [eur]
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "link": "all",
        },
        "expression": str(parameters.dist_cost)+"*length",
        "result": "@rumpi",
        "aggregation": None,
    })
    # Total cost [eur]
    netw_specs.append({
        "type": "NETWORK_CALCULATION",
        "selections": {
            "link": "all",
        },
        "expression": "@ruma+@rumpi",
        "result": "@rumsi",
        "aggregation": None,
    })
    netcalc = emme_modeller.tool(
        "inro.emme.network_calculation.network_calculator")
    netcalc(netw_specs, scenario)

    print "Road charges calculated for scenario " + str(scen_id)