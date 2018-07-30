import pickle, glob
import numpy as np
from model import *
from scipy import integrate




class Bias():
    def __init__(self, name_save_folder, bin_models, a = None):
        """Initializing narrow bin models, broad bin and bias model parameters
        (Amplitude A and exponant a) for bias estimation; setting error on parameters to 0"""
        self.name_save_folder = name_save_folder
        self.bin_models = bin_models
        self.A =  1
        self.a =  0
        self.errors = [0 for i in range(0, len(self), 1)]


    def __len__(self):
        """Returning number of parameters of the used model"""
        return 2


    @property
    def params(self):
        return [self.A, self.a]


    @params.setter
    def params(self, params):
        if len(params) != len(self):
            raise ValueError("Parameters not compatible with model")
        self.A, self.a = params[0], params[1]


    def __call__(self, x):
        """Returning superposition of Gaussian mixture models from individual bins multiplied by bias model"""
        func = sum(self.bin_models[i](x)/(1+x)**self.bin_models[i].a for i in range(0, len(self.bin_models),1))
        return func*self.A*(1+x)**self.a


    def normalize(self):
        """Calculating normalization factor for function defined in __call__()"""
        f = lambda x: self(x)
        N, error = integrate.quad(f, 0, np.inf)
        return 1/N


    def mean(self):
        """Calculating mean and corresponding std. deviation of model using Monte Carlo sampling"""
        mean_list = []
        f = lambda x: x*self(x)
        mean, error = integrate.quad(f, 0, np.inf)
        int_params = self.params
        for i in range(0, 1000, 1):
            self.params = [self.params[j]+random.uniform(-self.errors[j], self.errors[j]) for j in range(len(self))]
            mean_i, error = integrate.quad(f, 0, np.inf)
            mean_list.append(mean_i)
            self.params = int_params
        return self.normalize()*mean, self.normalize()*np.std(mean_list)


    def __str__(self):
        """Returning amplitude and exponent of bias model and mean of whole model (superpositions*A(1+x)**a)"""
        mean, sigma = self.mean()
        return "{0:>}{1:.3f}{2:>}{3:.3f}{4:>14}{5:.3f}{6:>}{7:.3f}{8:>21}{9:.3f}{10:>}{11:.3f}".format(
               "Amplitude: ", self.A, "+-", self.errors[0], "Exponent: ", self.a, "+-", self.errors[1], "Calculated mean: ", mean, "+-", sigma)+"\n"


    def plot(self, ax, x, color, norm = None, mean = None):
        """Plotting (normalized) superposition of individual narrow bin models on a matplotlib axes object"""
        if norm == None:
            norm = 1
        ax.plot(x, norm*self(x)/(self.A*(1+x)**self.a), color, label="summed sub-bin models", linewidth = 5)
        if mean == True:
            mean, mean_variance = self.mean()
            ax.axvline(mean, color='peru', label="mean calculated from summed sub-bin models", linewidth = 5)


    def plot_with_bias(self, ax, x, color, norm = None, mean = None):
        """Plotting (normalized) superposition of individual narrow bin models
        multiplied by the bias model on a matplotlib axes object"""
        if norm == None:
            norm = 1
        ax.plot(x, norm*self(x), color, label="summed sub-bin models multiplied with bias model", linewidth = 5)
        if mean == True:
            mean, mean_variance = self.mean()
            ax.axvline(mean, color='magenta', label="mean calculated from summed sub-bin models multiplied with bias model", linewidth = 5)


    def save(self, filepath):
        """Saving amplitude and exponent of bias model and plot of
        (normalized) superposition of individual narrow bin models (multiplied by the bias model)"""
        d = open(filepath+".txt", "a")
        sys.stdout = d
        print(self)
        d.close()
        sys.stdout = sys.__stdout__
        p = open(filepath+".bin", "ab")
        pickle.dump(self, p)
        p.close()
        plt.savefig(filepath+".png")


