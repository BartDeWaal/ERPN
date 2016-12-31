# CRPN
*A curses based calculator written in Python*

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

## Instructions
To enter a negative number, you can start entry with an underscore ("_"). This
will be converted to a "-" in the interface.

Commands that are listed as starting with ! mean to combine with alt. So for
example "!m" means alt-m.

## Todo
### Short term
 * Rethink all keyboard shortcuts
 * Add log window (like emacs has)
 * Add way more functions
 * Change display settings
 * Make real documentation
 * Add Redo functions

### Longer term
 * Complex numbers
 * Multiple stacks, including the option to apply commands to more than one
   stack at the same time
 * Save and load stacks
 * Variables
 * Functions
 * Custom key bindings
 * Customizable interface
 * Lists as objects
 * Reference (Stuff like common formulas)
 * GUI interface
 * Go back and edit history, redoing all the calculations that came after that
 * Units of measurement support

## Licence
GPL-3

pyperclip used under BSD licence
