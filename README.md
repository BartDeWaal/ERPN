# ERPN
*An RPN  calculator written in Python*

**This is not yet ready for use**
Keyboard shortcuts, layout and other major interface changes will still be made
without remorse.

The goal is to create a calculator that has a much easier and more usable
interface for "live" use than dc.

It's keyboard based, for fast use.

There is always a quick reference of the availble functions, so you can use it
for tasks you don't do every day.

It has strong undo functions and a clear overview of what is going on, so you
don't lose time on typos and mistakes.

## Instalation on Linux
This will install erpn for the current user only.

Make sure `$/.local/bin/` is in your PATH.
Run `pip install --user erpn`

## Instructions
If you don't know what an RPN calculator is, you will probably need to find
that out first. You can find a tutorial here:
<http://linuxfocus.org/~guido/hp_calc/handbooks/rpn-tutorial.html>

This calculator only uses floating point numbers. This means there is a limit
to how precise a number can be, and also how large or small it can be. The
program will show an error if you try to go out of bounds.

To start number entry, simply start entering it using `0`-`9` or `.`.

To enter a negative number, you can start entry with an underscore (`_`). This
will be converted to a "-" in the interface.

You can enter a number with an exponent. So for example

Some of the keys in the sidebar as listed "meta" something. Some people call
that key "Alt" instead.

You can move a marker up and down using the arrows (or the `j` and `k` keys).
You can then use `enter` or space to copy that value to the end of the stack,
or you can run any function to first copy the selected item to the end of the
stack and then run the function. With `x` you can remove the item from the
stack.

`meta p` and `meta e` are used to enter pi (3.14...) and e (eulers constant,
2.718...) onto the stack.

### Display options
Using `D` you can enter the display menu.
You can exit it by pressing `D` again, or by pressing `enter`.

There are a few options for display modes here.

**Default display** (`d`) tries to show the number without an exponent. It only
displays an exponent when it needs to, either because the number can't be
accurataly displayed without an exponent or because it would be too long.

**Scientific Format** (`s`) always shows an exponent, so you could have `1e2`.

**Engineering Format** (`e`) is the same as scientific format, except the
exponent is always a multiple of 3. So for example `100e6`.

**No Exponent** (`p`) Never show an exponent. Example: `0.000`.

You can change the precision usin `+` and `-`.

## Development Setup on Linux
Clone the repository into a directory.
```bash
git clone https://github.com/BartDeWaal/ERPN.git
cd ERPN
```

Create a virtual environment with `pyvenv venv` or (for python 3.6 and up)
`python3 -m venv venv`.

Load it into your environment, the methed deponds on your shell. For bash it's `source venv/bin/activate`

Now install the package into the venv, using the "develop" command so you don't need to reinstall to apply changes
```bash
python setup.py develop
```

Now you can run it using the command `erpn`

## Licence
GPLv3
