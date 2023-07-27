# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:06:51 2023

@author: robotlab
"""
import ActuatorIndependetDynamicController
import ActuadorDataVisualization as adv
import numpy as np
import time

AcindyController = ActuatorIndependetDynamicController.AcindyController

class tester:
    def __init__(self):
        self.acind = AcindyController()
    
    def setup_visualizer(self):
        self.GUI = adv.GUI()
        gui = self.GUI
        self.plot_titles = ["time","position","velocity","acceler.","jerk","Jounce","Force"]
        lines = 1
        colums = 1
        plots = 1
        gui.setup_dashboard(lines, colums, plots)
    
    def simulate_position_advancing(self, dt):
        acind = self.acind
        state_vector = acind.state_data[acind.most_recent_data_index] # state vector is : Position, Velocity, Acceleration, Jerk, jounce
        p0 = state_vector[0]
        v0 = state_vector[1]
        a  = acind.outputforce
        position = p0 + v0 * dt + (0.5) * a * dt*dt
        timestamp = acind.sensor_last_timestamp + dt
        acind.get_sensor_data(position, timestamp)

    def simulate_force_applied(self):
        acind = self.acind
        acind.outputforce = 0.1
        for i in range(40):
            testing_obj.simulate_position_advancing(0.1)
            acind.state_update()
            timestamp = acind.sensor_last_timestamp
            print("Timestamp: ", timestamp)
            testing_obj.acind.print_variables()
            time.sleep(0.02)

    def simulate_jerk_control(self):   
        acind = self.acind
        acind.jerk_goal = 0.05
        for i in range(20):
            acind.jerk_control()
            testing_obj.simulate_position_advancing(0.1)
            acind.state_update()
            timestamp = acind.sensor_last_timestamp
            print("Timestamp: ", timestamp)
            testing_obj.acind.print_variables()
            time.sleep(0.02)



testing_obj = tester()
# testing_obj.simulate_force_applied()
testing_obj.simulate_jerk_control()
# acceleração está dando metade da força