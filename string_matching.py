# -*- coding: utf-8 -*-
# Katja Konermann
# Matrikelnummer: 802658
"""
String Matching Classes:
    NaiveMatching - Uses naive algorithm when looking for keywords.
    AhoCorasickMatching - Uses algorithm described by Aho and Corasick.
"""


class NaiveMatching:

    """
    A class that represents string matching by using a naive
    algorithm.

    Attributes:
        keywords (set): Set of strings to search for.

    Methods:
        match_pattern(input_text, start=0):
            Find start indices of keywords in a string.
    """

    def __init__(self, keywords):
        """
        Constructs necessary attributes for String Matching Instance.

        Args:
            keywords (list): Iterable of strings to search for.

        Raises:
            ValueError:
                If an element is not a string or
                if the empty string "" is in the keywords.

        Returns:
            None.
        """
        self._keywords = set(keywords)

        try:
            assert all(isinstance(word, str) for word in self.keywords)
        except AssertionError:
            raise ValueError("Keywords must be strings.")

        if "" in self.keywords:
            raise ValueError("Invalid Keyword: "
                             "Can't match empty string.")

    @property
    def keywords(self):
        return self._keywords

    def match_pattern(self, input_text, start=0):
        """Returns the indices of self.keywords in a string.

        Given a text, find all indices where the instance's keywords begin.
        Optionally, existing matches can be updated
        and a start index can be defined. This should be used together, when
        matching in files for example.

        Args:
            input_text (str):
                A string to find instance's keywords in.
            start (int):
                Is added to index where keyword is found.
                The default is 0.

        Returns:
            dict:
                keys are the instance's keywords, values are lists
                of integers that indicate indices where the keyword
                starts in input_text
        """
        matches = dict()
        for word in self.keywords:
            for i in range(len(input_text)-len(word)+1):
                if word == input_text[i:i+len(word)]:
                    matches.setdefault(word, [])
                    matches[word].append(start+i)
        return matches


class AhoCorasickMatching(NaiveMatching):

    """
    A class that represents string matching by using the
    algorithm described by Aho and Corasick.

    Attributes:
        keywords (list): List of strings to search for.

    Methods:
        match_pattern(input_text, start=0):
            Find start indices of keywords in a string.
    """

    def __init__(self, keywords):
        super().__init__(keywords)
        self._part_goto = dict()
        self._output = dict()
        self._fail = dict()

        self.__construct_functions()

    def __construct_functions(self):
        """Determines goto, failure and output function.

        Functions are constructed according to Aho-Corasick Algorithm.

        Returns:
            None.
        """
        # Construct goto function and partial output function.
        newstate = 0
        for word in self.keywords:
            state = 0
            for char in word:
                # Transistion already in goto function.
                if state in self._part_goto and char in self._part_goto[state]:
                    state = self._goto(state, char)
                # New transition necessary.
                else:
                    newstate += 1
                    self._part_goto.setdefault(state, dict())
                    self._part_goto[state][char] = newstate
                    state = newstate
            # Last state of a keyword indicates that keyword is found.
            self._output.setdefault(state, set()).add(word)
        # Construct failure function and final output function.
        # sigma contains alphabet of keywords.
        sigma = {char for word in self.keywords for char in word}
        queue = []
        # Intializing queue.
        for char in sigma:
            out = self._goto(0, char)
            # States that can be reached from start state.
            if out is not False and out != 0:
                queue.append(out)
                self._fail[out] = 0
        while queue:
            # First state in queue.
            state = queue.pop(0)
            for char in sigma:
                if self._goto(state, char) is not False:
                    # Next states that can be reached from current state.
                    out = self._goto(state, char)
                    queue.append(out)
                    curr_state = self._fail[state]
                    # Determing fail function transition.
                    # while loop will always terminate because
                    # for state 0 goto function is never False.
                    while self._goto(curr_state, char) is False:
                        curr_state = self._fail[curr_state]
                    self._fail[out] = self._goto(curr_state, char)
                    output = self._output.get(out, set())
                    # Only add output when failure transition state
                    # actually has output.
                    fail_out = self._fail[out]
                    if fail_out in self._output:
                        self._output[out] = output.union(self._output[fail_out])

    def _goto(self, state, char):
        """ Implementation of the goto function described by Aho and Corasick.

        For a state and a character, returns a state if transition is possible.
        Otherwise returns False. An exception to this is the start state 0.
        When a transition from start state is not possible, returns 0.

        Args:
            state (int):
                An integer indicating a state.
            char (str):
                A single character.

        Returns:
            An Integer indicating a state if transition is possible,
            False otherwise.
        """
        if state in self._part_goto:
            # Transitions from start state don't fail.
            if state == 0 and char not in self._part_goto[state]:
                return 0
            elif char in self._part_goto[state]:
                return self._part_goto[state][char]
        return False

    def match_pattern(self, input_text, start=0):
        matches = dict()
        state = 0
        for i, char in enumerate(input_text):
            # Find possible transition.
            while self._goto(state, char) is False:
                state = self._fail[state]
            state = self._goto(state, char)
            # Save index if state is in output.
            if state in self._output:
                for out in self._output[state]:
                    matches.setdefault(out, [])
                    # Find start index by subtracting length of keyword.
                    matches[out].append(start+i-len(out)+1)
        return matches
