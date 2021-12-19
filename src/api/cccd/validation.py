from src.utils.error_handle import Exception_Handle
import json
from datetime import datetime


def validate_release_date(birthdate):
    current_date = datetime.now().date()
    release_years = [200, 60, 40, 25]
    birthdate = datetime.fromisoformat(birthdate).date()
    for year in release_years:
        release_date = birthdate.replace(
            year=birthdate.year+year)
        if current_date > release_date:
            raise Exception_Handle(name=__name__, step=2,
                                   code=200,
                                   field="backside",
                                   result=False,
                                   message="identity expired")

    return True


def validate_sex(cccd):
    with open("data/sex.json") as sex_json:
        sex = json.load(sex_json)
    cccd_sex = cccd.sex
    cccd_sex_code = cccd.identityNumber[3]
    # cccd_year = int(datetime.fromisoformat(
    #     cccd.birthday).date().strftime("%Y"))
    cccd_year = int(cccd.birthday[0:4])
    for item in sex:
        if(int(item["fromDate"]) <= cccd_year <= (int(item["endDate"])) and item["sex"] == cccd_sex):
            if(int(item["id"]) != int(cccd_sex_code)):
                raise Exception_Handle(name=__name__, step=2,
                                       code=200,
                                       field="frontside",
                                       result=False,
                                       message="sex fail")
    return True


def validate_province_identity_number(cccd):
    with open("data/cccd.json") as cccd_json:
        cccd_data = json.load(cccd_json)
    cccd_code = cccd.code
    cccd_provice_code = cccd.identityNumber[0:3]
    for item in cccd_data:
        if(cccd_code == item["code"]):
            if(cccd_provice_code != item["cccdCode"]):
                raise Exception_Handle(name=__name__, step=2,
                                       code=200,
                                       field="frontside",
                                       result=False,
                                       message="province fail")
    return True


def validate_birthday(cccd):
    cccd_year = cccd.identityNumber[4:6]
    birthday_year = cccd.birthday[2:4]
    if(cccd_year != birthday_year):
        raise Exception_Handle(name=__name__, step=2,
                               code=200,
                               field="frontside",
                               result=False,
                               message="birthday fail")
    return True


def validate_identity_number(identityNumber):
    if(len(identityNumber) != 12):
        raise Exception_Handle(name=__name__, step=2,
                               code=200,
                               field="frontside",
                               result=False,
                               message="identityNumber fail")
    return True
