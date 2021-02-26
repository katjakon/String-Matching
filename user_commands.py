# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 12:12:37 2021

@author: HP I5
"""
import os

from string_matching import StringMatching


class Search:

    INPUT_EXT = (".txt")
    PATTERN_EXT = (".json")
    DIRS = ("\\", "/")

    def __init__(self, pattern, pattern_file, text, i, v, n):
        self.pattern = pattern
        self.pattern_file = pattern_file
        self.text = text
        self.i = i
        self.v = v
        self.n = n

    @property
    def input_from_file(self):
        if self.text.endswith(self.INPUT_EXT):
            return True
        return False

    @property
    def input_from_dir(self):
        if self.text.endswith(self.DIRS):
            return True
        return False

    @staticmethod
    def print_matches(match_dict):
        for match in match_dict:
            print("{}: {}".format(match,
                                  ",".join([str(i) for i in match_dict[match]])))

    def _match_in_file(self, match, file):
        path = os.path.join(file)
        with open(path, encoding="utf-8") as file_in:
            if self.v:
                count = 1
                for line in file_in:
                    if self.i:
                        line = line.lower()
                    matches = match.match_pattern(line)
                    if matches:
                        print("line {}".format(count))
                        self.print_matches(matches)
                    count += 1
            else:
                at = 0
                matches = dict()
                for line in file_in:
                    if self.i:
                        line = line.lower()
                    matches = match.match_pattern(line, start=at, matches=matches)
                    at += len(line)
                self.print_matches(matches)

    def _match_in_dir(self, match):
        files = [file for file in os.listdir(self.text) if file.endswith(self.INPUT_EXT)]
        for file in files:
            print(file)
            path = os.path.join(self.text, file)
            self._match_in_file(match, path)

    def _match_in_str(self, match, text):
        if self.i:
            text = text.lower()
        matches = match.match_pattern(text)
        self.print_matches(matches)

    def _pattern_from_file(self):
        pass

    def run(self):
        alg = "aho-corasick"
        if self.n:
            alg = "naive"
        if self.pattern_file:
            pattern = self._pattern_from_file()
        else:
            pattern = self.pattern
        if self.i:
            pattern = [keyword.lower() for keyword in pattern]
        match = StringMatching(algorithm=alg, keywords=pattern)
        if self.input_from_file:
            self._match_in_file(match, self.text)
        elif self.input_from_dir:
            self._match_in_dir(match)
        else:
            self._match_in_str(match, self.text)

if __name__ == "__main__":
    s = Search(["she", "he","hers", "his"], None, "demo/", False, False, False)
    s.run()
