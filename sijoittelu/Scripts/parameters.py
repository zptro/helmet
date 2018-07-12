length_weight = 0.2
stopping_criteria_fine = {
	"max_iterations": 200,
	"relative_gap": 0.00001,
	"best_relative_gap": 0.001,
	"normalized_gap": 0.0005,
}
stopping_criteria_coarse = {
	"max_iterations": 100,
	"relative_gap": 0.0001,
	"best_relative_gap": 0.01,
	"normalized_gap": 0.005,
}