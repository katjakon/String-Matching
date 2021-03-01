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
    DEMOS = ({"pattern": ["he"],
              "input_text": "She saw her.",
              "pattern_file": None},
             {"pattern": ["she"],
              "input_text": "She saw her.",
              "pattern_file": None},
             {"pattern": ["she"],
              "input_text": "She saw her.",
              "pattern_file": None,
              "i": True},
             {"pattern": ["her", "he"],
              "input_text": "She saw her.",
              "pattern_file": None},
             {"pattern": ["she", "he", "his", "her"],
              "input_text": "She saw her.",
              "pattern_file": None,
              "n": True},
             {"pattern": ["she", "he", "his", "her"],
              "input_text": "demo/demo1.txt",
              "pattern_file": None},
             {"pattern": ["she", "he", "his", "her"],
              "input_text": "demo/demo1.txt",
              "pattern_file": None,
              "v": True},
             {"pattern": ["she", "he", "his", "her"],
              "input_text": "demo/",
              "pattern_file": None},
             )

    def __init__(self,
                 pattern,
                 pattern_file,
                 input_text,
                 i=False,
                 v=False,
                 n=False):
        self.pattern = pattern
        self.pattern_file = pattern_file
        self.input = input_text
        self.i = i
        self.v = v
        self.n = n
        self.match = self._create_match()

    def __str__(self):
        commands = "search "
        if self.i:
            commands += "-i "
        if self.v:
            commands += "-v "
        if self.n:
            commands += "-n "
        if self.pattern:
            commands += "--pattern "
            for pattern in self.pattern:
                commands += '"{}" '.format(pattern)
        else:
            commands += "--pattern_file {} ".format(self.pattern_file)
        if self.input_from_dir or self.input_from_file:
            commands += self.input
        else:
            commands += '"{}"'.format(self.input)
        return commands

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
        if self.input.endswith(self.INPUT_EXT):
            return True
        return False

    @property
    def input_from_dir(self):
        if self.input.endswith(self.DIRS):
            return True
        return False

    @staticmethod
    def print_matches(match_dict):
        if not match_dict:
            print("No matches found.")
        for match in match_dict:
            print("{}: {}".format(match,
                                  ",".join([str(i) for i in match_dict[match]])))

    def _match_in_file(self, file=None):
        if file is None:
            file = self.input
        with open(os.path.join(file), encoding="utf-8") as file_in:
            count = 1
            index = 0
            matches = dict()
            for line in file_in:
                if self.i:
                    line = line.lower()
                if self.v:
                    matches = self.match.match_pattern(line)
                    if matches:
                        line_str = "Line {}".format(count)
                        print("{:-^30}".format(line_str))
                        self.print_matches(matches)
                else:
                    matches = self.match.match_pattern(line,
                                                       start=index,
                                                       matches=matches)
                index += len(line)
                count += 1
            if not self.v:
                self.print_matches(matches)

    def _match_in_dir(self):
        files = [file for file in os.listdir(self.input)
                 if file.endswith(self.INPUT_EXT)]
        for file in files:
            print("{:=^30}".format(file))
            path = os.path.join(self.input, file)
            self._match_in_file(path)

    def _match_in_str(self):
        if self.i:
            self.input = self.input.lower()
        matches = self.match.match_pattern(self.input)
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

    @classmethod
    def demo(cls):
        for demo in cls.DEMOS:
            s = cls(**demo)
            print(s)
            s.run()
            print("-"*60)


if __name__ == "__main__":
    s = Search.demo()
    with open("demo/demo1.txt") as f:
        content = f.read()
        print(content[14:18])
