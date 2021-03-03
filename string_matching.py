# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:33:24 2021

@author: HP I5
"""


class NaiveMatching:

    def __init__(self, keywords=None):
        if keywords is None:
            keywords = []
        self._keywords = keywords

        assert all(isinstance(keyword, str) for keyword in self.keywords), "Expected a string"

        if "" in self.keywords:
            raise ValueError("Invalid Keyword: "
                             "Can't match empty string.")

    @property
    def keywords(self):
        return self._keywords

    def match_pattern(self, input_text, start=0, matches=None):
        if matches is None:
            matches = dict()
        for i, char in enumerate(input_text):
            for word in self.keywords:
                if word == input_text[i:i+len(word)]:
                    matches.setdefault(word, set())
                    matches[word].add(start+i)
        return matches


class AhoCorasickMatching(NaiveMatching):

    def __init__(self, keywords=None):
        super().__init__(keywords)
        self._goto = dict()
        self.output = dict()
        self.fail = dict()

        self.__construct_functions()

    def __construct_functions(self):
        # Construct goto function and partial output function.
        newstate = 0
        for word in self.keywords:
            state = 0
            for char in word:
                if state in self._goto and char in self._goto[state]:
                    state = self.goto(state, char)
                else:
                    newstate += 1
                    self._goto.setdefault(state, dict())
                    self._goto[state][char] = newstate
                    state = newstate
            self.output.setdefault(state, set()).add(word)
        # Construct failure function and final output function.
        sigma = {char for word in self.keywords for char in word}
        queue = []
        for char in sigma:
            out = self.goto(0, char)
            if out is not False and out != 0:
                queue.append(out)
                self.fail[out] = 0
        while queue:
            state = queue.pop(0)
            for char in sigma:
                if self.goto(state, char) is not False:
                    out = self.goto(state, char)
                    queue.append(out)
                    curr_state = self.fail[state]
                    while self.goto(curr_state, char) is False:
                        curr_state = self.fail[curr_state]
                    self.fail[out] = self.goto(curr_state, char)
                    output = self.output.get(out, set())
                    if self.fail[out] in self.output:
                        self.output[out] = output.union(self.output[self.fail[out]])

    def goto(self, state, char):
        if state in self._goto:
            if state == 0 and char not in self._goto[state]:
                return 0
            elif char in self._goto[state]:
                return self._goto[state][char]
        return False

    def match_pattern(self, input_text, start=0, matches=None):
        if matches is None:
            matches = dict()
        state = 0
        for i, char in enumerate(input_text):
            while self.goto(state, char) is False:
                state = self.fail[state]
            state = self.goto(state, char)
            if state in self.output:
                for out in self.output[state]:
                    matches.setdefault(out, set())
                    matches[out].add(start+i-len(out)+1)
        return matches


if __name__ == "__main__":
    words = ["she", "he", "his", "her", "hers"]
    text = "ushers"
    try:
        s = AhoCorasickMatching(words)
        print(s.keywords)
    except ValueError as e:
        print(e)

