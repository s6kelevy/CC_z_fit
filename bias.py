import pickle
import numpy as np
from model import *
from scipy import integrate




class Bias():
    def __init__(self, name_save_folder, bins, data, weight, a = None):
        self.name_save_folder = name_save_folder
        self.bins = bins
        self.data = data
        self.weight = weight
        self.A =  1
        self.a =  a
        self.models = []


    def get_models(self):
        for i in range(0, len(self.bins), 1):
            d = open("../"+self.name_save_folder+"/bin"+str(i+1)+"/Best_Fit/Best_Fit.bin", "rb")
            self.models.append(pickle.load(d))
            d.close()


    def weighted(self):
        self.data.y = self.weight[-1]*np.array(self.data.y)/(self.A*(1+self.data.x)**self.a)
        self.data.yerr = self.weight[-1]*np.array(self.data.yerr)
        self.get_models()
        for i in range(0, len(self.bins), 1):
            p = self.models[i].params
            for j in range(0, len(p), 3):
                p[j] = p[j]*self.weight[i]
            self.models[i].params = p


    def __len__(self):
        return 2


    @property
    def params(self):
        """Getting amplitude and exponent of correction model"""
        return [self.A, self.a]


    @params.setter
    def params(self, params):
        """Setting amplitude and exponent for correction model"""
        if len(params) != len(self):
            raise ValueError("params not compatible with model")
        self.A, self.a = params[0], params[1]


    def __str__(self):
        """Printing amplitude and exponent of correction model"""
        return "Amplitude = {self.A}, Exponent = {self.a}\n\n".format(self=self)


    def __call__(self, x):
        """Returning superposition of models from individual bins"""
        func = sum(self.models[i](x) for i in range(0, len(self.bins),1))
        return func/(self.A*(1+x)**self.a)


    def plot(self, ax, x, color):
        """Plotting (normalized) superposition of models from individual bins on a matplotlib axes object"""
        ax.plot(x, self(x), color, label="curve-fit")


    def chi2(self):
        return np.dot(np.transpose(self.data.y - self(self.data.x)), np.dot(np.linalg.inv(self.data.cov), self.data.y - self(self.data.x)))


    def save(self, filepath):
        d = open(filepath+".txt", "a")
        sys.stdout = d
        print(self)
        d.close()
        sys.stdout = sys.__stdout__
        p = open(filepath+".bin", "ab")
        pickle.dump(self, p)
        p.close()
        plt.savefig(filepath+".png")

