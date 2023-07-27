# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 17:41:31 2022

@author: robotlab
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.style as mplstyle
import numpy as np


class PlotWindow:
    def __init__(self):
        plt.ioff()
        plt.rcParams['font.size'] = 7
        mplstyle.use('fast')
        self.fig = plt.figure(figsize=(7.0,7.0))
        self.axes = []
    
        
    def create_axes(self, line_n, col_n, plot_qtt):
        if col_n * line_n < plot_qtt:
            raise ValueError("Invalid input of lines, colums, plots")
        axes_l = []
        for i in range(1, plot_qtt + 1):
            axes_l.append(self.fig.add_subplot(line_n, col_n, i))
        self.axes = axes_l

        
    def define_plot(self, axis_index, data, plot_label):
        axis = self.axes[axis_index]
        axis.grid(visible=True , ls='--', lw=0.4)
        axis.set_title(plot_label)
        self.adjust_axis(axis, data)
        line = Line2D(data[0],data[1], marker='o')
        # line.set_animated(True)
        axis.add_line(line)
        
    def adjust_axis(self, axis, data):
        for i in [0,1]:
            min_value = float( min(data[i]) )
            max_value = float( max(data[i]) )
            interval = abs(max_value-min_value)
            if (interval < 0.002):
                interval = 0.002
                min_value = (min_value+max_value)/2 - interval/2
                max_value = (min_value+max_value)/2 + interval/2
            low_lim = min_value - interval/20
            hig_lim = max_value + interval/20
            ticks = np.linspace(min_value,max_value,20+1)
            if   (i == 0):
                axis.set_xlim(low_lim,hig_lim)
                axis.set_xticks(ticks)
            elif (i == 1):
                axis.set_ylim(low_lim,hig_lim)
                axis.set_yticks(ticks)

    def update_plot(self, axis_index, data):
        i = axis_index
        axis = self.axes[i]
        line = axis.get_lines()[0]
        line.set_xdata(data[0])
        line.set_ydata(data[1])
        self.adjust_axis(axis, data)
        # self.fig.draw_artist(axis.patch)
        # self.fig.draw_artist(axis)
        # self.fig.draw_artist(line)

    def draw_gui(self):
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def spawn_window(self):
        self.fig.show()
    
    def PlotWindowLoop(self):
        try:
            self.draw_gui()
        except:
            print("Gui failed. frontend thread finished.")
        plt.pause(0.02)

class GUI:

    def __init__(self):
        self.plot_window = PlotWindow()
        self.buffed_data_container = {}
        self.buffed_data_size = 30

    def setup_dashboard(self, lines, colums, plots):
        self.plots_number = plots
        self.plot_window.create_axes(lines, colums, plots)

    def setup_plots(self, big_data, plot_titles):
        for i in range(len(big_data)):
            data = big_data[i]
            title = plot_titles[i]
            if len(data[0]) > 1: # data is a vector of [x,y]
                self.plot_window.define_plot(i, data, title)
            else: # data is a single [x,y] entry, then log and show as timeline.
                bs = self.buffed_data_size
                self.buffed_data_container[i] = [np.array([data[0][0]]*bs), np.array([data[1][0]]*bs)]
                buffed_data = self.buffed_data_container[i]
                self.plot_window.define_plot(i, buffed_data, title)

    def update_plots(self, big_data):
        for i in range(len(big_data)):
            data = big_data[i]
            if not (self.buffed_data_container.get(i)):
                self.plot_window.update_plot(i, data)
            else:
                buffed_data = self.buffed_data_container[i]
                buffed_data[0] = np.roll(buffed_data[0], -1)
                buffed_data[1] = np.roll(buffed_data[1], -1)
                buffed_data[0][-1] = data[0][0]
                buffed_data[1][-1] = data[1][0]
                self.plot_window.update_plot(i, buffed_data)
       
    def draw_gui(self):
        self.plot_window.draw_gui()
    
    def spawn_window(self):
        self.plot_window.spawn_window()












