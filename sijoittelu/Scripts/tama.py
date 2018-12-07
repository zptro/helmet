import omx
import numpy
import CalcDistribution

population = numpy.loadtxt('C:\Helmet\HELMET_KEHI_31\sijoittelu\Data\\population.txt')
workplaces = numpy.loadtxt('C:\Helmet\HELMET_KEHI_31\sijoittelu\Data\\workplaces.txt')
logistics = numpy.loadtxt('C:\Helmet\HELMET_KEHI_31\sijoittelu\Data\\logistics.txt')
shops = numpy.loadtxt('C:\Helmet\HELMET_KEHI_31\sijoittelu\Data\\shops.txt')
external_growth = numpy.loadtxt('C:\Helmet\HELMET_KEHI_31\sijoittelu\Data\\external.txt')

trucks = ( 0.0044 * population 
         + 0.0222 * workplaces 
         + 0.1385 * logistics 
         + 0.134 * shops
         + 0.001)
trailer_trucks = ( 0.0213 * workplaces
                 + 0.1944 * logistics
                 + 0.095 * shops
                 + 0.001)
vans = trucks
garbage = 0.000125 * (population + 0.2 * workplaces)
demand_share = {}
demand_share['a'] = 0.0659
demand_share['p'] = 0.0702
demand_share['i'] = 0.0662
prod = {}
garb = {}
for time_period in demand_share:
    prod["KA" + time_period] = demand_share[time_period] * trucks
    prod["YHD" + time_period] = demand_share[time_period] * trailer_trucks
    prod["PA" + time_period] = demand_share[time_period] * vans
    garb["KA" + time_period] = demand_share[time_period] * garbage

base_demand_file = omx.openFile('C:\Helmet\HELMET_KEHI_31\sijoittelu\Data\\tama_pohjamatriisit.omx')
garbage_destination = base_demand_file.mapping("zone_number")[2792]
for id in base_demand_file.listMatrices():
    demand_mtx = numpy.array(base_demand_file[id])
    demand_mtx.clip(0.000001, None) # Remove zero values
    row_sum = demand_mtx.sum(1)
    # External demand is generated for the 44 last centroids
    external_base = row_sum[-44:]
    external_demand = external_growth * external_base
    production = numpy.append(prod[id], external_demand)
    # Balance the demand matrix according to production vector
    CalcDistribution.calcFratar(production, production, demand_mtx)
    if (id[:2] == "KA"):
        # Add garbage transports to/from zone 2792 
        demand_mtx[:-44,garbage_destination] += garb[id]
        demand_mtx[garbage_destination,:-44] += garb[id]
base_demand_file.close()




# x_sum = numpy.sum(base_demand["KAa"], 0)
# y_sum = numpy.sum(base_demand["KAa"], 1)
# forecasted_demand_x = base_demand["KAa"] * trucks / x_sum
# forecasted_demand_y = (base_demand["KAa"].T * trucks / y_sum).T
# forecasted_demand["KAa"] = 0.5 * (forecasted_demand_x + forecasted_demand_y)