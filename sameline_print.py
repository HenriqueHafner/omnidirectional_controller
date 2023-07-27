# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 14:50:09 2022

@author: robotlab
"""

import sys, time

for i in range(0, 101, 10):
  print('\r You have finished ', i, end='')
  sys.stdout.flush()
  time.sleep(0.5)
print