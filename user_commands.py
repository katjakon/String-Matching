# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 12:12:37 2021

@author: HP I5
"""
import os

from string_matching import StringMatching


class Search:

    INPUT_EXT = (".txt",)
    DIRS = ("\\", "/")
    DEMOS = ({"pattern": ["he"],
              "input_text": "She saw her."},
             {"pattern": ["she"],
              "input_text": "She saw her."},
             {"pattern": ["she"],
              "input_text": "She saw her.",
              "i": True},
             {"pattern": ["her", "he"],
              "input_text": "She saw her."},
             {"pattern": ["she", "he", "his", "her"],
              "input_text": "She saw her.",
              "n": True},
             {"pattern": ["she", "he", "his", "her"],
              "input_text": "demo/demo1.txt"},
             {"pattern": ["she", "he", "his", "her"],
              "input_text": "demo/demo1.txt",
              "v": True},
             {"pattern": ["she", "he", "his", "her"],
              "input_text": "demo/"}
             )

    def __init__(self,
                 pattern,
                 input_text,
                 i=False,
                 v=False,
                 n=False):
        self.pattern = pattern
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
        if self.input_from_dir or self.input_from_file:
            commands += "{} ".format(self.input)
        else:
            commands += '"{}" '.format(self.input)
        for pattern in self.pattern:
            commands += '"{}" '.format(pattern)
        return commands

    def _create_match(self):
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
            match_index = map(lambda x: str(x), match_dict[match])
            print("{}: {}".format(match, ",".join(match_index)))

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
                    line_match = self.match.match_pattern(line)
                    if line_match:
                        matches[count] = line_match
                else:
                    matches = self.match.match_pattern(line,
                                                       start=index,
                                                       matches=matches)
                index += len(line)
                count += 1
            if not matches or not self.v:
                self.print_matches(matches)
            else:
                for line in matches:
                    line_str = "Line {}".format(line)
                    print("{:-^30}".format(line_str))
                    self.print_matches(matches[line])

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
            print()


if __name__ == "__main__":
    s = Search.demo()
