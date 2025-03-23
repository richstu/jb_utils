#!/usr/bin/env python
import sys

def ask_key(question, valids, default=None):
  if sys.version_info[0] >= 3:
    answer = input(question)
  else:
    answer = raw_input(question)
  if '' not in valids: valids.append('')
  if answer not in valids:
    print('[Error] Did not enter valid key: '+', '.join(valids))
    return ask_key(question, valids, default)
  if answer == '': 
    if default == None:
      print('[Error] Did not enter valid key: '+', '.join(valids))
      return ask_key(question, valids, default)
    else:
      return default
  return answer

def ask_yn(question, default=None):
  return ask_key(question, ['y','n'], default)

