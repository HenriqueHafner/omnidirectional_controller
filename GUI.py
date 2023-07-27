# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 17:41:31 2022

@author: robotlab
"""

import matplotlib.pyplot as plt
import numpy as np
import time


# Separar entre "matplotlib handler" , "data processing" e "simulation" as rotinas e objetos neste código.
def construc_GUI():
    features_list = []
    features_list.append(Feature_Lines())
    graphical_interface = GUI()
    graphical_interface.setup_features(features_list)
    return graphical_interface

class GUI:
    def __init__(self):
        plt.ion()
        self.fig = plt.figure(figsize=(7.0,7.0))
        self.fig
        ax = self.fig.add_subplot(111)
        self.axes_list = [ax]
        self.axes_list[0].set_xticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
        self.axes_list[0].set_yticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
        self.axes_list[0].set_xlim(-5,5)
        self.axes_list[0].set_ylim(-5,5)
        self.axes_list[0].grid(visible=True , ls='--', lw=0.4)
        self.fig.show()
    
    def setup_features(self, features_list):
        self.features = features_list
        # Lines
        lines_feature = self.features[0]
        lines_feature.set_axes(self.axes_list)
        lines_feature.create_lines()        
        #
    
    def update_features(self):
        # Lines
        lines_feature = self.features[0]
        lines_feature.update()
    
    def gui_frontend(self):
        time_a = time.time()
        self.update_features()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.02)
        plt.show()
        print(time.time() - time_a)
    
    def GUI_loop(self):
        try:
            self.gui_frontend()
        except:
            print("Gui failed. frontend thread finished.")

class Feature_Lines:
    def __init__(self):
        self.angles_data = [0,0,0,0]
        None
    
    def line_c_create_data(self, length=1.0, x=0.0, y=0.0, angle=0.0):
        x_len = (length)*np.cos(angle)
        y_len = (length)*np.sin(angle)
        x_start = x - x_len/2
        y_start = y - y_len/2
        x_end =   x + x_len/2
        y_end =   y + y_len/2
        line_x_data  = np.array([x_start, x_end])
        line_y_data  = np.array([y_start, y_end])
        line_data = [line_x_data, line_y_data]
        return line_data

    def line_s_create_data(self, length=1.0, x=0.0, y=0.0, angle=0.0):
        x_len = (length)*np.cos(angle)
        y_len = (length)*np.sin(angle)
        x_start = x
        y_start = y
        x_end =   x + x_len
        y_end =   y + y_len
        line_x_data  = np.array([x_start, x_end])
        line_y_data  = np.array([y_start, y_end])
        line_data = [line_x_data, line_y_data]
        return line_data
    
    def set_axes(self, axes_list):
        self.axes = axes_list

    def create_lines(self):
        self.lines = [0,0,0,0]
        self.lines_data = [0,0,0,0]
        self.lines_data[0] = self.line_s_create_data(length=1.0, x= +1.0, y= +1.0, angle=self.angles_data[0])
        self.lines_data[1] = self.line_s_create_data(length=1.0, x= +1.0, y= -1.0, angle=self.angles_data[1])
        self.lines_data[2] = self.line_s_create_data(length=1.0, x= -1.0, y= -1.0, angle=self.angles_data[2])
        self.lines_data[3] = self.line_s_create_data(length=1.0, x= -1.0, y= +1.0, angle=self.angles_data[3])
        index = 0
        for self.line_data in self.lines_data:
            self.lines[index] = self.axes[0].plot(self.line_data[0], self.line_data[1])[0]
            index += 1

    def line_update_data(self, line, data):
        line.set_xdata(data[0])
        line.set_ydata(data[1])
        
    def update(self):
        self.lines_data[0] = self.line_s_create_data(length=1.0, x= +1.0, y= +1.0, angle=self.angles_data[0])
        self.lines_data[1] = self.line_s_create_data(length=1.0, x= +1.0, y= -1.0, angle=self.angles_data[1])
        self.lines_data[2] = self.line_s_create_data(length=1.0, x= -1.0, y= -1.0, angle=self.angles_data[2])
        self.lines_data[3] = self.line_s_create_data(length=1.0, x= -1.0, y= +1.0, angle=self.angles_data[3])
        self.line_update_data(self.lines[0], self.lines_data[0])
        self.line_update_data(self.lines[1], self.lines_data[1])
        self.line_update_data(self.lines[2], self.lines_data[2])
        self.line_update_data(self.lines[3], self.lines_data[3])
        return True
    
    def set_angle_data(self, angles_data_input):
        self.angles_data = angles_data_input
        return True

