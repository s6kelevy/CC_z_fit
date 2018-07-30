import emcee, time, corner
from data import *
from model import *
from emcee import PTSampler




class MCMC():
    def __init__(self, data, model, walkers, walker_offset, burn_in_steps, main_steps, priors):
        """Initialising data, model which should get fitted to the data, and general fit settings"""
        self.data = data
        self.model = model
        self.walkers = walkers
        self.walker_offset = walker_offset
        self.burn_in_steps = burn_in_steps
        self.main_steps = main_steps
        self.priors = priors
        self.sampler = None
        self.time0 = None
        self.time1 = None
        self.acc_frac = None
        self.chi2 = None
        self.BIC = None


    def prior(self, p):
        """Setting priors on parameters of model"""
        x = np.arange(0, len(self.priors), 1)
        for i in range(0, len(p), len(x)):
            for j in range(0, len(x), 1):
                if self.priors[j][0] < p[i+x[j]] < self.priors[j][1]:
                    result = 0.0
                else:
                    return -np.inf
        return result


    def lnprob(self, p, x, y, cov):
        """Calculating natural logarithm of Likelihood function using covariance matrix of data if priors are fulfilled"""
        self.model.params = p
        if self.prior(p) != -np.inf:
            chi_2 = np.dot(np.transpose(y - self.model(x)), np.dot(np.linalg.inv(cov), y - self.model(x)))
            lnlike = -0.5*chi_2 - np.log(np.sqrt((2*np.pi)**len(y)*np.linalg.det(cov)))
            return lnlike
        else:
            return -np.inf


    def fit(self, i=None, j=None):
        """Fitting model to data and determining best parameters, errors on parameters, run time, mean acceptance fraction, chi_square and BIC"""
        params = self.model.params
        ndim = len(self.model.params)
        self.sampler = emcee.EnsembleSampler(self.walkers, ndim, self.lnprob, a = 2, args=[self.data.x, self.data.y, self.data.cov])
        if i != None and j != None:
            print("\nRunning burn-in phase for data set", i,  "with", j, "fit curve(s) ...")
        p0 = [params + self.walker_offset*np.random.randn(ndim) for i in range(self.walkers)]
        time0 = time.time()
        pos, prob, state = self.sampler.run_mcmc(p0, self.burn_in_steps)
        time1 = time.time()
        self.time0 = time1 - time0
        self.sampler.reset()
        if i != None and j != None:
            print("Running MCMC for data set", i,  "with", j, "fit curve(s) ...\n\n")
        time0 = time.time()
        pos, prob, state = self.sampler.run_mcmc(pos, self.main_steps)
        time1 = time.time()
        self.time1 = time1 - time0
        self.sampler.reset()
        p0 = [pos[np.argmax(prob)] + self.walker_offset*np.random.randn(ndim) for i in range(self.walkers)]
        pos, prob, sate = self.sampler.run_mcmc(p0, 1000)
        self.model.params = [self.sampler.flatchain[:, i].mean() for i in range(0, ndim, 1)]
        self.model.errors = [self.sampler.flatchain[:, i].std() for i in range(0, ndim, 1)]
        self.acc_frac = np.mean(self.sampler.acceptance_fraction)
        self.chi2 = np.dot(np.transpose(self.data.y - self.model(self.data.x)), np.dot(np.linalg.inv(self.data.cov), self.data.y - self.model(self.data.x)))
        self.BIC = self.chi2 + ndim*np.log(len(self.data.x))


    def __str__(self):
        """Returning settings and analyze of fit"""
        settings = "\n\n\nSettings:\n\n  Walkers: "+str(self.walkers)+"\n  Burn-In steps: "+str(self.burn_in_steps)+"\n" \
                   "  Main steps: " + str(self.main_steps) +"\n\n\n"
        analyze = "Analyze:\n\n  Time for burn-in phase: "+str(round(self.time0, 0))+"s\n  Time for sample phase: "+str(round(self.time1, 0))+\
                  "s\n  Mean acceptance fraction: " + str(round(self.acc_frac, 3))+"\n  Chi2: "+str(round(self.chi2, 0))\
                   +"\n  BIC: "+str(round(self.BIC, 0))
        return settings+analyze


    def plot(self):
        """Plotting corner plots for analyze"""
        corner.corner(self.sampler.flatchain, labels=["p"+str(i) for i in range(0,  len(self.model.params), 1)])


    def save(self, filepath):
        """Saving settings and analyze of fit"""
        d = open(filepath+".txt", "a")
        sys.stdout = d
        print(self)
        d.close()
        sys.stdout = sys.__stdout__
        p = open(filepath+".bin", "ab")
        pickle.dump(self, p)
        p.close()































