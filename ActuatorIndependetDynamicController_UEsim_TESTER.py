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

tester = UESimulation_tester()
tester.setup_socket_server()
