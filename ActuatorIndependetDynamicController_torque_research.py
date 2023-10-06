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
        self.Initialize_variable_values()
        self.print_debug = True
        self.PosCon = None

    def Initialize_variable_values(self):
        # operational state
        self.state_code = 0
        # Sensor
        self.sensor_timestamp = 0.2
        self.sensor_last_timestamp = 0.1
        self.sensor_value = 0.0
        self.sensor_last_value = 0.0
        self.dt = 0.1
        #Actuator
        self.amplification_factor = 5 * 1e5
        # state vector is : Position, Velocity, Acceleration, Jerk, jounce
        self.state_data_a    = array('f', [0.0] * 5)
        self.state_data_b    = array('f', [0.0] * 5)
        self.state_data = [self.state_data_a, self.state_data_b]
        self.most_recent_data_index = 0
        self.last_recent_data_index = 1
        # Position aproximation
        self.position_departure = 0
        self.position_departure = 0
        self.position_arrival = 0
        self.position_middleway = 0
        self.time_middleway = 0.2

    def loop_routine_iteration(self):
        self.get_sensor_data()
        self.state_update()

    def cronological_data_index_roll(self):
        if (self.most_recent_data_index == 0):
            self.most_recent_data_index = 1
            self.last_recent_data_index = 0
        else:
            self.most_recent_data_index = 0
            self.last_recent_data_index = 1

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


    def state_update(self):
        self.cronological_data_index_roll()       
        dt = self.dt
        i_l = self.last_recent_data_index
        i_m = self.most_recent_data_index
        self.state_data[i_m][0] = self.sensor_value # set position
        self.state_data[i_m][1] = ( self.state_data[i_m][0] - self.state_data[i_l][0] ) / dt # set velocity
        self.state_data[i_m][2] = ( self.state_data[i_m][1] - self.state_data[i_l][1] ) / dt # set acceleration
        self.state_data[i_m][3] = ( self.state_data[i_m][2] - self.state_data[i_l][2] ) / dt # set jerk
        self.state_data[i_m][4] = ( self.state_data[i_m][3] - self.state_data[i_l][3] ) / dt # set jounce
        # self.print_variables()

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
        
    def calibrate_local_output_resiliance(self): # seconds
        print("Waiting for physics noise to fade.")
        time.sleep(5)
        print("Calibrating..")
        self.get_inital_condition()
        curr_accleration = self.state_data[self.most_recent_data_index][2]
        curr_pos    = self.state_data[self.most_recent_data_index][0]
        output_value = 0.0
        # get noise data
        self.max_pos = 0
        max_vel = 0
        max_acc = 0
        for i in range(5):
            self.get_sensor_data()
            self.state_update()
            self.max_pos = max(self.max_pos, abs(self.state_data[self.most_recent_data_index][0]))
            max_vel = max(max_vel, abs(self.state_data[self.most_recent_data_index][1]))
            max_acc = max(max_acc, abs(self.state_data[self.most_recent_data_index][2]))
        print("Max noise pos: ", self.max_pos)
        print("Max noise vel: ", max_vel)
        print("Max noise acc: ", max_acc)
        min_pos = max(self.max_pos*4, 90.0)
        min_acc = max(max_acc*1.5, 1.0)
        max_vel = 2
        min_vel = 2
        output_iminent_motion_value = 0
        for i in range(3, 8):
            start_pos    = self.state_data[self.most_recent_data_index][0]
            delta_p = 0.0
            interval_iterations = 1000
            offset_value = 10.0**i
            output_value = offset_value # initially
            grow_rate = offset_value*(10.0/interval_iterations)
            for j in range(interval_iterations):
                self.call_impulse_order(output_value, self.dt*2)
                self.state_update()
                curr_pos         = self.state_data[self.most_recent_data_index][0]
                curr_vel         = self.state_data[self.most_recent_data_index][1]
                curr_accleration = self.state_data[self.most_recent_data_index][2]
                print("\r output: ", self.float_format(output_value), " position:", self.float_format(curr_pos), " vel:", self.float_format(curr_vel), " acce:", self.float_format(curr_accleration), end='')
                sys.stdout.flush()
                if(curr_pos > start_pos+min_pos):
                    break
                if (curr_vel > max_vel):
                    output_value = 0
                    continue
                if (curr_accleration < min_acc):
                    offset_value += grow_rate
                    output_value = offset_value
                else:
                    offset_value -= grow_rate
                    output_value = offset_value

            if(curr_pos > min_pos):
                break
        delta_p =  self.state_data[self.last_recent_data_index][0] - start_pos
        print(' ')
        print("Delta position: ", delta_p)
        print("Offset value: ", offset_value)
        print("Curr aceleration: ", self.state_data[self.most_recent_data_index][2])
        print("Delta position: ", delta_p)
        print("Iminent motion output value: ", output_iminent_motion_value)

    def call_impulse_order(self, value, time_period):
        timestamp, sensor_value = self.interface.send_type_4_message(self.ID, value, time_period)
        self._set_sensor_data(timestamp, sensor_value)
        
    def jerk_control(self):
        p0 = self.outputforce
        dp = self.outputforce_increment
        state_vector = self.state_data[self.most_recent_data_index]
        jerk_current = state_vector[3]
        jerk_control_error = jerk_current - self.jerk_goal
        dp = dp - jerk_control_error*0.002
        force = p0 + dp
        self.outputforce_increment = dp
        self.outputforce = force

    def position_control(self, value, period, is_relative_position = True):
        if not (self.PosCon):
            self.PosCon = self.PID_Component("Position_PID_Controller", self)
        self.get_sensor_data()
        self.get_sensor_data()
        target_pos = value
        if (is_relative_position):
            target_pos += self.sensor_value
        self.PosCon.set_target(target_pos)
        self.PosCon.compute_PID_first_iteration()
        start_time = self.sensor_timestamp
        last_print = self.sensor_timestamp
        while(self.sensor_timestamp - start_time < period):
            self.PosCon.compute_PID()
            output_power = self.PosCon.output * self.amplification_factor
            self.call_impulse_order(output_power, self.dt*10)
            if (self.sensor_timestamp - last_print > 0.2):
                last_print = self.sensor_timestamp
                if(self.print_debug):
                    print("\r output:", self.float_format(self.PosCon.output),
                          " distance:", self.float_format(self.PosCon.curr_error),
                          " dt:", self.float_format(self.dt),
                          end='')
        if(self.print_debug):
            print(" ")
        return True

    def position_approach_setup(self, delta_position, delta_time):
        state_vector = self.state_data[self.most_recent_data_index]
        starting_time = self.sensor_last_timestamp
        starting_position = state_vector[0]
        v0 = state_vector[1]
        a0 = state_vector[2]
        delta_position_middleway = delta_position/2.0
        delta_time_middleway = delta_time/2.0
        self.position_departure = starting_position
        self.position_middleway = starting_position + delta_position_middleway
        self.position_arrival   = starting_position + delta_position
        self.time_middleway     = starting_time     + delta_time_middleway
        self.time_arrival       = starting_time     + delta_time
        dt = max(self.dt*20, delta_time_middleway)        
        dt_squad = dt*dt
        dt_cubed = dt_squad*dt
        self.jerk_goal = (6.0 / dt_cubed) * (delta_position_middleway - v0 * dt - (0.5) * a0 * dt_squad)
        self.accelerate_twards = True
            
    def position_approach_control(self):
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

        def calibrate(self, initial_calibration_values = None): # implementar
            if not (initial_calibration_values):
                self.get_positive_eminent_output
                self.get_positive_eminent_output

### continuar aqui, implementar controle de acceleração PID, pois é a mais linear

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
            
        def compute_PID_first_iteration(self):
            self.curr_error  = self.value_target - self.controller.sensor_value
            self.last_error = self.curr_error
            self.compute_PID()
            # pid calculation done