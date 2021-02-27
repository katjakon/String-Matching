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
        self.match = self._create_match()

    def _create_match(self):
        if self.pattern_file:
            return self.pattern_from_file()
        alg = "aho-corasick"
        if self.n:
            alg = "naive"
        if self.i:
            self.pattern = [pattern.lower() for pattern in self.pattern]
        return StringMatching(algorithm=alg, keywords=self.pattern)

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

    def _match_in_file(self, file=None):
        if file is None:
            file = self.text
        path = os.path.join(file)
        with open(path, encoding="utf-8") as file_in:
            if self.v:
                count = 1
                for line in file_in:
                    if self.i:
                        line = line.lower()
                    matches = self.match.match_pattern(line)
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
                    matches = self.match.match_pattern(line, start=at, matches=matches)
                    at += len(line)
                self.print_matches(matches)

    def _match_in_dir(self):
        files = [file for file in os.listdir(self.text) if file.endswith(self.INPUT_EXT)]
        for file in files:
            print(file)
            path = os.path.join(self.text, file)
            self._match_in_file(path)

    def _match_in_str(self):
        if self.i:
            self.text = self.text.lower()
        matches = self.match.match_pattern(self.text)
        self.print_matches(matches)

    def _pattern_from_file(self):
        pass

    def run(self):
        if self.input_from_file:
            self._match_in_file()
        elif self.input_from_dir:
            self._match_in_dir()
        else:
            self._match_in_str()


if __name__ == "__main__":
    s = Search(["she", "he","hers", "his"], None, "demo/", False, True, False)
    s.run()