# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 14:54:52 2021

@author: HP I5
"""

import argparse

input_parser = argparse.ArgumentParser()
subs = input_parser.add_subparsers(dest='command')
search_p = subs.add_parser("search")
save_p = subs.add_parser("save")
demo_p = subs.add_parser("demo")


# input_parser.add_argument("command", choices=["search", "save", "demo"])
input_parser.add_argument("-i", "-insensitive", action="store_true")
search_p.add_argument("-n", "-naive",  action="store_true")
input_parser.add_argument("-v", "-verbose", action="store_true")
g = search_p.add_mutually_exclusive_group(required=True)
g.add_argument("--pattern", type=lambda x: x.split(","))
g.add_argument("--pattern_file", type=argparse.FileType('r', encoding='UTF-8'))
search_p.add_argument("input_text")
a =input_parser.parse_args()

print(a)