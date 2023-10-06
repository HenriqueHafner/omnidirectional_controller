# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:08:28 2023

@author: robotlab
"""

import MotionManager
import time
mm = MotionManager.MotionManager()
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
    angle1_degrees, angle2_degrees , signs , factors = MotionManager.MathTools.bikemode_params(point_on_axis, 1)
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












