import json
import os
import pandas as pd
import numpy as np

def deal_with_lists(object):
  if len(object) == 0:
    return False
  lst_type = type(object[0])
  if (lst_type == int) or (lst_type == float):
    return True
  elif lst_type == str:
    return False
  elif lst_type == list:
    return deal_with_lists(object[0])
  else:
    print(f"more list types: {lst_type}")

def read_json_object(obj, stack):
  attribute_set = set()
  for elem in obj:
    stack.append(elem)
    stack_str = '.'.join(map(str,stack))
    object = obj[elem]
    obj_type = type(object)
    if obj_type == dict:
      attribute_set.update(read_json_object(obj[elem], stack))
    elif obj_type == str:
      pass # only using numerical values as features
    elif obj_type == bool:
      attribute_set.add(stack_str)
    elif obj_type == int:
      attribute_set.add(stack_str)
    elif obj_type == float:
      attribute_set.add(stack_str)
    elif obj_type == list:
      if deal_with_lists(object):
        attribute_set.add(stack_str)
      else:
        pass
    else:
      print(f"more object types: {obj_type}")
    stack.pop()
  return attribute_set

def list_2_dict(object):
  if len(object) == 0:
    return []
  lst_type = type(object[0]) # acousticbrainz has no empty lists and no lists with different types TODO: check this
  if (lst_type == int) or (lst_type == float) or (lst_type == bool):
    return [float(x) for x in object]
  elif lst_type == str:
    return []
  elif lst_type == list:
    complete_lst = []
    for lst in object:
      complete_lst.extend(list_2_dict(lst))
    return complete_lst
  else:
    print(f"more list types: {lst_type}")

def json_2_dict(obj, stack, attribute_dict):
  for elem in obj:
    stack.append(elem)
    stack_str = '.'.join(map(str,stack))
    object = obj[elem]
    obj_type = type(object)
    if obj_type == dict:
      json_2_dict(obj[elem], stack, attribute_dict)
    elif obj_type == str:
      pass # only using numerical values as features
    elif (obj_type == bool) or (obj_type == int) or (obj_type == float):
      if stack_str in attribute_dict:
        attribute_dict[stack_str] = float(object)
    elif obj_type == list:
      if stack_str in attribute_dict:
        arr = list_2_dict(object)
        if len(arr) == 0:
          pass
        else:
          attribute_dict[stack_str] = arr
          # print(stack_str, len(arr))
    else:
      print(f"more object types: {obj_type}")
    stack.pop()

if __name__ == "__main__":
  df = pd.read_csv("../data/disco-olga_complete.csv")[['artist_am-id', 'track_mb-id']]

  common_set = set()
  for idx, row in df.iterrows():
    filename = "../data/jsons/ab-low-level_disco-olga/" + row['track_mb-id'] + ".json"
    f = open(filename)
    data = json.load(f)
    stack = []
    attribute_set = read_json_object(data, stack)
    if len(common_set) == 0:
      common_set = attribute_set
    else:
      common_set = common_set.intersection(attribute_set)
    f.close()
  print(len(common_set))

  all_features = []
  for idx, row in df.iterrows():
    filename = "../data/jsons/ab-low-level_disco-olga/" + row['track_mb-id'] + ".json"
    f = open(filename)
    data = json.load(f)
    stack = []
    common_dict = dict.fromkeys(common_set, 0)
    json_2_dict(data, stack, common_dict)
    features_nested = list(common_dict.values())
    features = []
    for feature in features_nested:
      if isinstance(feature, list):
        for sub_feature in feature:
          features.append(sub_feature)
      else:
        features.append(feature)
    all_features.append(features)
    print(len(features))

  acousticbrainz_features = np.array(all_features)
  np.save('../data/disco-olga/acousticbrainz.npy', acousticbrainz_features)
