import sys, pickle
import numpy as np





class Data():
    def __init__(self, filepath_1, filepath_2 = None, a = None):
        """Initializing x- and y-values, error on y-values and excluding NaN data values"""
        if a == None:
            a = 0
        data_1 = np.loadtxt(filepath_1)
        self.x = np.array(np.delete(data_1[:, 0], np.where(np.isnan(data_1[:, 0]) == True)))
        self.y = np.array(np.delete(data_1[:, 1], np.where(np.isnan(data_1[:, 1]) == True))/ ((1+self.x)**a))
        self.yerr = np.array(np.delete(data_1[:, 2], np.where(np.isnan(data_1[:, 2]) == True))/((1+self.x)**a))
        if filepath_2 == None:
            self.cov = np.array(self.yerr)*self.yerr*np.eye(len(self.yerr), dtype=int)
        else:
            data_2 = np.loadtxt(filepath_2)
            self.cov = np.reshape(np.delete(data_2.flatten(), np.where(np.isnan(data_2.flatten()) == True)),
                                  (len(self.yerr), len(self.yerr)))/((1+self.x)**a)


    def mean(self):
        """Calculating mean of data as sum of x*p(x)"""
        mean, mean_variance, norm, i = 0, 0, 0, 0
        while self.y[i] >= 0 and i < len(self.y)-1:
            norm += self.y[i]
            i += 1
        p = self.y[:i]/norm
        return sum(self.x[i]*p[i] for i in range(0, i, 1))


    def __str__(self):
        """Printing mean of data"""
        mean = self.mean()
        return "{0:>12}{1:6.3f}".format("Data mean:", mean)


    def plot(self, ax, color, norm = None, mean = None):
        """Plotting (normalized) data (and mean of data) on a matplotlib axes object"""
        if norm == None:
            norm = 1
        ax.errorbar(self.x, norm*self.y, yerr = norm*self.yerr, color = color,
                    ecolor = color, marker = "x", ls = "", label = "redshift distribution")
        if mean != None:
            mean = self.mean()
            ax.axvline(mean, color = 'blue', label = "data mean")


    def save_mean(self, filepath):
        """Saving mean of data"""
        d = open(filepath+".txt", "a")
        sys.stdout = d
        print(self)
        d.close()
        sys.stdout = sys.__stdout__
        p = open(filepath+".bin", "ab")
        pickle.dump(self, p)
        p.close()




if __name__ == "__main__":
    import matplotlib.pyplot as plt
    ax = plt.subplot()
    ax.grid()
    ax.set_title("Redshift Distribution")
    ax.set_xlabel("z")
    ax.set_ylabel("n(z)")
    d = Data("../Raw_Data_2/CC_0.101z0.301.bref", "../Raw_Data_2/CC_0.101z0.301_bref.cov")
    print(d)
    d.plot(ax, "red", mean = True)
    plt.legend(loc = "best")
    plt.show()













