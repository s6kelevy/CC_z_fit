import pickle
from model import *




class Iterate():
    def __init__(self, folder, i, priors, x):
        self.folder = folder
        self.model = None
        self.correction = []
        self.make_model(i, priors, x)


    def make_model(self, i, priors, x):
        d = open("../" + self.folder + "/bin" + str(i + 1) + "/Best_Fit/Best_Fit.bin", "rb")
        nbre = len(pickle.load(d).components)
        gauss_params = nbre*np.mean(priors, axis=1)
        self.model = Model(gauss_params)
        d.close()
        j =0
        while j < x+1:
            d = open("../" + self.folder + "/Bias/Bias.bin", "rb")
            self.correction.append(pickle.load(d))
            j += 1
        d.close()


    def __len__(self):
        return len(self.model)


    def get_params(self):
        return self.model.get_params()


    def set_params(self, params):
        return self.model.set_params(params)


    def __str__(self):
        return "Amplitudes = {self.B}, Exponents = {self.b}\n\n".format(self=self)


    def __call__(self, x):
        A = self.correction[len(self.correction)-1].A
        a = self.correction[len(self.correction)-1].a
        return A*self.model(x)*(1+x)**a


    def save(self, filepath):
        d = open(filepath+".bin", "wb")
        pickle.dump(self.model, d)
        d.close()


