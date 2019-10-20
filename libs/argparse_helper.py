#!/usr/bin/env python
import argparse
def initialize_arguments(args, list_args):

  # Get rid non list_args
  for key in args:
    if key in list_args: continue
    if isinstance(args[key], list) and len(args[key])==1: 
      args[key] = args[key][0]

  #print(args)
  # Convert comma to list
  for key in args:
    if args[key] == None: continue
    if len(args[key]) != 1 : continue
    if key not in list_args: continue
    if "," in args[key][0]:
      args[key] = args[key][0].split(',')
      
  ## Convert to int
  #for key in args:
  #  if isinstance(args[key], list):
  #    for index, item in enumerate(args[key]):
  #      if unicode(item).isnumeric():
  #        args[key][index] = int(item)
  #  if isinstance(args[key], basestring):
  #    if unicode(args[key]).isnumeric():
  #      args[key] = int(args[key])

def set_default(args, key, value):
  if not args[key]:
    args[key] = value

def is_valid(args, key, valid_list):
  if isinstance(args[key], list):
    for item in args[key]:
      if item not in valid_list:
        return False
  if isinstance(args[key], basestring):
    if args[key] not in valid_list:
      return False
  return True
