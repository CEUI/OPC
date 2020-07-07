#!/usr/bin/env python

import argparse
import random

# type determines the type of the argument

parser = argparse.ArgumentParser()
   
parser.add_argument('-n', type=int, required=True, help="define the number of random integers")
args = parser.parse_args()

n = args.n

for i in range(n):
    print(random.randint(-100, 100))