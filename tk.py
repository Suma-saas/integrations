from tkinter import *
import os 
import numpy as np
import pandas as pd
import matplotlib                                                                     
matplotlib.use("TKAgg")
matplotlib.use("agg") 
from matplotlib import pyplot as plt
import pickle
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image


class Ploter(Frame):

    def __init__(self, root):

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.graphics = self.dir_path + "/statics/graphics/" 
        self.style = self.dir_path + "/statics/style/"
        self.file_redes = self.dir_path + "/statics/redes/DF_REDES.json"
        self.file_RED_EXTERNA = ""
        self.DF_REDES = pd.read_json(self.file_redes)
        self.DF_EXTERNA = pd.DataFrame({})

        self.master = root
        self.master.protocol('WM_DELETE_WINDOW', self.close_app)
        self.master.title("Sistemas Complejos  -  Jhonatan Garzón")
        self.master.resizable(1,1)

        #Frame RED  -  Image Distro Grafo
        self.frame_RED = Frame(self.master,width = 780, height = 615)
        self.frame_RED.pack()


        #self.imaaaaaaaagen = Image.open(self.graphics+"plot.png")
        self.img_no_plot = ImageTk.PhotoImage(Image.open(self.graphics+"no_imagen.png"))
        self.img_plot = ImageTk.PhotoImage(Image.open(self.graphics+"plot.png"))
          
        self.imgLabel = Label(self.frame_RED)
        self.imgLabel.place(x = 0, y= 0)
        self.imgLabel.configure(image=self.img_plot)


        # Frame mensaje
        self.frame_mensaje = Frame(self.master)
        self.frame_mensaje.pack()
        Label(self.frame_mensaje,text = "Typo of NET:").pack()

        # Frame check
        self.frame_check = Frame(self.master)
        self.frame_check.pack()

        self.red1_1 = IntVar()
        self.red1_1.set(1)
        self.red1_2 = IntVar()
        self.red2_1 = IntVar()
        self.red2_2 = IntVar()
        self.red_ext = IntVar()
        Checkbutton(self.frame_check, text="NET 1 [4038 arcs]", variable=self.red1_1, onvalue=1, offvalue=0, command=self.plotear).pack(side=LEFT)
        Checkbutton(self.frame_check, text="NET 1 [88234 arcs]", variable=self.red1_2, onvalue=1, offvalue=0, command=self.plotear).pack(side=LEFT)
        Checkbutton(self.frame_check, text="NET 2 [4038 arcs]", variable=self.red2_1, onvalue=1, offvalue=0, command=self.plotear).pack(side=LEFT)
        Checkbutton(self.frame_check, text="NET 2 [88234 arcs]", variable=self.red2_2, onvalue=1, offvalue=0, command=self.plotear).pack(side=LEFT)
        Checkbutton(self.frame_check, text="EXT NET", variable=self.red_ext, onvalue=1, offvalue=0, command=self.plotear).pack(side=LEFT)

        # Frame mensaje
        self.frame_mensaje2 = Frame(self.master)
        self.frame_mensaje2.pack()
        Label(self.frame_mensaje2,text = "").pack()
        Label(self.frame_mensaje2,text = "Typo of Plot:").pack()

        # Frame check
        self.frame_radio = Frame(self.master)
        self.frame_radio.pack()
        self.plot = IntVar()
        self.plot.set(1)
        Radiobutton(self.frame_radio, text="Hist", variable=self.plot, value = 1, command=self.plotear).pack(side=LEFT)
        Radiobutton(self.frame_radio, text="Plot", variable=self.plot, value=2, command=self.plotear).pack(side=LEFT)
        Radiobutton(self.frame_radio, text="Scatter", variable=self.plot, value=3, command=self.plotear).pack(side=LEFT)

        # Frame mensaje
        self.frame_mensaje2 = Frame(self.master)
        self.frame_mensaje2.pack()
        Label(self.frame_mensaje2).pack()
        self.text = StringVar()
        self.text.set("Select Outside NET´s File (.xlsx)")
        Label(self.frame_mensaje2, textvariable = self.text).pack()

        # Frame Controladores
        self.frame_widgets2 = Frame(self.master,width = 779)
        self.frame_widgets2.pack()
        Button(self.frame_widgets2, text = "LOAD" ,width = 20 , command=self.seleccionar_archivo ).pack(side=LEFT)
        Button(self.frame_widgets2, text = "CLEAN" ,width = 20 , command=self.borrar_selección ).pack(side=LEFT)
        self.plotear()

    def plotear(self):
        self.lista_binaria = []
        self.lista_binaria.append(self.red1_1.get()==1)
        self.lista_binaria.append(self.red1_2.get()==1)
        self.lista_binaria.append(self.red2_1.get()==1)
        self.lista_binaria.append(self.red2_2.get()==1)
        self.lista_binaria.append(self.red_ext.get()==1)

        plt.figure(figsize=(8,5))
        if sum(self.lista_binaria) == 0:
            print("Ploteando NADAA...")
            self.imgLabel.configure(image=self.img_no_plot)
            self.imgLabel.image=self.img_no_plot
        else:
            if self.plot.get() == 1:
                self._hist()
            elif self.plot.get() == 2:
                self._plot()
            else:
                self._scatter()   
            plt.legend(loc='upper right')
            plt.savefig(self.graphics+"plot.png")
            plt.close('all')
            self.img_plot = ImageTk.PhotoImage(Image.open(self.graphics+"plot.png"))
            self.imgLabel.configure(image=self.img_plot)
            self.imgLabel.image=self.img_plot
        

    def _hist(self):
        if self.lista_binaria[0]:
            plt.hist(self.DF_REDES["RED1_A"], alpha=0.5, label='RED 1 (4038 Arcos)',color = "b")
        if self.lista_binaria[1]:
            plt.hist(self.DF_REDES["RED1_B"], alpha=0.5, label='RED 1 (88324 Arcos)',color = "r")
        if self.lista_binaria[2]:
            plt.hist(self.DF_REDES["RED2_A"], alpha=0.5, label='RED 2 (4038 Arcos)',color = "g")
        if self.lista_binaria[3]:
            plt.hist(self.DF_REDES["RED2_B"], alpha=0.5, label='RED 2 (88324 Arcos)',color = "c")
        if self.lista_binaria[4] and len(self.DF_EXTERNA):
            try:
                plt.hist(self.DF_EXTERNA.iloc[:,1], alpha=0.5, label='RED Externa',color = "y")
            except:
                pass

    def _plot(self):
        if self.lista_binaria[0]:
            plt.plot(self.DF_REDES["RED1_A"], alpha=0.5, label='RED 1 (4038 Arcos)',color = "b")
        if self.lista_binaria[1]:
            plt.plot(self.DF_REDES["RED1_B"], alpha=0.5, label='RED 1 (88324 Arcos)',color = "r")
        if self.lista_binaria[2]:
            plt.plot(self.DF_REDES["RED2_A"], alpha=0.5, label='RED 2 (4038 Arcos)',color = "g")
        if self.lista_binaria[3]:
            plt.plot(self.DF_REDES["RED2_B"], alpha=0.5, label='RED 2 (88324 Arcos)',color = "c")
        if self.lista_binaria[4] and len(self.DF_EXTERNA):
            try:
                plt.plot(self.DF_EXTERNA.iloc[:,1], alpha=0.5, label='RED Externa',color = "y")
            except:
                pass
        
    def _scatter(self):
        if self.lista_binaria[0]:
            plt.scatter(self.DF_REDES.index,self.DF_REDES["RED1_A"], alpha=0.5, label='RED 1 (4038 Arcos)',color = "b")
        if self.lista_binaria[1]:
            plt.scatter(self.DF_REDES.index,self.DF_REDES["RED1_B"], alpha=0.5, label='RED 1 (88324 Arcos)',color = "r")
        if self.lista_binaria[2]:
            plt.scatter(self.DF_REDES.index,self.DF_REDES["RED2_A"], alpha=0.5, label='RED 2 (4038 Arcos)',color = "g")
        if self.lista_binaria[3]:
            plt.scatter(self.DF_REDES.index,self.DF_REDES["RED2_B"], alpha=0.5, label='RED 2 (88324 Arcos)',color = "c")
        if self.lista_binaria[4] and len(self.DF_EXTERNA):
            try:
                plt.scatter(self.DF_EXTERNA.index,self.DF_EXTERNA.iloc[:,1], alpha=0.5, label='RED Externa',color = "y")
            except:
                pass


    def seleccionar_archivo(self):
        self.file_RED_EXTERNA = filedialog.askopenfilename(initialdir = "/",
            title = "Select file",
            filetypes = (("Exel files","*.xlsx"),("all files","*.*")))
        self.text.set("Dirección :" + self.file_RED_EXTERNA)
        try:
            self.DF_EXTERNA = pd.read_excel(self.file_RED_EXTERNA)
        except:
            self.text.set("Error en el archivo :" + self.file_RED_EXTERNA + " !")
            self.DF_EXTERNA = pd.DataFrame({})

        self.plotear()

    def borrar_selección(self):
        self.file_RED_EXTERNA = ""
        self.text.set("Select Outside NET´s File (.xlsx)")
        self.DF_EXTERNA = pd.DataFrame({})
        self.plotear()

    # LOOP
    def close_app(self):
        self.master.quit()
        self.master.destroy()
        

# ------------------------- INTERFAZ ---------------------------
root = Tk()
ploteador = Ploter(root)
root.mainloop()
ploteador = None
root = None
        


