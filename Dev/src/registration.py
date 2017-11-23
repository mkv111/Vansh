#!/usr/bin/python3
import os
from env import ParamInit, ProfileReg, AncestryReg

os.system('cls' if os.name=='nt' else 'clear')

AncestryReg()
ParamInit()

while True:
    ProfileReg()
