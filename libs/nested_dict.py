import json
import sys
if sys.version_info[0] >= 3:
  unicode = str


def fill_dict(target_dict, key, item):
  if key not in target_dict:
    target_dict[key] = item
  else:
    if target_dict[key] != item:
      print('[Error] fill_dict: target_dict['+key+']:'+target_dict[key]+' is different with item:'+item)

def fill_nested_dict(target_dict, keys, item):
  if len(keys) == 0:
    print ('[Error] fill_nested_dict: keys:'+str(keys)+' length is 0.')
  elif len(keys) != 1:
    if keys[0] not in target_dict:
      target_dict[keys[0]] = {}
    fill_nested_dict(target_dict[keys[0]], keys[1:], item)
  else:
    fill_dict(target_dict, keys[0], item)

def fill_empty_nested_dict(target_dict, keys):
  keys.append(None)
  fill_nested_dict(target_dict, keys, {})

def get_item_nested_dict(target_dict, keys):
  if len(keys) == 1:
    return target_dict[keys[0]]
  return get_item_nested_dict(target_dict[keys[0]], keys[1:])

def get_nested_dict(target_dict, keys):
  out_dict = {}
  if is_nested_dict(target_dict, keys):
    fill_nested_dict(out_dict, keys, get_item_nested_dict(target_dict, keys))
  return out_dict

def get_from_nested_dict(target_dict, target_key):
  if isinstance(target_dict, dict):
    if target_key in target_dict:
      return target_dict[target_key]
    else:
      for key in target_dict:
        target_item = get_from_nested_dict(target_dict[key], target_key)
        if target_item != None:
          return target_item
  else: return None

def remove_key_nested_dict(target_dict, target_key):
  if isinstance(target_dict, dict):
    if target_key in target_dict:
      target_dict.pop(target_key)
    for key in target_dict:
      remove_key_nested_dict(target_dict[key], target_key)
  remove_empty_nested_dict(target_dict)

def remove_empty_nested_dict(target_dict):
  if not isinstance(target_dict, dict): return
  empty_dict_keys = []
  for key in target_dict:
    remove_empty_nested_dict(target_dict[key])
    # Remove empty dict
    if isinstance(target_dict[key], dict):
      if len(target_dict[key]) == 0:
        empty_dict_keys.append(key)
  # Remove empty dict
  for remove_key in empty_dict_keys:
    del target_dict[remove_key]

def remove_keys_nested_dict(target_dict, keys):
  if not isinstance(target_dict, dict): return
  if len(keys) == 0:
    print ('[Error] remove_keys_nested_dict: keys:'+str(keys)+' length is 0.')
  elif len(keys) != 1:
    if keys[0] in target_dict:
      remove_keys_nested_dict(target_dict[keys[0]], keys[1:])
  else:
    if keys[0] in target_dict:
      del target_dict[keys[0]]
  remove_empty_nested_dict(target_dict)

def check_key_nested_dict(target_dict, target_key):
  if isinstance(target_dict, dict):
    if target_key in target_dict:
      print(target_key+' is in target_dict')
    for key in target_dict:
      check_key_nested_dict(target_dict[key], target_key)

def is_nested_dict(target_dict, keys):
  if len(keys) == 0:
    print ('[Error] is_nested_dict: keys:'+str(keys)+' length is 0.')
  elif len(keys) != 1:
    #print(str(keys)+' len!=1')
    if keys[0] not in target_dict:
      #print(str(keys[0])+' keys not in target_dict len!=1')
      return False
    return is_nested_dict(target_dict[keys[0]], keys[1:])
  else:
    #print(str(keys)+','+str(target_dict)+' len==1')
    if keys[0] not in target_dict:
      #print(str(keys[0])+' keys not in target_dict len==1')
      return False
    else:
      #print(target_dict)
      #print(str(keys[0])+' in target_dict len==1')
      return True

def save_json_file(dict_name, json_filename):
  with open(json_filename,'w') as json_file:
    json.dump(dict_name, json_file, indent=2)
  print('Saved '+json_filename)

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii') if isinstance(x, unicode) else x
    return dict(map(ascii_encode, pair) for pair in data.items())

def convert_to_ascii(out_dict):
  if isinstance(out_dict, list):
    for key, value in enumerate(out_dict):
      if isinstance(value, unicode): out_dict[key] = value.encode('ascii') 
      if isinstance(value, (list, dict)): convert_to_ascii(out_dict[key])
  elif isinstance(out_dict, dict):
    for key in out_dict:
      value = out_dict[key]
      if isinstance(value, unicode): out_dict[key] = value.encode('ascii') 
      if isinstance(value, (list, dict)): convert_to_ascii(out_dict[key])
  elif isinstance(out_dict, unicode): out_dict = value.encode('ascii') 

def load_json_file(json_filename, no_null=True):
  with open(json_filename) as json_file:
    out_dict = json.load(json_file, object_hook=ascii_encode_dict)
  #nested_dict.check_key_nested_dict(out_dict, 'null')
  convert_to_ascii(out_dict)
  if no_null:
    remove_key_nested_dict(out_dict, 'null')
    check_key_nested_dict(out_dict, 'null')
    check_key_nested_dict(out_dict, None)
  return out_dict

