# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 12:12:37 2021

@author: HP I5
"""


class CommandLineInput:

    COMMANDS = ("suche", "speicher", "demo")
    OPTIONS = ("-i", "-n", "-v")
    INPUT_EXT = (".txt")
    PATTERN_EXT = (".json")
    DIRS = ("\\", "/")

    def __init__(self, commands):
        self.commands = commands
        self.command = None
        self.pattern = None
        self.input_text = None
        self.options = []

    @property
    def pattern_from_file(self):
        if self.pattern.endswith(self.PATTERN_EXT):
            return True
        return False

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

    def parse_commands(self):
        if self.commands[0] not in self.COMMANDS:
            raise ValueError("Invalid command '{}'.".format(self.commands[0]))
        self.command = self.commands[0]
        for i in range(1, len(self.commands)):
            if not self.commands[i].startswith("-"):
                break
            if self.commands[i] not in self.OPTIONS:
                raise ValueError("Unknown option: {}".format(self.commands[i]))
            self.options.append(self.commands[i])
        self.pattern = self.commands[i]
        self.input_text = self.commands[i+1]

if __name__ == "__main__":
    c = ["suche", "wedc.json", "wlek/"]
    i = CommandLineInput(c)
    i.parse_commands()
    print(i.command)
    print(i.pattern)
