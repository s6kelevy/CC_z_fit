from gauss import *
from mcmc import *
from best_model import *
from bias import *
from iterate import *
from folder import *
import numpy as np
import matplotlib.pyplot as plt
import pickle, glob




class Fit():
    def __init__(self, bins, broad_bin, data_color, weights, figure_title, max_nbre_gauss_fits, model_color, walkers, walker_offset, burn_in_steps, main_steps, priors_gauss, priors_bias, name_save_folder, bins_cov = None, broad_bin_cov = None, normalize=None, mean=None):
        self.bins = bins
        self.broad_bin = broad_bin
        self.data_color = data_color
        self.weights = weights
        self.figure_title = figure_title
        self.max_nbre_gauss_fits = max_nbre_gauss_fits
        self.model_color = model_color
        self.walkers = walkers
        self.walker_offset = walker_offset
        self.burn_in_steps = burn_in_steps
        self.main_steps = main_steps
        self.priors_gauss = priors_gauss
        self.priors_bias = priors_bias
        self.name_save_folder = name_save_folder
        self.bins_cov = bins_cov
        self.broad_bin_cov = broad_bin_cov
        self.normalize = normalize
        self.mean = mean
        self.a = 0


    def figure(self, i):
        """Creating figure and ax object for later data and model plots"""
        fig, ax = plt.subplots(figsize=(20, 12))
        ax.xaxis.set_tick_params(labelsize= 36)
        ax.yaxis.set_tick_params(labelsize=36)
        ax.set_title(str(self.figure_title[i][0])+"< $z_{\mathrm{phot}}$ $\leq$"+str(self.figure_title[i][1]), fontsize = 40)
        ax.set_xlabel("$z$", fontsize=36)
        ax.set_ylabel("$n(z)$", fontsize=36)
        ax.axhline(0, color='black')
        ax.axvspan(self.figure_title[i][0], self.figure_title[i][1], alpha = 0.2, color = "grey", label = "tomographic bin")
        return fig, ax


    def run(self, nber_of_curves = None):
        """Fitting 1 to maximum number of Gaussian distributions to each narrow bin if no specific number is given,
        in the last case, only the specific number of curves gets fitted to each narrow bin; the results for each
        narrow bin get saved in a specific folder """
        for i in range(0, len(self.bins), 1):
            if self.bins_cov == None:
                data = Data(self.bins[i])
            else:
                data = Data(self.bins[i], self.bins_cov[i])
            if  nber_of_curves == None:
                min_fits, max_fits = 1,  self.max_nbre_gauss_fits+1
            else:
                min_fits, max_fits = nber_of_curves[i], nber_of_curves[i]+1
            for j in range(min_fits, max_fits, 1):
                fig, ax = self.figure(i)
                folder = Folder(self.name_save_folder, i+1, j)
                folder.make_folder_run()
                interval = (self.priors_gauss[1][1]-self.priors_gauss[1][0])/j
                z_0 = interval/3
                gauss_params = []
                for k in range(0, j*len(self.priors_gauss), 3):
                    gauss_params.extend([np.mean(self.priors_gauss[0], axis=0), z_0, np.mean(self.priors_gauss[2], axis=0)])
                    z_0 += interval/3
                components = [Gauss(gauss_params[i], gauss_params[i+1], gauss_params[i+2]) for i in range(0, len(gauss_params), 3)]
                model = Model(components, self.a)
                mcmc = MCMC(data, model, self.walkers, self.walker_offset, self.burn_in_steps, self.main_steps, self.priors_gauss)
                mcmc.fit(i+1, j)
                x_max = max(np.loadtxt(self.bins[i])[:, 0])
                x = np.linspace(0, x_max, 100000)
                if self.normalize == True:
                    norm = model.normalize()
                else:
                    norm = None
                data.plot(ax, self.data_color, norm)
                model.plot(ax, x, self.model_color, norm, self.mean)
                ax.legend(loc="best", prop={'size': 25})
                model.save("../"+self.name_save_folder+"/bin"+str(i+1)+"/"+str(j)+"Gauss/"+str(j)+"Gauss")
                mcmc.save("../"+self.name_save_folder+"/bin"+str(i+1)+"/"+str(j)+"Gauss/"+str(j)+"Gauss")


    def get_best_model(self):
        """Getting best model for each narrow bin based on the bayesian information criterion (BIC);
        the BIC value of each model and the best model get saved in specific folders for each narrow bin"""
        for i in range(0, len(self.bins), 1):
            folder = Folder(self.name_save_folder, i+1)
            folder.make_folder_get_best_model()
            best_model = Best_Model(self.name_save_folder, i+1, self.max_nbre_gauss_fits)
            print(best_model)
            best_model.best()
            best_model.save("../"+self.name_save_folder+"/bin"+str(i+1)+"/BIC-Table/BIC-Table", "../"+self.name_save_folder+"/bin"+str(i+1)+"/Best_Fit", )


    def get_bias(self, nber_of_curves):
        """Getting bias by weighting and summing the best model of each narrow bin and fitting the weighted sum with a bias power law model,
        containing an amplitude and an exponent, to the weighted large bin; the weights are based on the number of galaxies per arcmin^2 in each tomographic bin 
        the results get saved in a specific folder"""
        folder = Folder(self.name_save_folder)
        folder.make_folder_get_bias()
        data = Data(self.broad_bin[0], self.broad_bin_cov[0])
        bin_models = []
        for i in range(0, len(self.bins), 1):
            d = open("../"+self.name_save_folder+"/bin"+str(i+1)+"/"+str(nber_of_curves[i])+"Gauss/"+str(nber_of_curves[i])+"Gauss.bin", "rb")
            bin_models.append(pickle.load(d))
            d.close()
        data.y = self.weights[-1]*data.y
        data.yerr = self.weights[-1]*data.yerr
        for i in range(0, len(self.bins), 1):
            p = bin_models[i].params
            for j in range(0, len(p), 3):
                p[j] = self.weights[i]*p[j]
            bin_models[i].params = p
        bias = Bias(self.name_save_folder, bin_models)
        fig, ax = self.figure(len(self.figure_title)-1)
        x_max = max(np.loadtxt(self.broad_bin[0])[:, 0])
        x = np.linspace(0, x_max, 100000)
        if self.normalize == True:
            norm = bias.normalize()
        else:
            norm = None
        data.plot(ax, self.data_color, norm)
        bias.plot(ax, x, "green", norm, self.mean)
        print("Calculating bias parameter for next iteration step ...")
        mcmc = MCMC(data, bias, self.walkers, self.walker_offset, self.burn_in_steps, self.main_steps, self.priors_bias)
        mcmc.fit()
        print(bias)
        print("\n\n")
        bias.plot_with_bias(ax, x, "blue", norm, self.mean)
        ax.legend(loc="best", prop={'size': 25})
        bias.save("../" + self.name_save_folder + "/Bias/Bias")
        self.a = bias.a


    def iterate(self, iterate_steps):
        """Iterating def run() and def get_bias() for a given number of iteration steps to recover
        the bias exponent iteratively"""
        step, nber_of_curves = 0, []
        print("Iteration step", step, "(Initialisation)")
        self.run()
        self.get_best_model()
        for i in range(1, len(self.bins)+1, 1):
            d = open(glob.glob("../" + self.name_save_folder + "/bin" + str(i) + "/Best_Fit/*.bin")[0], "rb")
            nber_of_curves.append(len(pickle.load(d).components))
            d.close()
        self.get_bias(nber_of_curves)
        while step < iterate_steps:
            step += 1
            print("Iteration step", step)
            self.run(nber_of_curves)
            self.get_bias(nber_of_curves)

