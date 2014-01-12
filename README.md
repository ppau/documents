# Pirate Party Australia Official Documents

## Constitution

### Generate as PDF

To compile the Constitution, you need to have installed a `xelatex` compiler, which comes with TeX Live and other package sets.

Then run: `xelatex constitution.tex` twice and open the resulting PDF file.

### Generate as HTML

Requires Python 3, with `lxml` and `roman` packages.

Run: `python3 convert_tex_to_html.py > file.html` and open the resulting HTML file.
