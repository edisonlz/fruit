# -*- coding: utf-8 -*-


def convert_user_reg(user):
    return {
        "status": "success",
        "uid": user.id,
        "nickname": user.nick or ""
    }


def convert_user_login(user):
    return {
        "status": "success",
        "uid": user.id,
        "nickname": user.nick or ""
    }

def convert_user(user):
    return {
        "status":"success",
        "uid":user.id,
    }