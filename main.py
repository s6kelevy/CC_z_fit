from fit import *




bins =  ["../Data/bin_0.101t0.301.ascii", "../Data/bin_0.301t0.501.ascii", "../Data/bin_0.501t0.701.ascii","../Data/bin_0.701t0.901.ascii","../Data/bin_0.901t1.201.ascii"]
bins_cov = ["../Data/bin_0.101t0.301.covmat", "../Data/bin_0.301t0.501.covmat", "../Data/bin_0.501t0.701.covmat","../Data/bin_0.701t0.901.covmat","../Data/bin_0.901t1.201.covmat"]
broad_bin = ["../Data/bin_0.101t1.201.ascii"]
broad_bin_cov = ["../Data/bin_0.101t1.201.covmat"]
data_color = "red"
weights = [0.879744416989, 1.32956148749, 2.03726720346, 1.49372952652, 1.26487295888, 6.93383958441]
figure_title = [[0.1, 0.3], [0.3, 0.5], [0.5, 0.7], [0.7, 0.9], [0.9, 1.2], [0.1, 1.2]]
max_nbre_gauss_fits = 6
model_color = "blue"
walkers = 150
walker_offset = 1e-4
burn_in_steps = 500
main_steps = 10000
priors_gauss = [[0.01, 0.4], [0, 2], [0.035, 0.3]]
priors_bias = [[0,5],[-10,10]]
name_save_folder = "Results"


fit = Fit(bins, broad_bin, data_color, weights, figure_title, max_nbre_gauss_fits, model_color, walkers, walker_offset, burn_in_steps, main_steps, priors_gauss, priors_bias, name_save_folder, bins_cov, broad_bin_cov, normalize = True, mean = True)
fit.iterate(10)



































