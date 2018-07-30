import numpy as np




class Gauss():
    def __init__(self, A = None, m = None, s = None):
        """Initializing amplitude (A), mean (m) and std. deviation (s) for a Gaussian distribution"""
        self.A = A
        self.m = m
        self.s = s


    def __len__(self):
        """Returning number of parameters for Gaussian distribution"""
        return 3


    @ property
    def params(self):
        return [self.A, self.m, self.s]


    @ params.setter
    def params(self, params):
        if len(params) != len(self):
            raise ValueError("Parameters not compatible for Gaussian distribution")
        self.A, self.m, self.s = params[0], params[1], params[2]


    def __str__(self):
        return "Gauss(A = {self.A}, m = {self.m}, s = {self.s})".format(self=self)


    def __call__(self, x):
        return self.A*np.exp(-((x-self.m)**2)/(2*self.s**2))


    def plot(self, ax, x, color):
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

