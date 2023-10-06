# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:08:28 2023

@author: robotlab
"""

from array import array
import ActuatorIndependetDynamicController as Acindy
from   ActuatorIndependetDynamicController import AcindyController as ctr_cls
import MathTools
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(parent_dir)
from UnrealEngine_Python_Socket import ServerSocket



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

import time
mm = MotionManager()
mm.setup_socket_server()
steering = [10,11,12,13]
wheels   = [14,15,16,17]
for controller_id in steering:
    mm.add_controller_interface(controller_id)
    controller = mm.controllers[controller_id]
for controller_id in wheels:
    mm.add_controller_interface(controller_id)
    controller = mm.controllers[controller_id]

def test_position_approach(i, pos, period):
    controller = mm.controllers[i]
    controller.get_inital_condition()
    mm.acc_aproximation_static(i, pos, period)
    aproximation_iteration(period)

def aproximation_iteration(time_limit):
    keep_loop = True
    start_loop_time = time.time()
    while keep_loop:
        delta_time = time.time() - start_loop_time
        if (delta_time > time_limit + 0.5):
            keep_loop = False
        mm.iterate_mission_controlers()
    print("finished")

def test_heading(pos,period):
    for i in steering[0:2]:
        controller = mm.controllers[i]
        controller.get_inital_condition()
        mm.acc_aproximation_static(i, pos, period)
    aproximation_iteration(period)

def test_roll(velocity,period):
    for i in wheels:
        controller = mm.controllers[i]
        controller.get_inital_condition()
        mm.velocity_constant(i, velocity, period)
    aproximation_iteration(period)

def test_bike(point_on_axis, period_s = 1, roll=False, angular_vel = 0, period_r = 1):
    angle1_degrees, angle2_degrees , signs , factors = MathTools.bikemode_params(point_on_axis, 1)
    for i in steering:
        controller = mm.controllers[i]
        controller.get_inital_condition()
    mm.acc_aproximation_static(10, angle1_degrees, period_s)
    mm.acc_aproximation_static(11, angle2_degrees, period_s)
    mm.acc_aproximation_static(12, 0, period_s)
    mm.acc_aproximation_static(13, 0, period_s)
    aproximation_iteration(period_s)
    if (roll):
        for i in range(4):
            wheel_id = wheels[i]
            sign = signs[i]
            factor = factors[i]
            velocity = angular_vel*factor*sign
            # print(sign)
            print(velocity)
            controller = mm.controllers[wheel_id]
            controller.get_inital_condition()
            mm.velocity_constant(wheel_id, velocity, period_r)
        aproximation_iteration(period_r)












