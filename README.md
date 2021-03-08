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

Use `search` as a command-line argument to indicate you want to search for keywords. After the _search_ command follows the text you want to search in. If the text contains whitespace, make sure to wrap it in quotes.<br>
Put the words you want to search for after the input text. There needs to be at least one keyword but you can put more in. Keywords are seperated by a space. Again, if your keyword contains whitespace, wrap it in quotes.<br>

### Match in a File
``
search <input.txt> <keyword> (<keyword> ...)
``

Same as above but put the path to the the file after the _search_ command. The program will then look for matches in that file. By default, this will tell you the absolute indices of the keywords in the content of the file, including any whitespace at the end of a line and end-of-line characters.

__Note:__ This program only reads from text files. If your file name doesn't end with `.txt`, the program will treat it as a normal input text.


### Match in a Directory
``
search <input/> <keyword> (<keyword> ...)
``

Same as above but put the name of the directory followed by a slash or a backslash after the _search_ command.<br>
This causes the program to search all files in the given directory for matches.

__Note:__ this program only reads from text files, any file that doesn't end with `.txt` will be ignored.

### Options
+ `-h`: Get a help message.
+ `-i`: Ignore case when looking for matches.
+ `-n`: Use the naive matching algorithm.
+ `-v`: Get more verbose output when matching in files. This will tell you the line and the index in that line when a match is found.

## Demo and Examples
Use`demo` as a command-line argument when running _main.py_ to get some more example inputs and outputs.

Command-line arguments:<br>
```search "She saw her." "he" ```

Output:<br>
```he: 1,8```

Command-line arguments:<br>
```search -i "She saw her." "she"```

Output:<br>
```she: 0```

Command-line arguments:<br>
```search demo/demo1.txt "she" "he" "his" "her"```

Output:<br>
```he: 81,70,7,2
she: 80,1
her: 70,2
his: 84,15```

## Additional Info
If the text you want to search in ends with `.txt`, `\` or `/`, put it in a file instead of giving it directly as an argument. Otherwise the program will try to match in a file or a directory, likely causing an error message.

## Author
Katja Konermann<br>
Martikelnummer: 802658<br>
<br>
Ein Projekt für das Seminar _Programmierung I_ im Wintersemester 20/21.
