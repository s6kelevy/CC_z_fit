from fit import *




bins =  ["../Raw_Data_2/CC_0.101z0.301.bref", "../Raw_Data_2/CC_0.301z0.501.bref", "../Raw_Data_2/CC_0.501z0.701.bref","../Raw_Data_2/CC_0.701z0.901.bref", "../Raw_Data_2/CC_0.901z1.201.bref"]
bins_cov = ["../Raw_Data_2/CC_0.101z0.301_bref.cov", "../Raw_Data_2/CC_0.301z0.501_bref.cov", "../Raw_Data_2/CC_0.501z0.701_bref.cov", "../Raw_Data_2/CC_0.701z0.901_bref.cov","../Raw_Data_2/CC_0.901z1.201_bref.cov"]
large_bin = ["../Raw_Data_2/CC_0.101z1.201.bref"]
large_bin_cov = ["../Raw_Data_2/CC_0.101z1.201_bref.cov"]
weight = [0.879744416989, 1.32956148749, 2.03726720346, 1.49372952652, 1.26487295888, 6.93383958441]
data_color = "red"
max_nbre_gauss_fits = 3
fit_color = "black"
walkers = 100
burn_in_steps = 500
main_steps = 500
priors_gauss = [[0,0.05],[0,1.1], [0.032, 0.5]]
priors_bias = [[-5,5],[-5,5]]
name_save_folder = "Results_Raw_Data_2"
title = ["0.1 < z $\leq$ 0.3", "0.3  <z $\leq$ 0.5", "0.5 < z $\leq$ 0.7", "0.7 < z $\leq$ 0.9", "0.9 < z $\leq$ 1.2", "0.1 < z $\leq$ 1.2"]


fit = Fit(bins, data_color, max_nbre_gauss_fits, fit_color, walkers, burn_in_steps, main_steps, priors_gauss, name_save_folder, title, large_bin, weight, priors_bias, bins_cov, large_bin_cov, normalize = False, mean = True)
#fit.run()
#fit.get_best_model()
#fit.get_bias()
fit.iterate()



















































"""
data_arr =  ["../Data/bin_0.101t0.301.ascii", "../Data/bin_0.301t0.501.ascii", "../Data/bin_0.501t0.701.ascii","../Data/bin_0.701t0.901.ascii", "../Data/bin_0.901t1.201.ascii","../Data/CC_0.101t1.201.ascii"]
cov_arr = ["../Data/bin_0.101t0.301.covmat", "../Data/bin_0.301t0.501.covmat", "../Data/bin_0.501t0.701.covmat", "../Data/bin_0.701t0.901.covmat","../Data/bin_0.901t1.201.covmat", "../Data/bin_0.101t1.201.covmat"]


data_arr =  ["../Raw_Data_1/CC_0.101z0.301.bref", "../Raw_Data_1/CC_0.301z0.501.bref", "../Raw_Data_1/CC_0.501z0.701.bref","../Raw_Data_1/CC_0.701z0.901.bref", "../Raw_Data_1/CC_0.901z1.201.bref","../Raw_Data_1/CC_0.101z1.201.bref"]
cov_arr = ["../Raw_Data_1/CC_0.101z0.301_bref.cov", "../Raw_Data_1/CC_0.301z0.501_bref.cov", "../Raw_Data_1/CC_0.501z0.701_bref.cov", "../Raw_Data_1/CC_0.701z0.901_bref.cov","../Raw_Data_1/CC_0.901z1.201_bref.cov", "../Raw_Data_1/CC_0.101z1.201_bref.cov"]


data_arr =  ["../Raw_Data_2/CC_0.101z0.301.bref", "../Raw_Data_2/CC_0.301z0.501.bref", "../Raw_Data_2/CC_0.501z0.701.bref","../Raw_Data_2/CC_0.701z0.901.bref", "../Raw_Data_2/CC_0.901z1.201.bref","../Raw_Data_2/CC_0.101z1.201.bref"]
cov_arr = ["../Raw_Data_2/CC_0.101z0.301_bref.cov", "../Raw_Data_2/CC_0.301z0.501_bref.cov", "../Raw_Data_2/CC_0.501z0.701_bref.cov", "../Raw_Data_2/CC_0.701z0.901_bref.cov","../Raw_Data_2/CC_0.901z1.201_bref.cov", "../Raw_Data_2/CC_0.101z1.201_bref.cov"]
"""