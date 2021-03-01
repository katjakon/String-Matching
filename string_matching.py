# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:33:24 2021

@author: HP I5
"""


class StringMatching:

    ALGORITHMS = ("aho-corasick", "naive")

    def __init__(self, algorithm="aho-corasick", keywords=None):
        self._keywords = keywords
        self.algorithm = algorithm
        self._goto = dict()
        self.output = dict()
        self.fail = dict()

        if self.algorithm not in self.ALGORITHMS:
            raise NotImplementedError("Matching algorithm not implemented.")

        if self.keywords is not None:
            if "" in self.keywords:
                raise ValueError("Invalid Keyword:"
                                 "Can't search for empty string.")
            if self.algorithm == "aho-corasick":
                self.__construct_functions()

    @property
    def keywords(self):
        return self._keywords

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

    def _aho_corasick_match(self, input_text, start=0, matches=None):
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

    def _naive_match(self, input_text, start=0, matches=None):
        if matches is None:
            matches = dict()
        for i, char in enumerate(input_text):
            for word in self.keywords:
                if word == input_text[i:i+len(word)]:
                    matches.setdefault(word, set())
                    matches[word].add(start+i)
        return matches

    def match_pattern(self, input_text, start=0, matches=None):
        if matches is None:
            matches = dict()
        if self.algorithm == "aho-corasick":
            matches = self._aho_corasick_match(input_text, start=start, matches=matches)
        elif self.algorithm == "naive":
            matches = self._naive_match(input_text, start=start, matches=matches)
        return matches

    @classmethod
    def set_functions(cls, goto, fail, output, algorithm="aho-corasick"):
        string_match = cls(algorithm)
        if algorithm == "aho-corasick":
            string_match._goto = goto
            string_match.fail = fail
            string_match.output = output
        return string_match


if __name__ == "__main__":
    words = [""]
    text = "ushers"
    try:
        s = StringMatching("aho-corasick", words)
    except ValueError as e:
        print(e)
    # print(s._goto)
    # print(s.fail)
    # print(s.output)
    # g = {0: {'s': 1, 'h': 4}, 1: {'h': 2}, 2: {'e': 3}, 4: {'e': 5}, 5: {'r': 6}, 6: {'s': 7}}
    # f = {1: 0, 4: 0, 2: 4, 5: 0, 3: 5, 6: 0, 7: 1}
    # o = {3: {'she', 'he'}, 5: {'he'}, 7: {'hers'}, 6: {'her'}}
    # t = StringMatching.set_functions(g, f, o)
    # print(t.match_pattern(text))
