#!/usr/bin/env python3.8

import math
from stack import stack
from lexer import lexer, operand_codes
import maths
from signal import signal, SIGINT
from sys import exit


"""
Variables available for all processes in program
"""

stack_ = stack()
lex = lexer()

variable_map_ = {
    "variable": 10.0
}

def sigint_handler(signal_received, frame):
    exit(0)

def assign_value_(string: str):
  variable_ = string[1:]
  if(variable_.strip() in lex.keywords):
    print("cannot use {} as a variable name!".format(variable_))
    stack_.clear_contents()
  else:
    print("assigning {} with value of {}".format(string[1:], stack_.peek()))
    variable_map_[variable_] = stack_.peek()

def retrieve_value_(string: str):
  variable_ = string[1:]
  try:
      value_retrieved_ = variable_map_[variable_]
      stack_.push(value_retrieved_)
  except KeyError:
      print("cannot retrieve value of {}, it is not in the table".format(variable_))


def get_constant_(string: str):
    look_up_ = -1
    for i, element in enumerate(lex.constant_names_):
      if(element == string): 
        look_up_ = i
        break
    try:
      stack_.push(maths.constant_map_[look_up_])
    except KeyError:
      print("could not find constant: {}".format(string))
def math_operation_(string: str):
  try:
    # this is only for list operations
    multi_argument_code = lex.operand_map[string]
    contents_ = stack_.pop_n(2)
    try:
      stack_.push(maths.math_function(contents_, multi_argument_code))
    except TypeError as error:
      print("error value of: {}".format(error))
      print("invalid syntax: {}".format(string))
  except KeyError:
    value_ = [stack_.pop()]
    if(operand_codes.POW.value == lex.tokenize(string)):
      value_.append(stack_.pop())
    stack_.clear_contents()
    try:
      stack_.push(float(maths.math_function(value_, lex.tokenize(string))))
    except Exception as error:
      print("oops, got a math error ey there bud!: {}".format(error))


def rpn_calculator(expression: str) -> None:
  for chunk in expression.split():
    operand_code = lex.tokenize(chunk)
    if(operand_code == operand_codes.GARBAGE.value):
      print("got garbage with operand: {}".format(chunk))
    elif(operand_code == operand_codes.CONSTANT.value):
      get_constant_(chunk)

    elif(operand_code == operand_codes.NUMBER.value):
      stack_.push(float(chunk))

    elif(operand_code == operand_codes.ASSIGN.value):
      assign_value_(chunk)

    elif(operand_code == operand_codes.RETRIEVE.value):
      retrieve_value_(chunk)

    else:
      math_operation_(chunk)

def unit_test_():
  expression = "10 SIN\n18 9 *"
  for element in expression.split('\n'):
    print(">>> {}".format(element))
    rpn_calculator(element)

    if(not stack_.is_empty()):
      try: print("\t{0:.15f}".format(stack_.peek()))
      except IndexError: print("\tstack is empty")
    stack_.clear_contents()

signal(SIGINT, sigint_handler)

while(True):
  exp = input(">>> ")
  rpn_calculator(exp)
  if(not stack_.is_empty()):
    try: print("\t{0:.15f}".format(stack_.peek()))
    except IndexError: print("\tstack is empty")
  stack_.clear_contents()
