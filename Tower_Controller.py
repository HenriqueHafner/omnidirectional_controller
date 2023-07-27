# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 17:44:20 2022

@author: robotlab
"""

from numpy import array
import numpy as np

class Tower_Motion_Ctrl:
    def __init__(self):
        self.name_id = 'Undefined'
        self.heading_rad_angle = float(0)
        self.heading_rad_goal = float(0)
        self.heading_rad_step = float(2*3.1416*(1e-3))
        self.heading_rad_threshold = float(2*3.1416*(2e-3))
        self.xpos = 0
        self.ypos = 0
        self.rolling_log_size = 50
        self.rolling_log = np.array([[float(0)]*5]*self.rolling_log_size)
        self.rolling_log_index = int(1)
        self.rolling_log_max_index = self.rolling_log_size-1
        self.rolling_step = float(2*3.1416*(1e-2))
    
    def steer(self, simulate = True):
        if simulate:
            return self.steer_simulated()
    
    def steer_simulated(self):
        """
        Steer twords the set goal.
        Returns
        -------
        float
            return discrepance (goal residue) if motion success.
        bool
            return False if no motion done.

        """
        discrepance = (self.heading_rad_angle - self.heading_rad_goal)
        if abs(discrepance) > self.heading_rad_threshold:
            if  discrepance > 0:
                self.heading_rad_angle -= self.heading_rad_step
            elif discrepance < 0:
                self.heading_rad_angle += self.heading_rad_step
            residue = abs(discrepance)
            return residue
        else:
            return False

    def set_heading_goal(self, heading:float):
        self.heading_rad_goal = heading
        return True
    
    def get_heading_angle(self):
        heading = self.heading_rad_angle
        return heading

    def roll(self,sign):
        """

        Parameters
        ----------
        sign : +1 or -1 int
            the signal of rolling vector, positive or negative.

        Returns
        -------
        dx : TYPE
            x componente of displacemente vector.
        dy : TYPE
            y componente of displacemente vector.

        """

        roll = sign*self.rolling_step
        index = self.rolling_log_index
        dx,dy = self._compute_displacement(roll)
        self.rolling_log[index][0] = dx
        self.rolling_log[index][1] = dy
        self.rolling_log[index][2] = self.heading_rad_angle
        self.rolling_log[index][3] = self.heading_rad_goal
        self.rolling_log[index][4] = roll
        index += 1
        if index >= self.rolling_log_max_index:
            index = 1
        self.rolling_log_index = index
        return dx, dy
    
    def _compute_displacement(self,roll):
        x_cos = np.cos(self.heading_rad_angle)
        y_sin = np.sin(self.heading_rad_angle)
        dx  = x_cos*roll
        dy  = y_sin*roll
        return dx, dy
    
    def print_status(self):
        log_line = self.rolling_log[self.rolling_log_index-1]
        log_line_formatted = []
        for value in log_line:
            log_line_formatted.append(np.format_float_scientific(value, precision=4, trim='k'))
        print(self.name_id, ' ', log_line_formatted)
















