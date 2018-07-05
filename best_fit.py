import os, shutil, pickle, sys
import matplotlib.pyplot as plt
import numpy as np


class Best_Fit():
    def __init__(self, data_set = None, all_fits = None):
        self.data_set = data_set+1
        self.all_fits = all_fits
        self.x = None
        self.y = None
        self.z = None
        if not os.path.exists("../Results"):
            raise ValueError("There is no data to analyze")
        if not os.path.exists("../Results/bin"+str(self.data_set)):
            raise ValueError("Data-Set"+str(self.data_set)+" does not exist")
        if not os.path.exists("../Results/bin"+str(self.data_set)+"/BIC-Table"):
            os.makedirs("../Results/bin"+str(self.data_set)+"/BIC-Table")
        else:
            shutil.rmtree("../Results/bin"+str(self.data_set)+"/BIC-Table")
            os.makedirs("../Results/bin"+str(self.data_set)+"/BIC-Table")
        if not os.path.exists("../Results/bin" + str(self.data_set) + "/Best_Fit"):
            os.makedirs("../Results/bin" + str(self.data_set) + "/Best_Fit")
        else:
            shutil.rmtree("../Results/bin" + str(self.data_set) + "/Best_Fit")
            os.makedirs("../Results/bin" + str(self.data_set) + "/Best_Fit")


    def best_fit(self):
        d = open("../Results/bin"+str(self.data_set)+"/"+str(1)+"Gauss/"+str(1)+"Gauss.bin", "rb")
        self.x = pickle.load(d)
        self.y = pickle.load(d)
        self.z = pickle.load(d)
        d.close()
        for i in range(1, self.all_fits, 1):
            d = open("../Results/bin"+str(self.data_set)+"/"+str(i+1)+"Gauss/"+str(i+1)+"Gauss.bin", "rb")
            x = pickle.load(d)
            y = pickle.load(d)
            z = pickle.load(d)
            d.close()
            if z.BIC < self.z.BIC:
                self.x = x
                self.y = y
                self.z = z
                self.z.BIC = z.BIC
        best_fit = self.x, self.y, self.z
        return best_fit


    def __str__(self):
        data_set = "Analyze for Data Set "+str(self.data_set)+":\n\n"
        title = "Nr. of            BIC\n" \
                "fit-curves\n"
        table = ""
        for i in range(0, self.all_fits, 1):
            d = open("../Results/bin"+str(self.data_set)+"/"+str(i+1)+"Gauss/"+str(i+1)+"Gauss.bin", "rb")
            x = pickle.load(d)
            y = pickle.load(d)
            z = pickle.load(d)
            d.close()
            table += "{0:5.0f}{1:>11}{2:5.3f}".format(i+1, " ", z.BIC)+"\n"
        return data_set+title+table+"\n\n"


    def save(self, filepath1, filepath2):
        d = open(filepath1+".txt", "w")
        sys.stdout = d
        print(self)
        d.close()
        sys.stdout = sys.__stdout__
        p = open(filepath1+".bin", "wb")
        pickle.dump(self, p)
        p.close()
        m, d, f = self.best_fit()
        m.save(filepath2)
        d.save(filepath2)
        f.save(filepath2)


        f.plot()
        plt.savefig(filepath2 + "_Analyze.png")
        fig, ax = plt.subplots(figsize=(20, 12))
        ax.grid()
        ax.set_title("Redshift Distribution")
        ax.set_xlabel("z")
        ax.set_ylabel("n(z)")
        x_max = max(d.x)
        x = np.linspace(0, x_max, 100000)
        d.plot(ax, "red")
        m.plot(ax, x, "k")
        plt.savefig(filepath2+".png")




if __name__ == "__main__":
    for i in range(0, 5, 1):
        bic = BIC(i+1, 10)
        print(bic)
        bic.save("../BIC/bin"+str(i+1)+"/BIC_bin"+str(i+1))
