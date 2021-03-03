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
    search_p = subs.add_parser("search",
                               help="Search for keywords in a string, file "
                               "or directory, type 'search -h' for more info")
    demo_p = subs.add_parser("demo",
                             help="Get a demo with examples for input and output")
    search_p.add_argument("-n", "-naive", action="store_true", help="Use naive matching algorithm")
    search_p.add_argument("-i", "-insensitive", action="store_true", help="Match case insensitive")
    search_p.add_argument("-v", "-verbose", action="store_true", help="Get verbose ouput when matching in files")
    search_p.add_argument("input", help="Text to search in, can be a string, file or directory")
    search_p.add_argument("pattern", nargs="+", help="Patterns to search for.")
    args = parser.parse_args()
    if args.command == "search":
        try:
            search = Search(pattern=args.pattern,
                            input_text=args.input,
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
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
