# -*- coding: utf-8 -*-
# Katja Konermann
# Matrikelnummer: 802658
"""
Main file of the String Matching Programm.

Command line input is handled here by argparse.
"""
import argparse

from user_commands import Search


def main():
    parser = argparse.ArgumentParser(description="String matching programm")
    subs = parser.add_subparsers(dest='command')
    search_p = subs.add_parser("search",
                               help="Search for keywords in a string, file "
                               "or directory, type 'search -h' for more info")
    demo_p = subs.add_parser("demo",
                             description="Get a demo with examples "
                             "for input and output",
                             help="Get a demo with examples "
                             "for input and output")
    search_p.add_argument("-n",
                          "-naive",
                          action="store_true",
                          help="Use naive matching algorithm")
    search_p.add_argument("-i",
                          "-insensitive",
                          action="store_true",
                          help="Match case insensitive")
    search_p.add_argument("-v",
                          "-verbose",
                          action="store_true",
                          help="Get verbose ouput when matching in files")
    search_p.add_argument("input",
                          help="Text to search in, "
                          "can be a string, file or directory")
    search_p.add_argument("pattern",
                          nargs="+",
                          help="Patterns to search for.")
    args = parser.parse_args()
    if args.command == "search":
        try:
            search = Search(pattern=args.pattern,
                            input_text=args.input,
                            insensitive=args.i,
                            verbose=args.v,
                            naive=args.n)
            try:
                search.run()
            except OSError as error:
                print(error)
                search_p.print_help()
        except ValueError as error:
            print(error)
            search_p.print_help()
    elif args.command == "demo":
        Search.demo()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
