import emcee, time, corner
from data import *
from model import *
from scipy import integrate




class MCMC():
    def __init__(self, data, model, walkers, burn_in_steps, main_steps, priors):
        self.data = data
        self.model = model
        self.walkers = walkers
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
        x = np.arange(0, len(self.priors), 1)
        for i in range(0, len(p), len(x)):
            for j in range(0, len(x), 1):
                if self.priors[j][0] < p[i+x[j]] < self.priors[j][1]:
                    result = 0.0
                else:
                    return -np.inf
        return result


    def lnprob(self, p, x, y, cov):
        self.model.params =p
        chi_2 = np.dot(np.transpose(y - self.model(x)), np.dot(np.linalg.inv(cov), y - self.model(x)))
        lnlike = -0.5*chi_2
        return self.prior(p) + lnlike


    def fit(self, i=None, j=None):
        params = self.model.params
        ndim = len(params)
        p0 = [params+1e-3*np.random.randn(ndim) for i in range(self.walkers)]


        self.sampler = emcee.EnsembleSampler(self.walkers, ndim, self.lnprob, a=2, args=[self.data.x, self.data.y, self.data.cov])
        if i != None and j != None:
            print("\n\n\n\nRunning burn-in for data set", i+1,  "with", j+1, "fit curve(s)")
        time0 = time.time()


        pos, prob, state = self.sampler.run_mcmc(p0, self.burn_in_steps)
        p0 = [pos[np.argmax(prob)] + 1e-4*np.random.randn(ndim) for i in range(self.walkers)]
        self.sampler.reset()
        pos, prob, state = self.sampler.run_mcmc(p0, self.burn_in_steps)


        time1 = time.time()
        self.sampler.reset()
        self.time0 = time1-time0
        if i != None and j != None:
            print("Running production for data set", i+1,  "with", j+1, "fit curve(s)\n\n")
        time0 = time.time()
        pos, prob, state = self.sampler.run_mcmc(pos, self.main_steps, rstate0=state)
        time1 = time.time()
        self.time1 = time1-time0


        params = pos[np.argmax(prob)]
        errors = []
        for i in range(0, ndim, 1):
            std = self.sampler.flatchain[:, i].std()
            errors.append(std)
        self.model.params = params
        self.model.errors = errors


        self.acc_frac = np.mean(self.sampler.acceptance_fraction)
        self.chi2 = np.dot(np.transpose(self.data.y - self.model(self.data.x)), np.dot(np.linalg.inv(self.data.cov), self.data.y - self.model(self.data.x)))
        self.BIC = self.chi2 + ndim*np.log(len(self.data.x))


    def __str__(self):
        x = "\n\n\nSettings:\n\n  Walkers: "+str(self.walkers)+"\n  Burn-In Steps: "+str(self.burn_in_steps)+"\n" \
            "  Steps: " + str(self.main_steps) +"\n\n\n"
        y = "Analyze:\n\n  Time for burn-in: "+str(round(self.time0, 2))+"s\n  Time for main-run: "+str(round(self.time1, 2))+\
            "s\n  Mean acceptance fraction: " + str(round(self.acc_frac, 3)) + "\n  Chi2: "+str(round(self.chi2, 0))\
            +"\n  BIC: "+str(round(self.BIC, 0))
        return x+y


    def plot(self):
        samples = self.sampler.flatchain
        corner.corner(samples) #data, labels=[r"$x$", r"$y$", r"$\log \alpha$", r"$\Gamma \, [\mathrm{parsec}]$"], quantiles=[0.16, 0.5, 0.84], show_titles=True, title_kwargs={"fontsize": 12}


    def save(self, filepath):
        d = open(filepath+".txt", "a")
        sys.stdout = d
        print(self)
        d.close()
        sys.stdout = sys.__stdout__
        p = open(filepath+".bin", "ab")
        pickle.dump(self, p)
        p.close()
        f, ax = plt.subplots(figsize=(20, 12))
        ax = corner.corner(self.sampler.flatchain)
        plt.savefig(filepath + "_Analyze.png")






























    #   fig, axes = plt.subplots(len(self.model.get_params()), figsize=(10, 7), sharex=True)
    #   for i in range(len(self.model.get_params())):
    #     ax = axes[i]
    #       ax.plot(samples[:, i], "k", alpha=0.3)
    #       ax.set_xlim(0, len(samples))
    # ax.set_ylabel(labels[i])
    # ax.yaxis.set_label_coords(-0.1, 0.5)
    #   axes[-1].set_xlabel("step number")
    #  plt.show()

    #  length = len(self.sampler.flatchain[:, 0])
    #  a = []
    #  for i in range(0, self.walkers, 1):
    #      for j in range(i*self.main_steps, i*self.main_steps+self.main_steps-50, 1):
    #           a.append(j)
    #  l = np.delete(self.sampler.flatchain[:, 1], a,0)
    #  m = np.delete(self.sampler.flatchain[:, 1],a,0)
    #   k = np.delete(self.sampler.flatchain[:, 2], a,0)
    #  ndim = len(self.model.get_params())
    #  fig, axes = plt.subplots(ndim, sharex=True)
    #  for i in range(0, ndim, 1):
    #      axs = axes[i]
    #      axs.set_xticks(np.arange(0, 5000, 100))
    #      x = np.linspace(0, len(np.delete(self.sampler.flatchain[:, i], a,0)), len(np.delete(self.sampler.flatchain[:, i], a,0)))
    #      axs.plot(x, np.delete(self.sampler.flatchain[:, i], a,0), '-', color='k', alpha=0.3)
    #   axes[-1].set_xlabel("step n")
