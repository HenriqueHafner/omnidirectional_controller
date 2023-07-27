# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:08:28 2023

@author: robotlab
"""

from array import array

class Path_manager:
    def __init__(self):
        self.state_data_a    = array('f', [0.0] * 4)
        self.state_data_b    = array('f', [0.0] * 4)
        self.state_data_c    = array('f', [0.0] * 4)
        self.state_data_d    = array('f', [0.0] * 4)
        self.legacy_state    = self.state_data_a
        self.past_state      = self.state_data_b
        self.departure_state = self.state_data_c
        self.arrival_state   = self.state_data_d
        self.state_vector    = [self.legacy_state, self.past_state, self.departure_state, self.arrival_state]
        self.control_state   = array('f', [0.0] * 3)
        self.control_state_timestamp = float(0.1)