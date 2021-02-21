# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:33:24 2021

@author: HP I5
"""


class StringMatching:

    ALGORITHMS = ("aho-corasick", "naive")

    def __init__(self, alogrithm, keywords):
        self.keywords = keywords
        self.algorithm = alogrithm
        self.sigma = {char for word in keywords for char in word}
        self._goto = dict()
        self.output = dict()
        self.fail = dict()

        if self.algorithm not in self.ALGORITHMS:
            raise NotImplementedError("Matching algorithm not implemented")

        if self.algorithm == "aho-corasick":
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
        queue = []
        for char in self.sigma:
            out = self.goto(0, char)
            if out is not False and out != 0:
                queue.append(out)
                self.fail[out] = 0
        while queue:
            state = queue.pop(0)
            for char in self.sigma:
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

    def _aho_corasick_match(self, input_text, start=0):
        output = dict()
        state = 0
        for i, char in enumerate(input_text):
            while self.goto(state, char) is False:
                state = self.fail[state]
            state = self.goto(state, char)
            if state in self.output:
                for out in self.output[state]:
                    output.setdefault(out, set())
                    output[out].add(start+i-len(out)+1)
        return output

    def _naive_match(self, input_text, start=0):
        matches = dict()
        for i, char in enumerate(input_text):
            for word in self.keywords:
                if word == input_text[i:i+len(word)]:
                    matches.setdefault(word, set())
                    matches[word].add(start+i)
        return matches

    def match_pattern(self, input_text, start=0):
        matches = dict()
        if self.algorithm == "aho-corasick":
            matches = self._aho_corasick_match(input_text, start=start)
        elif self.algorithm == "naive":
            matches = self._naive_match(input_text, start=start)
        return matches


if __name__ == "__main__":
    words = ["hallo", "lol"]
    text = "hallol"
    s = StringMatching("naive", words)
    print(s.match_pattern(text))
    s = StringMatching("aho-corasick", words)
    print(s.fail)
    print(s.match_pattern(text))
