# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:08:28 2023

@author: robotlab
"""

import ActuatorIndependetDynamicController as Acindy
from   ActuatorIndependetDynamicController import AcindyController as ctr_cls
import MathTools
import ServerSocket



class MotionManager:
    def __init__(self):
        self.controllers = dict()
        self.controllers_in_mission = list()

    def setup_socket_server(self):
        HOST = '127.0.0.1'
        PORT = 12300
        self.interface = ServerSocket.Server(HOST, PORT)
        self.interface.start()

    def add_controller_interface(self,controller_ID):
        if (self.controllers.get(controller_ID)):
            return False
        new_controller = Acindy.AcindyController(controller_ID)
        new_controller.set_interface(self.interface)
        new_controller.behavior_type = 2
        self.controllers[controller_ID] = new_controller
        self.controllers_in_mission.append(new_controller)
        return True

    def iterate_mission_controlers(self):
        for controller in self.controllers_in_mission:
            controller.iterate()
        # print(self.controllers_in_mission[0].dt)
        return

    ### posição -180 0 180 destroi as derivadas
    def acc_aproximation_static(self,controller_ID, target_position, maneuver_period): # implementar parametro de intervalo de tempo alvo
        controller:ctr_cls = self.controllers[controller_ID]
        start_pos = controller.sensor_value
        delta_signal, delta_pos = MathTools.min_angle_distance(start_pos, target_position)
        arrive_pos = start_pos + delta_signal*delta_pos
        start_time = controller.sensor_timestamp
        controller.behavior_params = [start_pos, delta_signal, delta_pos, arrive_pos, start_time, maneuver_period]
        controller.behavior_type = 3
        controller.idle = False
        return True

    def velocity_constant(self, controller_ID, target_velocity, maneuver_period):
        controller:ctr_cls = self.controllers[controller_ID]
        end_time = controller.sensor_timestamp + maneuver_period
        controller.behavior_params = [target_velocity, end_time]
        controller.behavior_type = 4
        controller.idle = False
        return










