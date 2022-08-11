# Introduction
The main file `GapToTex.py` in this directory is used to produce `.tex` files of example GAP sessions.

# Instructions
Run `python GapToTex.py [GAP]` from this directory, where the optional argument `[GAP]` should be the path to a GAP installation. The argument `GAP` is set to `'/bin/gap.sh'` by default.

All files in the directory `in/` need to be readable GAP files that do not cause any break loops.
We advise to use at most 80 characters per line in order to prevent overfloats in the `.tex` files.

The `out/` directory will contain all `.tex` files generated from the files in `in/`.
The `out/` directory is <ins>**not**</ins> cleaned automatically by the script.

To compile the `.tex` files, you need the header from `Preamble.tex` in your document.

# Example

We include an example file called `example.g` in the `in/` directory
and an example dependency called `dependency.g` in the `lib/` directory.
You may run the script and insert `\input{out/example.tex}` into the document body of `Preamble.tex` if you wish to test out the LaTeX compilation.

# Troubleshooting

If you have configured your GAP installation to load additional packages, etc.
this might result in additional output on startup.
In order to prevent the script from breaking
and producing wrong (or no) output in such a case,
you can adjust the parameter `DELAY` in `GapToTex.py` to your needs.
The parameter is set to `0` by default.

## Dependencies
- GAP
- python3
- python3 packages:
    - signal

## License

GapToTex is free software you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version. For details, see the file LICENSE distributed as part of this package or see the FSF's own site.
