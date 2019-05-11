#!/usr/bin/python

#
# Brainfuck Interpreter
#

import sys


OPERATIONS_LIMIT = 1000

def execute(filename):
  f = open(filename, "r")
  evaluate(f.read())
  f.close()


def evaluate(code):
  code     = cleanup(list(code))
  bracemap = buildbracemap(code)

  cells, codeptr, cellptr = [0], 0, 0
  result = ""
  operations = 0

  if bracemap is None:
    return result

  while codeptr < len(code) and operations < OPERATIONS_LIMIT:
    command = code[codeptr]

    if command == ">":
      cellptr += 1
      if cellptr == len(cells): cells.append(0)

    if command == "<":
      cellptr = 0 if cellptr <= 0 else cellptr - 1

    if command == "+":
      cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

    if command == "-":
      cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

    if command == "[" and cells[cellptr] == 0 and codeptr in bracemap:
      codeptr = bracemap[codeptr]

    if command == "]" and cells[cellptr] != 0 and codeptr in bracemap:
      codeptr = bracemap[codeptr]

    if command == ".":
      result = result + chr(cells[cellptr])
    if command == ",":
      pass#cells[cellptr] = ord(getch.getch())
    codeptr += 1
    operations += 1
  return result

def cleanup(code):
  return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))

def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      if len(temp_bracestack) > 0:
        start = temp_bracestack.pop()
        bracemap[start] = position
        bracemap[position] = start
      else:
        return None
  return bracemap

def main():
  if len(sys.argv) == 2:
    execute(sys.argv[1])
  else: 
    print("Usage:", sys.argv[0], "filename")

if __name__ == "__main__": main()

