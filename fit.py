from mcmc import *
from best_model import *
from bias import *
from iterate import *
from folder import *
import numpy as np
import matplotlib.pyplot as plt




class Fit():
    def __init__(self, bins, data_color, max_nbre_gauss_fits, fit_color, walkers, burn_in_steps, main_steps, priors_gauss, name_save_folder, title, large_bin, weight, priors_bias, bins_cov = None, large_bin_cov = None, normalize=None, mean=None, a = None):
        self.bins = bins
        self.bins_cov = bins_cov
        self.data_color = data_color
        self.max_nbre_gauss_fits = max_nbre_gauss_fits
        self.fit_color = fit_color
        self.walkers = walkers
        self.burn_in_steps = burn_in_steps
        self.main_steps = main_steps
        self.priors_gauss = priors_gauss
        self.name_save_folder = name_save_folder
        self.title = title
        self. large_bin = large_bin
        self.weight = weight
        self.priors_bias = priors_bias
        self.large_bin_cov = large_bin_cov
        self.normalize = normalize
        self.a = 0
        self.mean = mean
        self.chi2 = None



    def figure(self, i):
        """creating figure and ax object"""
        fig, ax = plt.subplots(figsize=(20, 12))
        ax.grid()
        ax.xaxis.set_tick_params(labelsize= 17)
        ax.yaxis.set_tick_params(labelsize=17)
        ax.set_title(self.title[i], fontsize=17)
        ax.set_xlabel("z", fontsize=17)
        ax.set_ylabel("n(z)", fontsize=17)
        return fig, ax


    def run(self):
        """Fitting from 1 to maximum number of gaussian distributions for each bin"""
        for i in range(0, len(self.bins), 1):
            if self.bins_cov == None:
                data = Data(self.bins[i])
            else:
                data = Data(self.bins[i], self.bins_cov[i])
            if self.normalize == True:
                norm = model.normalize()
            else:
                norm = None
            for j in range(0, self.max_nbre_gauss_fits, 1):
                fig, ax = self.figure(i)
                folder = Folder(self.name_save_folder, i, j)
                folder.make_folder_run()
                gauss_params = np.mean((j + 1) * self.priors_gauss, axis=1)
                model = Model(gauss_params, self.a)
                mcmc = MCMC(data, model, self.walkers, self.burn_in_steps, self.main_steps, self.priors_gauss)
                mcmc.fit(i, j)
                x_max = max(np.loadtxt(self.bins[0])[:, 0])
                x = np.linspace(0, x_max, 100000)
                data.plot(ax, self.data_color, norm, self.mean)
                model.plot(ax, x, self.fit_color, norm, self.mean)
                ax.legend(loc=9, bbox_to_anchor=(0.5, -0.08), ncol=4)
                model.save("../" + self.name_save_folder + "/bin" + str(i + 1) + "/" + str(j + 1) + "Gauss/" + str(
                    j + 1) + "Gauss")
                data.save_mean("../" + self.name_save_folder + "/bin" + str(i + 1) + "/" + str(j + 1) + "Gauss/" + str(
                    j + 1) + "Gauss")
                mcmc.save("../" + self.name_save_folder + "/bin" + str(i + 1) + "/" + str(j + 1) + "Gauss/" + str(
                    j + 1) + "Gauss")


    def get_best_model(self):
        """Getting best curve-fit for each bin based on the bayesian information criterion (BIC)"""
        for bin in range(0, len(self.bins), 1):
            folder = Folder(self.name_save_folder, bin)
            folder.make_folder_get_best_fit()
            best_fit = Best_Fit(self.name_save_folder, bin, self.max_nbre_gauss_fits)
            print(best_fit)
            best_fit.save("../" + self.name_save_folder + "/bin" + str(bin + 1) + "/BIC-Table/BIC-Table",
                          "../" + self.name_save_folder + "/bin" + str(bin + 1) + "/Best_Fit/Best_Fit")



    def get_bias(self):
        """Getting bias by summing the best models for each bin and fitting the sum with a bias term on the large bin"""
        folder = Folder(self.name_save_folder)
        folder.make_folder_get_bias()
        data = Data(self.large_bin[0], self.large_bin_cov[0])
        bias = Bias(self.name_save_folder, self.bins, data, self.weight, self.a)
        bias.weighted()
        print(bias)
        mcmc = MCMC(bias.data, bias, self.walkers, self.burn_in_steps, self.main_steps, self.priors_bias)
        mcmc.fit()
        fig, ax = self.figure(len(self.title)-1)
        x_max = max(np.loadtxt(self.bins[0])[:, 0])
        x = np.linspace(0, x_max, 100000)
        data.plot(ax, self.data_color)
        bias.plot(ax, x, "gold")
        print(bias)
        bias.save("../"+self.name_save_folder+"/Bias/Bias")
        return bias.a
    #            self.chi2 = bias.chi2()
     #          print(self.chi2)


    def iterate(self):
        x = 0
        while x < 2:
            print("Iteration step", x+1)
            self.run()
            self.get_best_model()
            self.a = self.get_bias()
            x +=1
