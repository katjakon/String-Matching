# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:33:24 2021

@author: HP I5
"""

class AhoCorasick:

    def __init__(self, keywords):
        self.keywords = keywords
        self.goto = dict()
        self.output = dict()

        self.__construct()

    def __construct(self):
        newstate = 0
        for word in self.keywords:
            state = 0
            for char in word:
                if state in self.goto and char in self.goto[state]:
                    state = self.goto[state][char]
                else:
                    newstate += 1
                    self.goto.setdefault(state, dict())
                    self.goto[state][char] = newstate
                    state = newstate
            self.output.setdefault(state, set()).add(word)

a = AhoCorasick(["he", "she", "his", "hers"])
print(a.goto)
print(a.output)

