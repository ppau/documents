# Pirate Party Australia Official Documents

## Constitution

### Generate as PDF

To compile the Constitution, you need to have installed a `xelatex` compiler, which comes with TeX Live and other package sets.

Then run: `xelatex constitution.tex` twice and open the resulting PDF file.

### Generate as HTML

Requires Python 3, with `lxml` and `roman` packages (see below).

Run: `python3 convert_tex_to_html.py > file.html` and open the resulting HTML file.

## convert_tex_to_html.py

Script options:

- `-F`, `--final` - removes draft markings.
- `-d yyyy-mm-dd`, `--date` - changes the default date (today) to whatever is specified.
- `-f document.tex`, `--file` - changes the default input TeX file (constitution.tex) to whatever is specified.
- `-T Title\ Goes\ Here`, `--title` - defines the title (if empty, prints blank).
- `-P`, `--parts` - used for documents with parts (numbered with Roman numerals).

Example: `python3 convert_tex_to_html.py > output.html -f input.tex -T Title -P`

This will make output.html from input.tex, the contents will be titled 'Title', and it will have part numbering.

The input TeX file can be very basic and does not need a preamble:

```
\part{Part i}

\section{Section 1}

\begin{enumerate}
  \item Item (1)
  \item Item (2)
  \item Item (3)
\end{enumerate}
```

Note that `\part` must be present in the TeX document (at least for now) regardless of whether it actually has parts; this can be an empty `\part{}` if parts are not intended to be used.

## build_all_draft.sh and build_all_final.sh

For convenience, two bash scripts are provided to compile multiple documents.

Put documents that are divided into parts into a subdirectory called `part` and documents that are divided into sections into a subdirectory called `section`. Files must use the Mediawiki syntax and must have the extension `.wik`.

The file name is taken from the file name of the .wik file, and the title of the document is taken from the first line of the .wik file.

`example_document.wik` with the contents

```
Document Title

=Heading Level 1=

Body.

==Heading Level 2==

* Unordered list item

===Heading Level 3===

# Ordered list item

```

will produce `example_document.html`

## Setting up on OS X

This works for getting the Python script running in OS X El Capitan (10.11.6). More efficient/appropriate steps may exist, but this _worked_.

1. Install [TeX](http://tug.org/mactex/).
2. Install [Python 3](https://www.python.org/downloads/).
3. Launch Terminal.
4. Install [Homebrew](http://brew.sh)
5. Install [Pandoc](https://github.com/jgm/pandoc/releases/tag/1.17.2) with `brew install pandoc`.
6. Install [Libxml2](http://xmlsoft.org/index.html) with `brew install libxml2`.
7. Install [Libxslt](http://xmlsoft.org/libxslt/) with `brew install libxslt`.
8. Run `link libxml2 --force`.
9. Run `link libxslt --force`.
10. Install [lxml](http://lxml.de) with `pip install lxml`.
11. Install [Roman](https://pypi.python.org/pypi/roman) with `pip install Roman`.
12. Install [cssselect](https://pypi.python.org/pypi/cssselect) with `pip install cssselect`.
