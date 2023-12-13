# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 14:30:09 2023

@author: robotlab
"""
import math

def degrees_to_mp180(degrees):
    angle = (degrees + 180.0) % 360.0 - 180.0
    return angle

def min_angle_distance(angle1, angle2):
    angle1 = degrees_to_mp180(angle1)
    angle2 = degrees_to_mp180(angle2)
    delta_angle = angle2 - angle1
    distance_angle = abs(delta_angle)
    if (delta_angle >= 0):
        delta_sign = 1
    else:
        delta_sign = -1
    if (distance_angle <= 180.0):
        direction = delta_sign
    else:
        direction = delta_sign*-1
        distance_angle = 360-distance_angle
    return direction, distance_angle

def min_angle_simetry(angle):
    angle_raw = degrees_to_mp180(angle)
    angle_sim = degrees_to_mp180(angle+180)
    if (abs(angle_raw) <= abs(angle_sim)):
        return angle_raw
    else:
        return angle_sim

def aproximation_order3(ds, ct, tt):
    t = ct/tt
    t2 = t*t
    t3 = t2*t
    factor = ( -2*t3 + 3*t2 )
    if (factor>1):
        factor = 1
    elif (factor<0):
        factor = 0
    pos = ds*factor
    return pos

def angle_wheels_bikemode(point_on_axis):
    point_above1 = (-0.5, 1)
    point_above2 = (+0.5, 1)
    vector1 = (point_above1[0] - point_on_axis, point_above1[1])
    vector2 = (point_above2[0] - point_on_axis, point_above2[1])
    angle1 = math.atan2(vector1[1], vector1[0])
    angle2 = math.atan2(vector2[1], vector2[0])
    angle1_degrees = math.degrees(angle1)
    angle2_degrees = math.degrees(angle2)
    angle1_degrees = min_angle_simetry(angle1_degrees)
    angle2_degrees = min_angle_simetry(angle2_degrees)
    angle1_degrees = math.trunc(angle1_degrees * 100) / 100.0
    angle2_degrees = math.trunc(angle2_degrees * 100) / 100.0
    print(angle1_degrees, angle2_degrees)
    return angle1_degrees, angle2_degrees

def turning_sign_bikemode(point_on_axis):
    signs = [1,-1,1,1]
    if (point_on_axis > -0.5):
        signs[0] = -1
    if (point_on_axis > 0.5):
        signs[1] = -1
    if (point_on_axis > -0.5):
        signs[2] = -1
    if (point_on_axis > 0.5):
        signs[3] = -1
    return signs


#ajustar velocidade linear angular
def velocity_factor_bikemode(point_on_axis, r_scale):
    radius = [0,0,0,0]
    radius[0] = abs(math.hypot((-0.5 - point_on_axis), 1))
    radius[1] = abs(math.hypot((+0.5 - point_on_axis), 1))
    radius[2] = abs(-0.5 - point_on_axis)
    radius[3] = abs(+0.5 - point_on_axis)
    factors = [0,0,0,0]
    for index in range(4):
        r = radius[index]
        if (r < 0.0005):
            factors[index] = 0
        else:
            f = r*r_scale
            f = math.trunc(f * 10000) / 10000.0
            factors[index] = f
    return factors

def point_from_omega_v_ration(omega,v):
    if (omega >= 0.05):
        return v/omega
    else:
        return 1.0e9

def bikemode_params(point_on_axis, r_scale):
    angle1_degrees, angle2_degrees = angle_wheels_bikemode(point_on_axis)
    signs = turning_sign_bikemode(point_on_axis)
    factors = velocity_factor_bikemode(point_on_axis, r_scale)
    print(signs)
    print(factors)
    return angle1_degrees, angle2_degrees , signs , factors



























