# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 18:24:31 2022
@author: robotlab
"""
import Tower_Controller
import GUI
import time

pi = 3.1416

class OMNI_Control:
    def __init__(self):
        self.xpos = float(0)
        self.ypos = float(0)
        self.tran_vec_mod = float(0)
        self.tran_vec_dir = float(0)
        self.rota_vec_mod = float(0)
        self.moving_mode = 0  # 0-NeverMove 1-SpinOnly 2-CrabOnly 3-DoubleDiff 4-Omni
        self.moving_mode_goal = 0
        self.towers = [0,0,0,0]
        self.towers[0] = Tower_Controller.Tower_Motion_Ctrl()
        self.towers[0].name_id = 'Front_Right'
        self.towers[0].xpos = +1.0
        self.towers[0].ypos = +1.0
        self.towers[1] = Tower_Controller.Tower_Motion_Ctrl()
        self.towers[1].name_id = 'Bot_Right'
        self.towers[1].xpos = +1.0
        self.towers[1].ypos = -1.0
        self.towers[2] = Tower_Controller.Tower_Motion_Ctrl()
        self.towers[2].name_id = 'Bot_Left'
        self.towers[2].xpos = -1.0
        self.towers[2].ypos = -1.0
        self.towers[3] = Tower_Controller.Tower_Motion_Ctrl()
        self.towers[3].name_id = 'Front_Left'
        self.towers[3].xpos = -1.0
        self.towers[3].ypos = +1.0


    def towers_steer(self, tower_to_steer=-1):
        if tower_to_steer == -1:
            total_residue = 0
            for tower in self.towers:
                residue = tower.steer()
                total_residue += residue
            return total_residue

    def set_target_moving_mode(self, targ_moving_mode):
        self.targ_moving_mode = targ_moving_mode
        return True
    
    def moving_mode_adjust(self):
        if self.moving_mode != self.targ_moving_mode:
            if self.targ_moving_mode == 0:
                residue = 0.0
            elif self.targ_moving_mode == 1:
                residue = self.moving_mode_spin_adjust()
            elif self.targ_moving_mode == 2:
                residue = self.moving_mode_crab_adjust()
        else:
            residue = 0
        return residue
                
    def moving_mode_spin_adjust(self):
        self.towers[0].set_heading_goal((-1)*(1/8)*(2*pi))
        self.towers[1].set_heading_goal((+1)*(1/8)*(2*pi))
        self.towers[2].set_heading_goal((-1)*(1/8)*(2*pi))
        self.towers[3].set_heading_goal((+1)*(1/8)*(2*pi))
        residue = self.towers_steer()
        if abs(residue) < self.towers[0].heading_rad_threshold:
            residue = 0
        return residue
    
    def moving_mode_crab_adjust(self):
        heading_values = [None, None, None, None]
        heading_target = [None, None, None, None]
        for i in range(len(heading_values)):
            heading_values[i] = self.towers[i].get_heading_angle()
        #
        heading_mean = sum(heading_values)/len(heading_values)
        for i in range(len(heading_target)):
            heading_target[i] = heading_mean
            self.towers[i].set_heading_goal(heading_mean)
        #
        residue = self.towers_steer()
        if abs(residue) < self.towers[0].heading_rad_threshold:
            residue = 0
        return residue


    def _gui_handler(self):
        towers_angle = []
        for tower in self.towers:
            towers_angle.append(tower.get_heading_angle())
            lines = self.gui_pointer.features[0] 
        lines.set_angle_data(towers_angle)
        self.gui_pointer.GUI_loop()
        
    def _set_gui_pointer(self, graph_inter_l):
        self.gui_pointer = graph_inter_l
              
    def test(self):
        print('move mode spin test')
        self.set_target_moving_mode(1)
        for i in range(100):
            residue = self.moving_mode_adjust()
            self._gui_handler()
            if i%100 ==0:
                print(residue)
        print('free heading set test')
        self.towers[0].set_heading_goal((-1)*(2/8)*(2*pi))
        self.towers[1].set_heading_goal((+1)*(3/8)*(2*pi))
        self.towers[2].set_heading_goal((-1)*(1.5/8)*(2*pi))
        self.towers[3].set_heading_goal((+1)*(2.5/8)*(2*pi))
        for i in range(400):
            residue = self.towers_steer(-1)
            self._gui_handler()
            if i%100 ==0:
                print(residue)
        print('move mode crab test')
        self.set_target_moving_mode(2)
        for i in range(400):
            residue = self.moving_mode_adjust()
            self._gui_handler()
            if i%100 ==0:
                print(residue)
        

def test():
    controller = OMNI_Control()
    graphical_interface = GUI.construc_GUI()
    controller._set_gui_pointer(graphical_interface)
    controller.test()

test()

















        