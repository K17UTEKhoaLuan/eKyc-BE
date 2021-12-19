import json


def getProvince():
  with open("data/province.json") as province_json:
    province = json.load(province_json)
  return province