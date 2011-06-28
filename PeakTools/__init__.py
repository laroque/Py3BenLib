#!/usr/bin/python3
'''
  File to make this directory importable as a package.

  All "fit-like" functions will live here. This will include histogram interval fitting to predefined functions, area determinations, width determinations, etc.
'''
from .LorentzianFit import LorentzianFit
from .LiteralFWHM import LiteralFWHM
