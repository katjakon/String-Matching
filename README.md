# String-Matching

A command-line program that finds the start indices of a set of keywords in a string, file or directory.<br>
By default, this program uses the string matching algorithm described by Aho and Corasick (1975).

## Requirements
Written with Python 3.8.5

## Installation
Download this repository to your local machine and unzip it.

## Usage

In your terminal, navigate into the _String-Matching_ directory. If you want to search in a file or in a directory, also move these here.<br>
For all commands and functionalities described below, run _main.py_.

### Match in a String
``
search <input text> <keyword> (<keyword> ...)
``
Type `search` to indicate you want to search for keywords. After the _search_ command follows the text you want to search in. If the text contains whitespace, make sure to wrap it in quotes.<br>
Put the words you want to search for after the input text. There needs to be at least one keyword but you can put more in. Keywords are seperated by a space. Again, if your keyword contains whitespace, wrapt it in quotes.<br>

### Match in a File
``
search <input.txt> <keyword> (<keyword> ...)
``
Same as above but put the name of the file after the _search_ command.
> This program only reads from text files. If your file name doesn't end with `.txt`, the program will treat this as a normal input text.

### Match in a Directory
``
search <input/> <keyword> (<keyword> ...)
``
Same as above but put the name of the directory followed by a slash or a backslash after the _search_ command. 
> As this program only reads from text files, any file that doesn't end with `.txt` will be ignored.

### Options
#### 