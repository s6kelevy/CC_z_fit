import os, shutil




class Folder():
    def __init__(self, folder = None, i = None, j = None):
        self.folder = folder
        self.i = i
        self.j = j


    def make_folder_run(self):
        if not os.path.exists("../" + self.folder):
            os.makedirs("../" + self.folder)
        if not os.path.exists("../" + self.folder + "/bin" + str(self.i+1)):
            os.makedirs("../" + self.folder + "/bin" + str(self.i+1))
        if not os.path.exists("../" + self.folder + "/bin" + str(self.i+1) + "/" + str(self.j + 1) + "Gauss"):
            os.makedirs("../" + self.folder + "/bin" + str(self.i+1) + "/" + str(self.j+1) + "Gauss")
        else:
            shutil.rmtree("../" + self.folder + "/bin" + str(self.i+1) + "/" + str(self.j+1) + "Gauss")
            os.makedirs("../" + self.folder + "/bin" + str(self.i+1) + "/" + str(self.j+1) + "Gauss")


    def make_folder_get_best_fit(self):
        if not os.path.exists("../" + self.folder):
            raise ValueError("Can't get best fit")
        if not os.path.exists("../" + self.folder + "/bin" + str(self.i+1)):
            raise ValueError("Data-Set " + str(self.i+1) + " does not exist")
        if not os.path.exists("../" + self.folder + "/bin" + str(self.i+1) + "/BIC-Table"):
            os.makedirs("../" + self.folder + "/bin" + str(self.i+1) + "/BIC-Table")
        else:
            shutil.rmtree("../" + self.folder + "/bin" + str(self.i+1) + "/BIC-Table")
            os.makedirs("../" + self.folder + "/bin" + str(self.i+1) + "/BIC-Table")
        if not os.path.exists("../" + self.folder + "/bin" + str(self.i+1) + "/Best_Fit"):
            os.makedirs("../" + self.folder + "/bin" + str(self.i+1) + "/Best_Fit")
        else:
            shutil.rmtree("../" + self.folder + "/bin" + str(self.i+1) + "/Best_Fit")
            os.makedirs("../" + self.folder + "/bin" + str(self.i+1) + "/Best_Fit")


    def make_folder_get_bias(self):
        if not os.path.exists("../" + self.folder):
            raise ValueError("Can't get bias")
        if not os.path.exists("../" + self.folder + "/Bias"):
            os.makedirs("../" + self.folder + "/Bias")
      #  else:
       #     shutil.rmtree("../" + self.folder + "/Bias")
        #    os.makedirs("../" + self.folder + "/Bias")