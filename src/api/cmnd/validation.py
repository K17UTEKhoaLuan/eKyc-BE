from src.utils.error_handle import Exception_Handle
import json
import datetime


def validate_name(input_name, identity_name):
    list_input_name = input_name.split(" ")
    list_identity_name = identity_name.split(" ")
    if(len(list_input_name) != len(list_identity_name)):
        raise Exception_Handle(name=__name__, step=2,
                               code=200,
                               field="name",
                               result=False,
                               message="len input name not equal identity name")
    for index in range(len(list_identity_name)):
        if(list_input_name[index] not in list_identity_name[index]):
            raise Exception_Handle(name=__name__, step=2,
                                   code=200,
                                   field="name",
                                   result=False,
                                   message="not equal name")
    return True


def validate_name2(input_name, identity_name):
    list_input_name = input_name.upper().split(" ")
    list_identity_name = identity_name.upper().split(" ")
    result = all(value in list_identity_name for value in list_input_name)
    if not result:
        raise Exception_Handle(name=__name__, step=2,
                               code=200,
                               field="name",
                               result=False,
                               message="not equal name")
    return True


def validate_number_identity(input_number_identity, scaned_number_identity):
    if(str(input_number_identity) != str(scaned_number_identity)):
        raise Exception_Handle(name=__name__, step=2,
                               code=200,
                               field="identityNumber",
                               result=False,
                               message="not equal identity number")
    return True


def validate_birthday(input_birthday, scaned_birthday):
    if(str(input_birthday) != str(scaned_birthday)):
        raise Exception_Handle(name=__name__, step=2,
                               code=200,
                               field="birthday",
                               result=False,
                               message="not equal birthday")
    return True


def validate_province_identity_number(scaned_number_identity, scaned_province):
    with open("data/cmnd.json") as cmnd_json:
        cmnd = json.load(cmnd_json)
    index = 0
    while(index < len(cmnd)):
        name_cmnd = (cmnd[index])["name"]
        success = False
        for string_province in scaned_province:
            result = (name_cmnd == string_province[1]) if (
                type(name_cmnd) is str) else (string_province[1] in set(name_cmnd))
            if (result):
                success = True
                break
        if not (success):
            index += 1
        else:
            print((cmnd[index])["name"])
            # index = len(cmnd)
            break
    if(index == len(cmnd)):
        raise Exception_Handle(name=__name__, step=2,
                               code=200,
                               field="backside",
                               result=False,
                               message="not found province in list")
    code_cmnd = (cmnd[index])["code"]
    result = (code_cmnd == scaned_number_identity[0:2]) if type(
        code_cmnd) is str else (scaned_number_identity[0:3] in set(code_cmnd))
    if not(result):
        raise Exception_Handle(name=__name__, step=2,
                               code=200,
                               field="backside",
                               result=False,
                               message="not equal identity vs province")
    return True


def validate_province_identity_number2(scaned_number_identity, scaned_province):
    with open("data/cmnd.json") as cmnd_json:
        cmnd = json.load(cmnd_json)
    province = None
    for data in cmnd:
        code_cmnd = data["code"]
        result = (code_cmnd == scaned_number_identity[0:2]) if type(
            code_cmnd) is str else (scaned_number_identity[0:3] in set(code_cmnd))
        if (result):
            province = data["name"]
            break
    if not (province):
        raise Exception_Handle(name=__name__, step=2,
                               code=200,
                               field="backside",
                               result=False,
                               message="not equal identity vs province")
    list_string = ""
    for string_province in scaned_province:
        list_string += string_province[1]+" "

    province = (str(province).lower()).split(" ")
    list_string = (list_string.lower()).split(" ")
    print(province)
    print(list_string)
    result = all(value in list_string for value in province)
    if not result:
        raise Exception_Handle(name=__name__, step=2,
                               code=200,
                               field="backside",
                               result=False,
                               message="not found province in list")
    return True


def validate_release_date(scaned_release_date):
    now = datetime.datetime.now()
    year = now.year
    if not(scaned_release_date.isnumeric()):
        raise Exception_Handle(name=__name__, step=2,
                               code=200,
                               field="backside",
                               result=False,
                               message="date is not number")
    if (int(year)-int(scaned_release_date)) > 15:
        raise Exception_Handle(name=__name__, step=2,
                               code=200,
                               field="backside",
                               result=False,
                               message="identity expired")
    return True
