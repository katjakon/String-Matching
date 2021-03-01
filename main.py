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
    search_p.add_argument("-f", "-from_file", action="store_true")
    search_p.add_argument("input")
    search_p.add_argument("pattern", nargs="+")
    args = parser.parse_args()
    if args.command == "search":
        try:
            search = Search(pattern=args.pattern,
                            input_text=args.input,
                            f=args.f,
                            i=args.i,
                            v=args.v,
                            n=args.n)
            try:
                search.run()
            except OSError as e:
                print(e)
                search_p.print_help()
        except ValueError as e:
            print(e)
            search_p.print_help()
    elif args.command == "demo":
        Search.demo()


if __name__ == "__main__":
    main()
