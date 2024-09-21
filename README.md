# dev_calc
dev_calc is a command-line calculator inspired by the Windows Developer Calculator. It provides advanced mathematical functions and is designed for developers who prefer using the terminal for calculations.

## Features
Basic arithmetic operations: addition, subtraction, multiplication, and division
Programmer mode: binary, hexadecimal, and octal calculations
History of calculations
Easy-to-use command-line interface
Installation
Install dev_calc using pip:
```bash
pip install dev_calc
```
Usage
To use dev_calc, simply call it from your terminal:

`dev_calc`
Keybindings
q: Quit the application
k: Switch to the previous mode (DEC, BIN, HEX, OCT)
j: Switch to the next mode (DEC, BIN, HEX, OCT)
c: Clear the current input
Backspace: Delete the last character
Enter: Solve the current expression

## Examples
### Basic arithmetic:

Start the calculator:
dev_calc
Enter the expression 3 + 4 in DEC mode and press Enter.
```
[DEC]:  3 + 4 
BIN:    0011 + 0100 
HEX:    3 + 4 
OCT:    3 + 4 
--------------------
q: quit, k: previous, j: next, c: clear
```
```
[DEC]:  7 
BIN:    0111 
HEX:    7 
OCT:    7 
--------------------
q: quit, k: previous, j: next, c: clear
```


### Switching modes:

DEC: Decimal (base 10)

BIN: Binary (base 2)

HEX: Hexadecimal (base 16)

OCT: Octal (base 8)

You can switch between these modes using the k and j keys.

### Debug Mode
To run dev_calc in debug mode, use the -d flag:

dev_calc -d
This will print debug information to the terminal.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.