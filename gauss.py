import numpy as np




class Gauss():
    def __init__(self, a=None, m=None, s=None):
        """Initializing amplitude, mean and std. deviation for a gaussian distribution"""
        self.a = a
        self.m = m
        self.s = s


    def __len__(self):
        """Returning number of parameters for gaussian distribution"""
        return 3


    @ property
    def params(self):
        """Getting amplitude, mean and std. deviation of gaussian distribution"""
        return [self.a, self.m, self.s]


    @ params.setter
    def params(self, params):
        """Setting amplitude, mean and std. deviatiation for gaussian distribution"""
        if len(params) != len(self):
            raise ValueError("params not compatible for gaussian distribution")
        self.a, self.m, self.s = params[0], params[1], params[2]


    def __str__(self):
        """Printing amplitude, mean and std. deviation of gaussian distribution"""
        return "Gauss(A = {self.a}, m = {self.m}, s = {self.s})".format(self=self)


    def __call__(self, x):
        """Returning gaussian function"""
        return self.a*np.exp(-((x-self.m)**2)/(2*self.s**2))


    def plot(self, ax, x, color):
        """Plotting gaussian function on a matplotlib axes object"""
        ax.plot(x, self(x), color = color, ls="--")




if __name__ == "__main__":
    import matplotlib.pyplot as plt
    ax = plt.subplot()
    ax.grid()
    ax.set_title("Gaussian Distribution")
    x = np.linspace(-10, 10, 100000)
    gauss = Gauss(1, 0, 2)
    print(gauss)
    gauss.plot(ax, x, "deepskyblue")
    gauss.params = [2, 6, 0.7]
    print(gauss)
    gauss.plot(ax, x, "green")
    plt.show()

