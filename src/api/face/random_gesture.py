from random import randint
import json
from os import path
import os
import shutil
from src.utils.error_handle import Exception_Handle


def add_id_to_list(saved_pose_data):
    list_id = []
    for index in range(1, len(saved_pose_data)-1):
        list_id.append(saved_pose_data[index]["id"])
    return list_id


def random_face_gesture(identity_number):
    with open("data/pose.json") as pose_json:
        pose_data = json.load(pose_json)
        pose_json.close()
    random_index = randint(0, len(pose_data))
    print("random_index", random_index)
    # save_json = [{"id": pose_data[random_index]["id"],"pose":pose_data[random_index]["pose"]}]
    save_json = []
    times = {"times": randint(3, 5)}
    save_json.append(times)
    save_json.append(pose_data[random_index])

    if(path.exists("savedata/gesture/{}.json".format(identity_number))):
        os.remove("savedata/gesture/{}.json".format(identity_number))

    # os.mkdir("savedata/gesture/{}.json".format(identity_number))
    with open("savedata/gesture/{}.json".format(identity_number), "x") as file:
        file.write(json.dumps(save_json))
        file.close()

    return pose_data[random_index]["id"], pose_data[random_index]["pose"]


def next_gesture(identity_number):
    if(path.exists("savedata/gesture/{}.json".format(identity_number))):
        with open("savedata/gesture/{}.json".format(identity_number)) as file_json:
            saved_pose_data = json.load(file_json)
            file_json.close()
        with open("data/pose.json") as pose_json:
            pose_data = json.load(pose_json)
            pose_json.close()

        times = saved_pose_data[0]["times"]
        if(times == len(saved_pose_data)-1): return True, None, None
        if(times > len(saved_pose_data)-1):
            list_pose_completed = add_id_to_list(saved_pose_data)
            print(list_pose_completed)
            random_index = randint(0, len(saved_pose_data))
            while random_index in list_pose_completed:
                random_index = randint(0, len(saved_pose_data))

            saved_pose_data.append(pose_data[random_index])

            with open("savedata/gesture/{}.json".format(identity_number), "w") as file_json:
                file_json.write(json.dumps(saved_pose_data))
                file_json.close()
            # completed = True if(times == len(saved_pose_data)-1) else False
            return False,pose_data[random_index]["id"], pose_data[random_index]["pose"]
        else:
            raise Exception_Handle(
                code=200,
                message="index exceeding times",
                result=False,
                field="times",
                step=3
            )
    else:
        raise Exception_Handle(
            code=200,
            result=False,
            message="file json not found",
            step=3,
            field="json"
        )
