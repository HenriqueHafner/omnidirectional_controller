# -*- coding: utf-8 -*-
from ActuadorDataVisualization import GUI
import numpy as np
import time
import math

class tester:
    def testing_multiplot():
        lines = 2
        colums = 2
        plots = 4
        plot_titles = ["title"]*plots
        gui = GUI()
        gui.setup_dashboard(lines, colums, plots)
        gui.draw_gui()
        gui.spawn_window()
        x_data=0
        y_data=0
        data = [[],[]]
        for i in range(5):
            x_data = 3.14*2*i/50
            y_data = math.sin(x_data)
            data[0].append(x_data)
            data[1].append(y_data)
        big_data = [data]*(plots-1)
        x = 3.14*2*(1/1000)
        y = math.sin(x)
        big_data.append([np.array([x]),np.array([y])])
        gui.setup_plots(big_data, plot_titles)
        gui.update_plots(big_data)
        gui.draw_gui()
        gui.plot_window.fig.canvas.flush_events()
        x=0
        iterations = 1000
        for i in range(iterations):
            x += 3.14*2*(1/(4*iterations))
            y = math.sin(x)
            big_data[-1][0] = np.array([x])
            big_data[-1][1] = np.array([y])
            gui.update_plots(big_data)
            gui.draw_gui()

    def testing_framerate():
        lines = 1
        colums = 1
        plots = 1
        plot_titles = ["title"]*plots
        gui = GUI()
        gui.setup_dashboard(lines, colums, plots)
        gui.draw_gui()
        gui.spawn_window()
        # define data
        x = 3.14*2*(1/1000)
        y = math.sin(x)
        big_data = [ [np.array([x]),np.array([y])] ]
        gui.setup_plots(big_data, plot_titles)
        gui.update_plots(big_data)
        gui.draw_gui()
        x=0
        iterations = 100
        for i in range(iterations):
            x += 3.14*2*(1/200)
            y = math.sin(x)
            big_data[-1][0] = np.array([x])
            big_data[-1][1] = np.array([y])
            time_a = time.time()
            gui.update_plots(big_data)
            gui.draw_gui()
            print(time.time() - time_a)

tester.testing_framerate()