import os
import json
import math
strategy = "-S2"
for i in range(1,2):
    input_file = "input/16x16/test{}.in".format(i)
    command  = "python3 SAT.py {} {}".format(strategy, input_file)
    os.system(command)
