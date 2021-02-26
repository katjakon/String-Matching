# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 14:54:52 2021

@author: HP I5
"""

import argparse

from user_commands import Search


def main():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='command')
    search_p = subs.add_parser("search")
    save_p = subs.add_parser("save")
    demo_p = subs.add_parser("demo")
    search_p.add_argument("-n", "-naive",  action="store_true")
    search_p.add_argument("-i", "-insensitive", action="store_true")
    search_p.add_argument("-v", "-verbose", action="store_true")
    g = search_p.add_mutually_exclusive_group(required=True)
    g.add_argument("--pattern")
    g.add_argument("--pattern_file", type=argparse.FileType('r', encoding='UTF-8'))
    search_p.add_argument("input_text")
    args = parser.parse_args()
    if args.command == "search":
        search = Search(pattern=args.pattern,
                        pattern_file=args.pattern_file,
                        text=args.input_text,
                        i=args.i,
                        v=args.v,
                        n=args.n)
        try:
            search.run()
        except OSError as e:
            print(e)
            parser.print_help()


if __name__ == "__main__":
    main()
