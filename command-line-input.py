# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 12:12:37 2021

@author: HP I5
"""
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

    def _match_in_file(self):
        pass

    def _match_in_dir(self):
        pass

    def _match_in_str(self, match, text, at=0):
        if self.i:
            text = text.lower()
        matches = match.match_pattern(text, start=at)
        for match in matches:
            print("{}: {}".format(match,
                                  ",".join([str(i) for i in matches[match]])))

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
            self._match_in_file()
        elif self.input_from_dir:
            self._match_in_dir()
        else:
            self._match_in_str(match, self.text)

if __name__ == "__main__":
    s = Search(["she", "he","hers", "his"], None, "ushershe", False, False, False)
    s.run()
