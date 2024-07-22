import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib as mpl
from scipy.stats import norm
from matplotlib.backend_bases import MouseButton
from tkinter import filedialog
import tkinter as tk
from matplotlib.widgets import Cursor
import time


file_path = filedialog.askopenfilename()

dfOriginal = pd.read_csv(file_path, sep=";")

df = dfOriginal.copy()
df = df[df['y']>0]
fig = plt.figure()
ax1 = fig.subplots()

serie_x = df['x'].to_list()
serie_y  = df['y'].to_list()

plt.scatter(serie_x,serie_y)
ax1.set_yscale('log')
ax1.set_xscale('log')
cursor = Cursor(ax1, horizOn = True, vertOn=True,useblit = True, color = 'red', linewidth = 0.5)

coord= []
i = 0
x_début = 0
background = 0

def onclick(event):
    global i
    global coord
    global df
    global x_début
    global background
    x = event.xdata
    y = event.ydata
    if i == 0:
        coord.append((event.xdata, event.ydata))
        plt.vlines(x, 0, 50, colors='green', linestyles='--')
        print([x,y])
        i+=1
        x_début = x
        fig.canvas.draw()
    elif i == 1:
        plt.hlines(y,0,1, colors='orange', linestyles='--')
        background = y
        i+=1
        
        fig.canvas.draw()


        
        df_début = df.copy()
        df_début['dist_début'] = abs(df_début['x']-x_début)
        df_début = df_début.sort_values(by='dist_début')
        indice_début = df_début.index[0]
        taille = 15
        incr = (df['x'].iloc[-1]-df['x'].iloc[indice_début])/taille
        x_init = df['x'].iloc[indice_début]

        df_mod = df.loc[0:indice_début]
        
        for j in range(taille):
            x = x_init + j * incr
            df2 = pd.DataFrame([[x,background]], columns=['x','y'])
            df_mod = pd.concat([df_mod, df2], ignore_index=True)
            
        plt.cla()
        df_mod = df_mod.loc[1:df_mod.shape[0]]
        serie_x_mod = df_mod['x'].to_list()
        serie_y_mod = df_mod['y'].to_list()
        plt.scatter(serie_x_mod ,serie_y_mod)
        
        ax1.set_yscale('log')
        ax1.set_xscale('log')
        nom = 'Nouveau_fichier_tres_joli'
        with open(nom+'.txt', 'a') as f:
            df_string = df_mod.to_string(header=False, index=False)
            f.write(df_string)
        df_mod.to_csv(nom+'.csv')
        
        plt.legend(['Données'])
fig.canvas.mpl_connect('button_press_event',onclick)


plt.show()

a = zip(*coord)
print(a)