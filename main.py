# -*- coding: utf-8 -*-
"""
@author: Jonathan Browning
"""
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import time
from Class.rice import Rice
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
from tkinter import messagebox

def draw_envelope(canvas, data):
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.figure(1)
    plt.xlabel(r"$r$", fontsize=18)
    plt.ylabel(r"$f_{R}(r)$", fontsize=18)
    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18) 
    plt.xlim((0, 6))
    plt.ylim(bottom=0)
    plt.grid(True)
    plt.tick_params(direction='in')
    plt.plot(data.r, data.envelopeProbability, "k", label='Theoretical')  
    plt.plot(data.xdataEnv[1:len(data.xdataEnv):2], data.ydataEnv[1:len(data.ydataEnv):2], "k.", label='Simulation') 
    leg = plt.legend(fontsize=15)
    leg.get_frame().set_edgecolor('k')
    fig = plt.gcf()
    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    plt.close(1)
    return figure_canvas_agg

def draw_phase(canvas, s):
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.figure(1)
    plt.xlabel(r'$\theta$', fontsize=18)
    plt.ylabel(r'$f_{\Theta}(\theta)$', fontsize=18)
    plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
               [r'$-\pi$',r'$-\pi/2$',r'$0$',r'$\pi/2$',r'$\pi$'],
               fontsize = 18)
    plt.yticks(fontsize = 18) 
    plt.xlim((-np.pi, np.pi))
    plt.ylim(bottom=0)
    plt.grid(True)
    plt.tick_params(direction='in')    
    plt.plot(s.theta, s.phaseProbability, "k", label='Theoretical')  
    plt.plot(s.xdataPh[1:len(s.xdataPh):2], s.ydataPh[1:len(s.ydataPh):2], "k.", label='Simulation')  
    leg = plt.legend(fontsize=15)
    leg.get_frame().set_edgecolor('k')
    fig = plt.gcf()
    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    plt.close(1)
    return figure_canvas_agg

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')
    
def main():   
        
    # Setting up window layout
    layout = [[sg.Text(r'Please enter K, \hat{r}^2 and \phi', font='Helvetica 18')],      
          [sg.Text("K:", size=(8, 1), font='Helvetica 18'), sg.Input(key='-K', size=(5, 1), font='Helvetica 18')],      
          [sg.Text(r"\hat{r}^2:", size=(8, 1), font='Helvetica 18'), sg.Input(key=r'-\hat{r}^2', size=(5, 1), font='Helvetica 18')],      
          [sg.Text("\phi:", size=(8, 1), font='Helvetica 18'), sg.Input(key=r'-\phi', size=(5, 1), font='Helvetica 18')],      
          [sg.Button('Calculate', font='Helvetica 18'), sg.Exit(font='Helvetica 18')],
          [sg.Text("Time (s):", size=(8, 1), font='Helvetica 18'), sg.Txt('', size=(8,1), key='output')],
          [sg.Canvas(key='-CANVAS1')],
          [sg.Canvas(key='-CANVAS2')],]
        
    window = sg.Window("The Rician fading model", layout, finalize=True, font='Helvetica 18')

    # The Event Loop                 
    while True:
        # Reading user inputs
        event, values = window.read() 
        
        # Close if the exist button is pressed or the X
        if event in (sg.WIN_CLOSED, 'Exit'):
            break      
        
        # check for previous figures and delete them
        if 'fig_canvas_agg1' in locals():
           delete_figure_agg(fig_canvas_agg1)
        
        if 'fig_canvas_agg2' in locals():
           delete_figure_agg(fig_canvas_agg2)
        
        # Rice class instance which calculates everything and time the exeuction
        start = time.time()
        try:
            s = Rice(values['-K'], values['-\hat{r}^2'], values['-\phi'])
        except Exception as e:  # displays the error message and will force the program to close
            messagebox.showerror("Error", e)
            continue
        end = time.time()
        
        # update the execution time
        exeTime = round(end - start, 4) # Roudn to 4 decimal places
        window['output'].update(exeTime)  # Display the execution time 
        
        # drawing the figures
        fig_canvas_agg1 = draw_envelope(window['-CANVAS1'].TKCanvas, s)
        fig_canvas_agg2 = draw_phase(window['-CANVAS2'].TKCanvas, s)
        
    window.close()
    
if __name__ == "__main__":
    main()