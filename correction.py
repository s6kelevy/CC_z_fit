import pickle
import numpy as np
from model import *
from scipy import integrate




class Correction():
    def __init__(self, bins, data, weight):
        self.bins = bins
        self.data = data
        self.weight = weight
        self.a = 0
        self.A = 1
        self.c1, self.c2, self.c3, self.c4, self.c5 = 1,1,1,1,1
        self.models = []


    def get_models(self):
        for i in range(0, len(self.bins), 1):
            d = open("../Results/bin"+str(i+1)+"/Best_Fit/Best_Fit.bin", "rb")
            self.models.append(pickle.load(d))
            d.close()


    def weighted(self):
        self.data.y = self.weight[len(self.weight)-1]*np.array(self.data.y)
        self.data.yerr = self.weight[len(self.weight)-1]*np.array(self.data.yerr)
        self.get_models()
        for i in range(0, len(self.bins), 1):
            p = self.models[i].get_params()
            for j in range(0, len(p), 3):
                p[j] = p[j]*self.weight[i]
            self.models[i].set_params(p)


    def __len__(self):
        return 5


    def get_params(self):
       # params = [self.a] + [self.A]
        params = [self.c1]+[self.c2]+[self.c3]+[self.c4]+[self.c5]
        return params


    def set_params(self, params):
        if len(params) != len(self):
            raise ValueError("params not compatible with model")
       # self.a = params[0]
       # self.A = params[1]
        self.c1, self.c2, self.c3, self.c4, self.c5 = params[0], params[1], params[2], params[3], params[4]



    def __str__(self):
        return "a = {self.a}, A = {self.A}".format(self=self)


  #  def __call__(self, x):
  #      function = 0
   #     for i in range(0, len(self.models), 1):
   #         for j in range(0, len(self.models[i]), 1):
    #            function += self.models[i].components[j](x)
    #    return self.A*function*(1+x)**self.a


    def __call__(self, x):
        function = 0
        C = [self.c1, self.c2, self.c3, self.c4, self.c5]
        for i in range(0, len(self.models), 1):
            for j in range(0, len(self.models[i]), 1):
                function += C[i]*self.models[i].components[j](x)
        return function



    def plot(self, ax, x, color):
        ax.plot(x, self(x), color, label="curve-fit")
        ax.plot(x, (1+x)**self.a, "y", label="curve-fit")
        f = lambda x: self(x)
        integral, error = integrate.quad(f, 0.00001, np.inf)
        print(integral)




if __name__ == "__main__":
    import matplotlib.pyplot as plt


    ax = plt.subplot()
    ax.grid()
    ax.set_title("Correction")
    x = np.linspace(-10, 10, 100)


    correction = Correction(4, "green")
    print(correction.get_params())
    correction.plot(ax, x)


    correction.set_params([5])


    print(correction.get_params())
    correction.plot(ax, x)


    plt.show()