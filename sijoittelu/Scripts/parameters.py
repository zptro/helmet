# Inversed value of time [min/eur]
vot_inv = 6
# Distance cost [eur/km]
dist_cost = 0.12
# Stopping criteria for last traffic assignment
stopping_criteria_fine = {
	"max_iterations": 200,
	"relative_gap": 0.00001,
	"best_relative_gap": 0.001,
	"normalized_gap": 0.0005,
}
# Stopping criteria for traffic assignment in loop
stopping_criteria_coarse = {
	"max_iterations": 100,
	"relative_gap": 0.0001,
	"best_relative_gap": 0.01,
	"normalized_gap": 0.005,
}