import sys, pickle
import numpy as np




class Data():
    def __init__(self, filepath_1, filepath_2 = None):
        """Initializing x- and y-values, error on y-values, covariance matrix and excluding NaN data values;
        if no covariance matrix is given, a covariance matrix will be generated out of the y error values"""
        data_1 = np.loadtxt(filepath_1)
        self.x = np.array(np.delete(data_1[:, 0], np.where(np.isnan(data_1[:, 0]) == True)))
        self.y = np.array(np.delete(data_1[:, 1], np.where(np.isnan(data_1[:, 1]) == True)))
        self.yerr = np.array(np.delete(data_1[:, 2], np.where(np.isnan(data_1[:, 2]) == True)))
        if filepath_2 == None:
            self.cov = np.array(self.yerr)*self.yerr*np.eye(len(self.yerr), dtype=int)
        else:
            data_2 = np.loadtxt(filepath_2)
            self.cov = np.reshape(np.delete(data_2.flatten(), np.where(np.isnan(data_2.flatten()) == True)),
                                  (len(self.yerr), len(self.yerr)))


    def plot(self, ax, color, norm = None):
        """Plotting (normalized) data on a matplotlib axes object"""
        if norm == None:
            norm = 1
        ax.errorbar(self.x, norm*self.y, yerr = norm*self.yerr, color = color, ecolor = color,
                    marker = ".", ls = "", label = "redshift distribution", markersize = 20, linewidth = 5)




if __name__ == "__main__":
    import matplotlib.pyplot as plt
    ax = plt.subplot()
    ax.grid()
    ax.set_title("Redshift Distribution")
    ax.set_xlabel("z")
    ax.set_ylabel("n(z)")
    d = Data("../Data/bin_0.901t1.201.ascii", "../Data/bin_0.901t1.201.covmat")
    d.plot(ax, "red")
    plt.legend(loc = "best")
    plt.show()













