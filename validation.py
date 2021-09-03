def validate_name(input_name, identity_name):
    list_input_name = input_name.split(" ")
    list_identity_name = identity_name.split(" ")
    if(len(list_input_name)!=len(list_identity_name)): return False
    for index in range(len(list_identity_name)):
        if(list_input_name[index] not in list_identity_name[index]): return False
    return True

