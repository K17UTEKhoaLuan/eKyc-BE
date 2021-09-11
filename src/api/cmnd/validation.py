from src.api.cmnd.documentScanner import scan_province
from src.utils.error_handle import Exception_Handle
import json
def validate_name(input_name, identity_name):
    list_input_name = input_name.split(" ")
    list_identity_name = identity_name.split(" ")
    if(len(list_input_name)!=len(list_identity_name)): 
        raise Exception_Handle(code=406, message="len input name not equal identity name")
    for index in range(len(list_identity_name)):
        if(list_input_name[index] not in list_identity_name[index]): 
            raise Exception_Handle(code=406, message="not equal name")
    return True

def validate_number_identity(input_number_identity, scaned_number_identity):
    if(str(input_number_identity)!=str(scaned_number_identity)):
        raise Exception_Handle(code=406, message="not equal identity number")
    return True

def validate_birthday(input_birthday, scaned_birthday):
    if(str(input_birthday)!=str(scaned_birthday)):
        raise Exception_Handle(code=406, message= "not equal birthday")
    return True

def validate_province_identity_number(scaned_number_identity, scaned_province):
    with open("data/cmnd.json") as cmnd_json:
        cmnd = json.load(cmnd_json)
    index = 0
    while(index < len(cmnd)):
        name_cmnd =(cmnd[index])["name"] 
        result = (str(name_cmnd) in str(scaned_province)) if (type(name_cmnd)==type("str")) else (scaned_province in set(name_cmnd))
        if not (result):
            index+=1
        else:
            print((cmnd[index])["name"])
            break
    if(index==len(cmnd)):
        raise Exception_Handle(code=404, message="not found province in list")
    if((cmnd[index])["code"]!=scaned_number_identity[0:2]):
        raise Exception_Handle(code= 406, message="not equal identity vs province")
    return True