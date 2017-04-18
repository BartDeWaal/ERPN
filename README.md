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

You can enter a number with an exponent. So for example `0.1e-4`.

Some of the keys in the sidebar as listed "meta" something. Some people call
that key "Alt" instead.

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

### Copy and Paste
#### Within the stack
To copy the top value in the stack use `space` or `enter`.

You can move a marker up and down using the arrows (or the `j` and `k` keys).
You can then use `enter` or `space` to copy that value to the end of the stack,
or you can run most functions to first copy the selected item to the end of the
stack and then run the function.

#### From the OS
You can copy to the OS (so you can use the results of your calculation
elsewhere) using the `c` button.
It will be formatted without regard to the current display settings.

To paste a value from the OS you use the `p` button.

### Functions
#### Addition
Bound to `+`. Calculates x+y.

If there is nothing in the stack, it will return a default value of 0.

#### Ceiling
Bound to `~`. Rounds x up to the first larger integer.

#### Delete
Bound to `x`. Removes item x from the stack.

If the arrow is pointing at something, delete that instead of item x.

#### Divide
Bound to `/`. Calculates y/x.

Dividing by 0 will result in an error, values like `inf` are not supported by
erpn.

#### Exponent
Bound to `p` (p for power). Calculates y^x.

#### Factorial
Bound to `!`. Calculates x!, i.e. x*(x-1)*(x-2)*...*2*1.

#### Floor
Bound to `` ` `` (backtick). Rounds x down to the first smaller integer.

#### GCD (Greatest common divisor)
Bound to `#`. Calculates the largest integer divisor of both x and y.

For example, the GCD of 8 and 12 is 4.

Is only defined on integer values.

#### Logaritm (base 10)
Bound to `l`. Calculates the 10-log of x.

#### Logaritm (Natural)
Bound to `L`. Calculates the natural logarithm of x.

#### Modulo
Bound to `%`. Calculates y mod x.

This also supports fractional modulo.

The sign of the result is the sign of x. So for example `-1 mod 2 = 1`, and
`1 mod -2 = -1`.

When used with the arrow, it calculates x mod arrow value.

#### Multiply
Bound to `*`. Calculates x*y.

If there is nothing in the stack, it will return a default value of 1.0.

#### Negative (additive inversion)
Bound to `i` (for invert). Calculates 0-x.

#### Invert (multiplicative)
Bound to `I`. Calculates 1/x.

#### Power of 10
Bound to `e` (e as used in scientific number notation). Calulates 10^x.

#### Power of e
Bound to `E`. Calulates e^x, where e is eulers constant (approx. 2.718).

#### Square
Bound to `s`. Calculates x*x.

#### Square root
Bound to `S`. Calculates sqrt(x).

#### Subtract
Bound to `-`. Calculates y-x.

#### Switch 2
Bound to tab. Swaps x and y.

If used with the arrow, switches the pointed at item with x.

#### Trigonomic functions
The most important trigonomic functions are also included.
These all work based on radians, and are not currently settable to degrees.

Sin is bound to `meta s`.  
Arcsin is bound to `meta S`.

Cos is bound to `meta c`.  
Arccos is bound to `meta C`.

Tan is bound to `meta t`.  
Arctan is bound to `meta T`.

## Development Setup on Linux
Clone the repository into a directory.
```bash
git clone https://github.com/BartDeWaal/ERPN.git
cd ERPN
```

Create a virtual environment with `pyvenv venv` or (for python 3.6 and up)
`python3 -m venv venv`.

Load it into your environment, the method depends on your shell. For bash it's `source venv/bin/activate`

Now install the package into the venv, using the "develop" command so you don't need to reinstall to apply changes
```bash
python setup.py develop
```

Now you can run it using the command `erpn`

## Licence
GPLv3
