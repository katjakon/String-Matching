# -*- coding: utf-8 -*-
# Katja Konermann
# Matrikelnummer: 802658
"""
A class that handles the different modes of string matching programm.
"""
import os

from string_matching import NaiveMatching, AhoCorasickMatching


class Search:

    """
    A class that represents the user commands from the command line
    and handles the different modes of the string matching programm.

    Attributes:
        pattern (list):
            List of strings, the strings that should be searched for.
        input (str):
            A string, can be the name of a file or a dir where the text
            should be read from. To indicate a directory, use \\ or /.
            To indicate a file, use a valid file extension (from INPUT_EXT).
        insensitive (bool):
            Indicates case insensitive mode, where text from input and
            strings in pattern will be treated as lowercase. Default is False.
        naive (bool):
            Indicates use of the naive matching algorithm when searching
            in input. Default is False.
        verbose (bool):
            Indicates verbose output when matching in files. Default is
            False.

    Properties:
        input_from_file (bool):
            True if input ends with valid file extension,
            False otherwise
        input_from_dir (bool):
            True if input ends with \\ or /, False otherwise.


    Methods:
        run:
            Print indices of patterns in input
            according to instance's mode
        demo:
            Get a demo of different modes that can be used with
            examples and output.
    """

    INPUT_EXT = (".txt",)
    DIRS = ("\\", "/")
    DEMOS = ({"pattern": ["he"],
              "input_text": "She saw her."},
             {"pattern": ["she"],
              "input_text": "She saw her."},
             {"pattern": ["she"],
              "input_text": "She saw her.",
              "insensitive": True},
             {"pattern": ["her", "he"],
              "input_text": "She saw her."},
             {"pattern": ["she", "he", "his", "her"],
              "input_text": "She saw her.",
              "naive": True},
             {"pattern": ["she", "he", "his", "her"],
              "input_text": "demo/demo1.txt"},
             {"pattern": ["she", "he", "his", "her"],
              "input_text": "demo/demo1.txt",
              "verbose": True},
             {"pattern": ["she", "he", "his", "her"],
              "input_text": "demo/"}
             )

    def __init__(self,
                 pattern,
                 input_text,
                 insensitive=False,
                 verbose=False,
                 naive=False):
        self.pattern = pattern
        self.input = input_text
        self.insensitive = insensitive
        self.verbose = verbose
        self.naive = naive
        self._match = self._create_match()

    def __str__(self):
        """String representation of instance is command line input"""
        commands = "search "
        if self.insensitive:
            commands += "-i "
        if self.verbose:
            commands += "-v "
        if self.naive:
            commands += "-n "
        if self.input_from_dir or self.input_from_file:
            commands += "{} ".format(self.input)
        else:
            commands += '"{}" '.format(self.input)
        for pattern in self.pattern:
            commands += '"{}" '.format(pattern)
        return commands

    def _create_match(self):
        """Creates a string matching object according to instance's attribute.

        If self.i is True. strings in self.pattern will be converted to
        lowercase when creating matching object.

        Returns:
            NaiveMatching object if self.n is True,
            otherwise returns AhoCorasickMatching object.
        """
        if self.insensitive:
            self.pattern = [pattern.lower() for pattern in self.pattern]
        if self.naive:
            return NaiveMatching(self.pattern)
        return AhoCorasickMatching(self.pattern)

    @property
    def input_from_file(self):
        """Determines whether input text should be read from file.

        Returns:
            bool:
                If input ends with classes file extensions, returns True.
                Returns False otherwise.
        """
        if self.input.endswith(self.INPUT_EXT):
            return True
        return False

    @property
    def input_from_dir(self):
        """Determines whether input text should be read from directory.

        Returns:
            bool:
                If input ends with / or \\, returns True.
                Returns False otherwise.
        """
        if self.input.endswith(self.DIRS):
            return True
        return False

    @staticmethod
    def _print_matches(match_dict):
        """Prints found matches.

        Args:
            match_dict (dict):
                keys are strings, values are sets of integers.

        Returns:
            None.
        """
        if not match_dict:
            print("No matches found.")
        for match in match_dict:
            match_index = map(lambda x: str(x), match_dict[match])
            print("{}: {}".format(match, ",".join(match_index)))

    def update_matches(self, matches1, matches2):
        for match in matches1:
            if match in matches2:
                matches1[match] += matches2[match]
        return {**matches2, **matches1}

    def _match_in_file(self, file=None):
        """Finds matches for pattern in file and prints them.

        If verbose is True, prints index of matches in each line. Otherwise
        prints index in file content, counting EOL characters.

        Args:
            file (str):
                Name of a file. If default is used, it's assumed that
                text should be read from self.input.

        Returns:
            None.
        """
        if file is None:
            file = self.input
        with open(os.path.join(file), encoding="utf-8") as file_in:
            # Line count.
            count = 1
            # Index count.
            index = 0
            matches = dict()
            for line in file_in:
                # Case insensitive mode.
                if self.insensitive:
                    line = line.lower()
                # Verbose mode will match in each line individually.
                if self.verbose:
                    line_match = self._match.match_pattern(line)
                    if line_match:
                        # Save matches by line.
                        matches[count] = line_match
                else:
                    # If not verbose, we need to keep track of
                    # current index by using the start parameter
                    # of match_pattern method.
                    new_matches = self._match.match_pattern(line,
                                                            start=index)
                    # Update matches
                    matches = self.update_matches(new_matches, matches)
                index += len(line)
                count += 1
            # Print no matches or matches without lines.
            if not matches or not self.verbose:
                self._print_matches(matches)
            else:
                # Print matches for each line.
                for line in matches:
                    line_str = "Line {}".format(line)
                    print("{:-^30}".format(line_str))
                    self._print_matches(matches[line])

    def _match_in_dir(self):
        """Finds matches for pattern in directory and prints them.

        Will only try to match in files that end with extension defined
        in class variable EXT.

        Returns:
            None
        """
        files = [file for file in os.listdir(self.input)
                 if file.endswith(self.INPUT_EXT)]
        if files:
            for file in files:
                print("{:=^30}".format(file))
                path = os.path.join(self.input, file)
                self._match_in_file(path)
        else:
            print("No files with valid file extension found. "
                  "Valid file extensions: {}".format(",".join(self.INPUT_EXT)))

    def _match_in_str(self):
        """Matches pattern in string and prints them.

        Returns:
            None

        """
        if self.insensitive:
            self.input = self.input.lower()
        matches = self._match.match_pattern(self.input)
        self._print_matches(matches)

    def run(self):
        """
        Matches pattern in input (str, file or dir) and prints indices.

        Returns:
            None
        """
        if self.input_from_file:
            self._match_in_file()
        elif self.input_from_dir:
            self._match_in_dir()
        else:
            self._match_in_str()

    @classmethod
    def demo(cls):
        """Demo of different functionalities of Search class"""
        for demo in cls.DEMOS:
            search = cls(**demo)
            print("\tCall:")
            print(search)
            print("\tOutput:")
            search.run()
            print()


if __name__ == "__main__":
    s = Search.demo()