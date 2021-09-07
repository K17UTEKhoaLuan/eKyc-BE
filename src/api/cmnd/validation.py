from src.utils.error_handle import Exception_Handle

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