import sys, pickle, random
import matplotlib.pyplot as plt
from scipy import integrate
from gauss import *





class Model():
    def __init__(self, gauss_params, a = None):
        """Initializing model with gaussian distributions"""
        self.gauss_params = gauss_params
        self.a = a
        self.components = self.build()
        self.p0 = self.params
        self.errors = [0 for i in range (0, len(self), 1)]


    def build(self):
        """Building list with components for model"""
        gauss_components = [Gauss(self.gauss_params[i], self.gauss_params[i + 1], self.gauss_params[i + 2])
                           for i in range(0, len(self.gauss_params), len(Gauss()))]
        return gauss_components


    def __len__(self):
        """Returning number of parameters of the used model"""
        return len(self.params)


    @ property
    def params(self):
        """Getting parameters of model"""
        params = np.array([self.components[i].params for i in range(0, len(self.components), 1)])
        return params.flatten()


    @ params.setter
    def params(self, params):
        """Setting parameters for model"""
        if len(params) != len(self.params):
            raise ValueError("params not compatible with model")
        init = 0
        for i in range(0, len(self.components), 1):
            p = [params[j] for j in range(init, init + len(self.components[i]), 1)]
            self.components[i].params = p
            init += len(self.components[i])
        for i in range(0, int(len(self.gauss_params)/len(Gauss()))-1, 1):
            for j in range(0, int(len(self.gauss_params)/len(Gauss()))-1-i, 1):
                if self.components[j].m > self.components[j+1].m:
                    self.components[j], self.components[j+1] = self.components[j+1], self.components[j]


    def __call__(self, x):
        """Returning superposition of individual functions of model"""
        if self.a == None:
            self.a = 0
        return sum(self.components[i](x)*(1+x)**self.a for i in range(0, len(self.components), 1))


    def normalize(self):
        """Normalizing model to unity"""
        f = lambda x: self(x)
        N, error = integrate.quad(f, -np.inf, np.inf)
        return 1/N


    def mean(self):
        """Calculating mean of model as integral of x*f(x)"""
        mean_list = []
        f = lambda x: x*self(x)
        mean, error = integrate.quad(f,0.0001, np.inf)
        int_params = self.params
        for i in range(0, 1000, 1):
            self.params = [self.params[j]+random.uniform(self.params[j]-self.errors[j], self.params[j]+self.errors[j]) for j in range(len(self))]
            m, error = integrate.quad(f, 0.0001, np.inf)
            mean_list.append(m)
            self.params = int_params
        return self.normalize()*mean, self.normalize()*np.std(mean_list)


    def __str__(self):
        """Printing intial and final parameters and mean of model"""
        parameters0 = "{0:>6}".format("")
        string0 = "\n"
        for i in range(0, len(self.components[0].params), 1):
            parameters0 += "{0:>15}".format("p"+str(i))
        for i in range(0, len(self.components), 1):
            values = "{0:>8}".format("Curve"+str(i+1))
            for j in range(0+3*i, len(self.components[0].params)+3*i, 1):
                values += "{0:15.3f}".format(self.p0[j])
            string0 += values+"\n"
        parameters = "{0:>3}".format("")
        for i in range(0, len(self.components[0].params), 1):
            parameters += "{0:>18}".format("p"+str(i))
        string = "\n"
        for i in range(0, len(self.components), 1):
            values = "{0:>8}".format("Curve"+str(i+1))
            for j in range(0+3*i, len(self.components[0].params)+3*i, 1):
                values += "{0:11.3f}{1:>1}{2:5.3f}".format(self.params[j], "+-", self.errors[j])
            string += values + "\n"
        mean, mean_sigma = self.mean()
        return "Initial parameters:\n\n"+parameters0+string0+"\n\n"+"Final parameters:\n\n"+parameters+string+"\n\n"\
               +"Mean:\n\n"+"{0:>18}{1:6.3f}{2:>}{3:4.3f}".format("Calculated mean:", mean, "+-", mean_sigma)


    def plot(self, ax, x, color, norm = None, mean = None):
        """Plotting (normalized) individual and superposition of individual model functions (and mean of model) on a matplotlib axes object"""
        if norm == None:
            norm = 1
        for i in range(0, len(self.components), 1):
            ax.plot(x, norm*self.components[i](x), color="deepskyblue", ls="--")
        ax.plot(x, norm*self(x), color, label="curve-fit")
        if mean != None:
            mean, mean_variance = self.mean()
            ax.axvline(mean, color='peru', label="calculated mean")


    def save(self, filepath):
        """Saving initial and final parameters and mean of model"""
        d = open(filepath+".txt", "a")
        sys.stdout = d
        print(self)
        d.close()
        sys.stdout = sys.__stdout__
        p = open(filepath+".bin", "ab")
        pickle.dump(self, p)
        p.close()
        plt.savefig(filepath + ".png")




if __name__ == "__main__":
    import matplotlib.pyplot as plt
    ax = plt.subplot()
    ax.grid()
    ax.set_title("Model")
    x = np.linspace(-10, 10, 100000)
    gauss_params = [-2, 0, 5, -1 ,8, 0.1, -1.5, 0, 0.9]
    model = Model(gauss_params)
    print(model)
    print("\n\n\n")
    model.plot(ax, x, "orange", mean = True)
    model.params = [1.5, 0.5, 2, 0.8 ,3, 0.5, 0.9, 1.5, 1]
    print(model)
    model.plot(ax, x, "magenta", mean = True)
    plt.legend(loc = "best")
    plt.show()
