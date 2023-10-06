# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:06:51 2023

@author: robotlab
"""
import ActuatorIndependetDynamicController
import ActuadorDataVisualization as adv
import numpy as np
import time
import matplotlib.pyplot as plt

AcindyController = ActuatorIndependetDynamicController.AcindyController

import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(parent_dir)
from UnrealEngine_Python_Socket import ServerSocket

class UESimulation_tester:
    def __init__(self):
        self.acind = AcindyController(10)
        self.data = []
        self.state_log = []
        self.time_log = []
    
    def setup_socket_server(self):
        HOST = '127.0.0.1'
        PORT = 12300
        self.interface = ServerSocket.Server(HOST, PORT)
        self.interface.start()
        self.acind.set_interface(self.interface)
        
    def sensor_getdata(self):
        self.acind.loop_routine_iteration()
    
    def log_state(self):
        state = self.acind.state_data[self.acind.most_recent_data_index]
        timestamp = self.acind.sensor_last_timestamp
        self.state_log.append(np.copy(state))
        self.time_log.append(timestamp)
        # self.acind.print_variables()

    def plot_states_timeline(self):
        time_log = np.array(self.time_log)
        state_log = np.array(self.state_log)
        for i in range(len(state_log[0])-1):
            y = state_log[:, i]
            x = time_log
            plt.plot(x, y, label = str(i))
        plt.legend()

class PythonSimulation_tester:
    def __init__(self):
        self.acind = AcindyController()
        self.data = []
        self.state_log = []
        self.time_log = []
    
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
        a  = 2*acind.outputforce
        position = p0 + v0 * dt + (0.5) * a * dt*dt
        timestamp = acind.sensor_last_timestamp + dt
        acind.get_sensor_data(position, timestamp)

    def simulate_force_applied(self, force):
        acind = self.acind
        acind.outputforce = force
        for i in range(1000):
            self.simulate_position_advancing(0.1)
            acind.state_update()
            self.log_state()

    def simulate_jerk_control(self, jerk, sensor_period):   
        acind = self.acind
        acind.jerk_goal = jerk
        for i in range(int(time/sensor_period)):
            acind.jerk_control()
            self.simulate_position_advancing(sensor_period)
            acind.state_update()
            self.log_state()
        self.acind.print_variables()

    def simulate_position_control(self, dposition, dtime):
        acind = self.acind
        acind.position_control_setup(dposition, dtime)
        for i in range(40):
            acind.position_control()
            self.simulate_position_advancing(0.1)
            acind.state_update()
            self.log_state()

    def log_state(self):
        state = self.acind.state_data[self.acind.most_recent_data_index]
        timestamp = self.acind.sensor_last_timestamp
        self.state_log.append(np.copy(state))
        self.time_log.append(timestamp)
        # self.acind.print_variables()

    def plot_states_timeline(self):
        time_log = np.array(self.time_log)
        state_log = np.array(self.state_log)
        for i in range(len(state_log[0])-1):
            y = state_log[:, i]
            x = time_log
            plt.plot(x, y, label = str(i))
        # y = 0.5*time_log*time_log*0.2
        # x = time_log
        # plt.plot(x, y, label = 'default')
        plt.legend()

def attributes_without_underscore(obj):
    attributes = {attr: value for attr, value in obj.__dict__.items() if not attr.startswith('_')}
    return attributes

tester = UESimulation_tester()
tester.setup_socket_server()
