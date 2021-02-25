# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 14:54:52 2021

@author: HP I5
"""

import argparse
import re

input_parser = argparse.ArgumentParser()
subs = input_parser.add_subparsers()
search_p = subs.add_parser("suche")
save_p = subs.add_parser("speicher")
demo_p = subs.add_parser("demo")



def split_pattern(pattern_strings):
    return re.split(r"(?!\\),", pattern_strings)

print(split_pattern("hallo,hallo ich\,weiß"))

# input_parser.add_argument("command", choices=["search", "save", "demo"])
input_parser.add_argument("-i", action="store_true")
search_p.add_argument("-n", "-naive",  action="store_true")
input_parser.add_argument("-v", "-verbose",  action="store_true")
g = search_p.add_mutually_exclusive_group(required=True)
g.add_argument("--pattern", nargs="+")
g.add_argument("--pattern_file")
search_p.add_argument("input_text")
a =input_parser.parse_args()

