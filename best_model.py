import os, shutil, pickle, sys
import numpy as np




class Best_Model():
    def __init__(self, name_save_folder, bin, bin_models):
        """Initializing narrow bin for which best model should be obtained out of all the bin models"""
        self.name_save_folder = name_save_folder
        self.bin = bin
        self.bin_models = bin_models
        self.m = None
        self.f = None
        self.d = None


    def __str__(self):
        """Returning for each model of the bin the number of corresponding Gaussian distributions and corresponding BIC value"""
        bin = "Analyze for bin "+str(self.bin)+":\n\n"
        title = "{0:>6}{1:>10}".format("Nr. of", "BIC")+"\ncurves\n"
        table = ""
        for i in range(0, self.bin_models, 1):
            d = open("../"+self.name_save_folder+"/bin"+str(self.bin)+"/"+str(i+1)+"Gauss/"+str(i+1)+"Gauss.bin", "rb")
            m = pickle.load(d)
            f = pickle.load(d)
            d.close()
            table += "{0:3.0f}{1:13.0f}".format(i+1, f.BIC)+"\n"
        return bin+title+table+"\n\n"


    def best(self):
        """Getting best model for considered bin based on the BIC values of the models"""
        d = open("../"+self.name_save_folder+"/bin"+str(self.bin)+"/"+str(1)+"Gauss/"+str(1)+"Gauss.bin", "rb")
        self.m = pickle.load(d)
        self.f = pickle.load(d)
        d.close()
        self.d = "../" + self.name_save_folder + "/bin" + str(self.bin) + "/" + str(1) + "Gauss"
        for i in range(1, self.bin_models, 1):
            d = open("../" + self.name_save_folder+"/bin"+str(self.bin)+"/"+str(i+1)+"Gauss/"+str(i+1)+"Gauss.bin", "rb")
            m = pickle.load(d)
            f = pickle.load(d)
            d.close()
            if self.f.BIC - f.BIC > 2:
                self.f.BIC = f.BIC
                self.d = "../"+self.name_save_folder+"/bin"+str(self.bin)+"/"+str(i+1)+"Gauss"
            else:
                return self.d
        return self.d


    def save(self, filepath1, filepath2):
        """Saving BIC values of the different models and the best model of the considered narrow bin"""
        d = open(filepath1+".txt", "w")
        sys.stdout = d
        print(self)
        d.close()
        sys.stdout = sys.__stdout__
        p = open(filepath1+".bin", "wb")
        pickle.dump(self, p)
        p.close()
        shutil.copytree(self.d, filepath2)


