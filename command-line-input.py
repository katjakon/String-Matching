# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 12:12:37 2021

@author: HP I5
"""
import string_matching

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
        if self.input_text.endswith(self.INPUT_EXT):
            return True
        return False

    @property
    def input_from_dir(self):
        if self.input_text.endswith(self.DIRS):
            return True
        return False

    def _match_in_file(self):
        pass

    def _match_in_dir(self):
        pass

    def _pattern_from_file(self):
        pass

    def run(self):
        if self.pattern:
            
