# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 14:02:48 2023

@author: Henrique Hafner Ferreira
"""

from array import array
import time
import sys

class AcindyController:
    def __init__(self, ID):
        self.ID = ID
        self.print_debug = True
        self.PosCon = None
        # operational state
        self.state_code = 0
        self.idle = 0
        self.request_number = 0
        self.behavior_params = []
        self.behavior_type = 0
        # constant parameters
        self.max_acc = float('Nan')
        self.max_vel = float('Nan')
        self.ta = 0
        self.max_pa = 0 # total displacement in manuever from 0 to maximum velocity, done with maximum aceleration.
        # Sensor
        self.sensor_timestamp = 0.2
        self.sensor_last_timestamp = 0.1
        self.sensor_value = 0.0
        self.sensor_last_value = 0.0
        self.dt = 0.1
        # state vector is : Position, Velocity, Acceleration, Jerk, jounce
        self.state_data_a    = array('f', [0.0] * 5)
        self.state_data_b    = array('f', [0.0] * 5)
        self.state_data = [self.state_data_a, self.state_data_b]
        self.most_recent_data_index = 0
        self.last_recent_data_index = 1

    def iterate(self):
        target_residue = None
        if (self.behavior_type == 2):
            self.behave_type2()
        if (self.behavior_type == 3):
            target_residue = self.behave_type3()
        if (self.behavior_type == 4):
            self.behave_type4()
        return target_residue

    def behave_type2(self):
        self.get_sensor_data()
        self.state_update()

    def behave_type3(self):
        # order 3 aproximation
        # [start_pos, delta_signal, delta_pos, arrive_pos, start_time, maneuver_period]
        arrive_pos = self.behavior_params[3]
        target_residue = abs(arrive_pos-self.sensor_last_value)
        if (target_residue <= 1):
            target_pos = arrive_pos
        else:
            start_pos = self.behavior_params[0]
            signal = self.behavior_params[1]
            ds = self.behavior_params[2]
            ct = self.sensor_timestamp - self.behavior_params[4]
            tt = self.behavior_params[5]
            t = ct/tt
            t = max(0.0,t)
            t = min(t,1.0 )
            t2 = t*t
            t3 = t2*t
            factor = ( -2*t3 + 3*t2 )
            if (factor>1):
                factor = 1
            elif (factor<0):
                factor = 0
            target_pos = start_pos + ds*factor*signal
        timestamp, value = self.interface.send_type_5_message(self.ID , target_pos)
        self._set_sensor_data(timestamp, value)
        self.state_update()
        return target_residue
        
    def behave_type4(self):
        until_time =  self.behavior_params[1]
        curr_time = self.sensor_timestamp
        if (curr_time >= until_time):
            velocity_target = 0
            self.behavior_type = 2
        else:
            velocity_target =  self.behavior_params[0]
        timestamp, value = self.interface.send_type_6_message(self.ID , velocity_target)
        self._set_sensor_data(timestamp, value)
        self.state_update()

    def get_sensor_data(self):
        # get actual data
        timestamp, value = self.interface.send_type_2_message(self.ID)
        # Sensor properties atualization
        self.sensor_last_timestamp = self.sensor_timestamp
        self.sensor_last_value = self.sensor_value
        self.sensor_timestamp = timestamp
        self.sensor_value = value
        self.dt = self.sensor_timestamp - self.sensor_last_timestamp
        return True

    def _set_sensor_data(self, timestamp, sensor_value):
        # Sensor properties atualization
        self.sensor_last_timestamp = self.sensor_timestamp
        self.sensor_last_value = self.sensor_value
        self.sensor_timestamp = timestamp
        self.sensor_value = sensor_value
        self.dt = timestamp - self.sensor_last_timestamp

    def cronological_data_index_roll(self):
        if (self.most_recent_data_index == 0):
            self.most_recent_data_index = 1
            self.last_recent_data_index = 0
        else:
            self.most_recent_data_index = 0
            self.last_recent_data_index = 1

    def state_update(self):
        self.cronological_data_index_roll()       
        dt = self.dt
        i_l = self.last_recent_data_index
        i_m = self.most_recent_data_index
        self.state_data[i_m][0] = self.sensor_value*1.0 # set position
        self.state_data[i_m][1] = ( self.state_data[i_m][0] - self.state_data[i_l][0] ) / dt # set velocity
        self.state_data[i_m][2] = ( self.state_data[i_m][1] - self.state_data[i_l][1] ) / dt # set acceleration
        self.state_data[i_m][3] = ( self.state_data[i_m][2] - self.state_data[i_l][2] ) / dt # set jerk
        self.state_data[i_m][4] = ( self.state_data[i_m][3] - self.state_data[i_l][3] ) / dt # set jounce
        # self.print_variables()

    def state_get_vector(self):
        return self.state_data[self.most_recent_data_index]

    def get_inital_condition(self):
        self.state_data_a    = array('f', [0.0] * 5)
        self.state_data_b    = array('f', [0.0] * 5)
        self.state_data = [self.state_data_a, self.state_data_b]
        self.get_sensor_data()
        self.get_sensor_data()
        self.state_data[0][0] = self.sensor_value
        self.state_data[1][0] = self.sensor_value
        for i in range(10):
            self.get_sensor_data()
            self.state_update()

    def print_variables(self):
        array_to_print = self.state_data[self.most_recent_data_index]
        line_to_print = self.float_format(self.sensor_last_timestamp) + ' '
        for value in array_to_print:
            line_to_print += self.float_format(value) + ' '
        print(line_to_print)
            
    def float_format(self, number):
        formatted_number = "{:+.5f}".format(number)
        return formatted_number

    def set_interface(self, interface_instance):
        self.interface = interface_instance

    class PID_Component:
        def __init__(self, name, controller):
            self.name = name
            self.controller = controller
            self.Initialize_variable_values()

        def Initialize_variable_values(self):
            self.value_target = 0.0
            self.Kp = 2
            self.Ki = 4
            self.Kd = 0.00001
            self.curr_error  = 0.0
            self.last_error  = 0.0
            self.derivative_error = 0.0
            self.output_positive_offset = 0.1
            self.output_negative_offset = -0.1

        def set_target(self, value):
            self.value_target = value

        def set_kp(self, kp_input):
            self.Kp = float(kp_input)

        def set_ki(self, ki_input):
            self.Ki = float(ki_input)

        def set_kd(self, kd_input):
            self.Kd = float(kd_input)

        def compute_PID_first_iteration(self):
            self.curr_error  = self.value_target - self.controller.sensor_value
            self.last_error = self.curr_error
            self.compute_PID()

        def compute_PID(self):
            self.last_error = self.curr_error
            self.curr_error  = self.value_target - self.controller.sensor_value
            # offset is a interpretation for Integrative error component
            if (self.curr_error >= 0):
                self.output_positive_offset += self.Ki * self.curr_error
                offset = self.output_positive_offset
            else:
                self.output_negative_offset += self.Ki * self.curr_error
                offset = self.output_negative_offset
            self.derivative_error = (self.curr_error - self.last_error) / self.controller.dt
            # value pid calculation
            self.output =     offset                                         \
                          + ( self.Kp * self.curr_error )                    \
                          - ( self.Kd * self.derivative_error )
            # pid calculation done
            return self.output
            
