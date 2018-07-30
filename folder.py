import os, shutil




class Folder():
    def __init__(self, folder = None, i = None, j = None):
        """Initializing name of folder in which relevant data will be saved; i is the bin number,
        j is the number of fit curves"""
        self.folder = folder
        self.i = i
        self.j = j


    def make_folder_run(self):
        """Creating folder for run-phase in fit.py"""
        if not os.path.exists("../" + self.folder):
            os.makedirs("../" + self.folder)
        if not os.path.exists("../" + self.folder + "/bin" + str(self.i)):
            os.makedirs("../" + self.folder + "/bin" + str(self.i))
        if not os.path.exists("../" + self.folder + "/bin" + str(self.i) + "/" + str(self.j) + "Gauss"):
            os.makedirs("../" + self.folder + "/bin" + str(self.i) + "/" + str(self.j) + "Gauss")
        else:
            shutil.rmtree("../" + self.folder + "/bin" + str(self.i) + "/" + str(self.j) + "Gauss")
            os.makedirs("../" + self.folder + "/bin" + str(self.i) + "/" + str(self.j) + "Gauss")


    def make_folder_get_best_model(self):
        """Creating folder for get_best_fit-phase in fit.py"""
        if not os.path.exists("../" + self.folder):
            raise ValueError("No existing data")
        if not os.path.exists("../" + self.folder + "/bin" + str(self.i)):
            raise ValueError("Bin " + str(self.i) + " does not exist")
        if not os.path.exists("../" + self.folder + "/bin" + str(self.i)+"/BIC-Table"):
            os.makedirs("../" + self.folder + "/bin" + str(self.i) +"/BIC-Table")
        else:
            shutil.rmtree("../" + self.folder + "/bin" + str(self.i) +"/BIC-Table")
            os.makedirs("../" + self.folder + "/bin" + str(self.i) + "/BIC-Table")
        if os.path.exists("../" + self.folder + "/bin" + str(self.i) +"/Best_Fit"):
            shutil.rmtree("../" + self.folder + "/bin" + str(self.i) + "/Best_Fit")


    def make_folder_get_bias(self):
        """Creating folder for get_best_fit-phase in fit.py"""
        if not os.path.exists("../" + self.folder):
            raise ValueError("No existing data")
        if not os.path.exists("../" + self.folder + "/Bias"):
            os.makedirs("../" + self.folder + "/Bias")
