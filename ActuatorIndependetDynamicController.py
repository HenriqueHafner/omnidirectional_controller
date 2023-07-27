# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 14:02:48 2023

@author: Henrique Hafner Ferreira
"""
from array import array

class AcindyController:
    def __init__(self):
        self.Initialize_variable_values()

    def Initialize_variable_values(self):
        self.sensor_last_timestamp = 0.1
        self.sensor_current_delta_time = 0.15
        self.sensor_position = 0.0
        # state vector is : Position, Velocity, Acceleration, Jerk, jounce
        self.state_data_a    = array('f', [0.0] * 5)
        self.state_data_b    = array('f', [0.0] * 5)
        self.state_data = [self.state_data_a, self.state_data_b]
        self.most_recent_data_index = 0
        self.last_recent_data_index = 1
        # Mechanical force Control
        self.jerk_goal = 0.0
        self.jerk_control_values = []
        self.acce_goal = 0.0
        self.position_departure = 0.0
        self.position_arrival = 0.0
        self.outputforce = 0   
        self.outputforce_increment = 0
        self.position_departure = 0
        self.position_arrival = 0
        self.position_middleway = 0
        self.time_middleway = 0.2
        self.accelerate_twards = True

    def cronological_data_index_roll(self):
        if (self.most_recent_data_index == 0):
            self.most_recent_data_index = 1
            self.last_recent_data_index = 0
        else:
            self.most_recent_data_index = 0
            self.last_recent_data_index = 1

    def get_sensor_data(self, position, timestamp): # Required to implement
        self.sensor_current_delta_time = timestamp - self.sensor_last_timestamp
        self.sensor_last_timestamp = timestamp
        self.sensor_position = position
        
    def state_update(self):
        self.cronological_data_index_roll()       
        dt = self.sensor_current_delta_time
        i_l = self.last_recent_data_index
        i_m = self.most_recent_data_index
        self.state_data[i_m][0] = self.sensor_position # set position
        self.state_data[i_m][1] = ( self.state_data[i_m][0] - self.state_data[i_l][0] ) / dt # set velocity
        self.state_data[i_m][2] = ( self.state_data[i_m][1] - self.state_data[i_l][1] ) / dt # set acceleration
        self.state_data[i_m][3] = ( self.state_data[i_m][2] - self.state_data[i_l][2] ) / dt # set jerk
        self.state_data[i_m][4] = ( self.state_data[i_m][3] - self.state_data[i_l][3] ) / dt # set jounce
        # self.print_variables()
        
    def set_applied_force(self, force): # implementar
        self.outputforce = force
    
    def jerk_control(self):
        p0 = self.outputforce
        dp = self.outputforce_increment
        state_vector = self.state_data[self.most_recent_data_index]
        jerk_current = state_vector[3]
        jerk_control_error = jerk_current - self.jerk_goal
        dp = dp - jerk_control_error * 0.08
        self.outputforce_increment = dp
        force = p0 + dp
        self.outputforce = force
        
    def position_control_setup(self, delta_position, delta_time):
        state_vector = self.state_data[self.most_recent_data_index]
        starting_position = state_vector[0]
        starting_time = self.sensor_last_timestamp
        v0 = state_vector[1]
        a0 = state_vector[2]
        delta_position_middleway = delta_position/2.0
        delta_time_middleway = delta_time/2.0
        self.position_departure = starting_position
        self.position_middleway = starting_position + delta_position_middleway
        self.position_arrival   = starting_position + delta_position
        self.time_middleway     = starting_time     + delta_time_middleway
        self.time_arrival       = starting_time     + delta_time
        dt = max(self.sensor_current_delta_time*20, delta_time_middleway)        
        dt_squad = dt*dt
        dt_cubed = dt_squad*dt
        self.jerk_goal = (6.0 / dt_cubed) * (delta_position_middleway - v0 * dt - (0.5) * a0 * dt_squad)
        self.accelerate_twards = True
            
    def position_control(self):
        if self.accelerate_twards:
            after_middle_pos = (self.state_data[self.most_recent_data_index][0] > self.position_middleway)
            after_middle_time = (self.sensor_last_timestamp > self.time_middleway)
            if (after_middle_pos or after_middle_time):
                self.jerk_goal = (-1.0) * self.jerk_goal 
                self.accelerate_twards = False
            else:
                self.jerk_control()
        else:
            after_arrival_pos = (self.state_data[self.most_recent_data_index][0] >= self.position_arrival)
            after_arrival_time = (self.sensor_last_timestamp >= self.time_arrival)
            if (after_arrival_pos or after_arrival_time):
                self.outputforce = 0
            else:                
                self.jerk_control()
            #implementar testes de jerk e de pos

    def print_variables(self):
        array_to_print = self.state_data[self.most_recent_data_index]
        line_to_print = ""
        for value in array_to_print:
            line_to_print += self.float_format(value) + ' '
        print(line_to_print)
            
    def float_format(self, number):
        formatted_number = "{:+.5f}".format(number)
        return formatted_number

