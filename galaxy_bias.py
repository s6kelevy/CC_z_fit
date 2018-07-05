from data import *
from model import *





class Galaxy_Bias():
    def __init__(self, bins, data, weight):
        self.bins = bins
        self.data = data
        self.weight = weight
        self.params = None
        self.chi2 = None
        self.a = 0


    def open(self, i):
        d = open("../Results/bin"+str(i+1)+"/Best_Fit/Best_Fit.bin", "rb")
        x = pickle.load(d)
        d.close()
        return x.get_params()


    def weighted(self):
        self.data.y = self.weight[len(self.weight)-1]*np.array(self.data.y)
        self.data.yerr = self.weight[len(self.weight)-1]*np.array(self.data.yerr)
        self.params = []
        for i in range(0, len(self.bins), 1):
            p = self.open(i)
            for j in range(0, len(p), 3):
                p[j] = p[j]*self.weight[i]
            self.params += p


    def __call__(self, x):
        p = self.params
        function = 0
        for i in range(0,len(self.params), 3):
            function += p[i]*np.exp(-((x-p[i+1])**2)/(2*p[i+2]**2))#*(1+x)**self.a
        return function*(1+x)**self.a


    def chi_square(self):
       return np.dot(np.transpose(self.data.y - self(self.data.x)), np.dot(np.linalg.inv(self.data.cov), self.data.y - self(self.data.x)))


    def plot(self, ax, x, color):
        ax.plot(self.data.x, self.data.y, color=color, marker="x", ls="None")
        ax.errorbar(self.data.x, self.data.y, yerr = self.data.yerr, ecolor=color, ls="None")
        ax.plot(x, self(x), "k-", label="curve-fit")


    def iterate(self):
        print(self.a)
        self.chi2 = self.chi_square()
        print(self.chi2)
        self.a += 0.000001
        chi_new = self.chi_square()
        if chi_new < self.chi2:
            while chi_new < self.chi2:
                self.chi2 = chi_new
                self.a += 0.000001
                chi_new = self.chi_square()
        else:
            self.a -= 0.000002
            chi_new = np.dot(np.transpose(self.data.y - self(self.data.x)), np.dot(np.linalg.inv(self.data.cov), self.data.y - self(self.data.x)))
            while chi_new < self.chi2:
                self.chi2 = chi_new
                self.a -= 0.000001
                chi_new = self.chi_square()
        print(self.a)
        print(self.chi2)
