#!/usr/bin/python3
"""
The `deploy` function creates a compressed archive file of the
`web_static` folder and saves it in the `versions` for deployment
"""
from datetime import datetime
import os
from fabric.api import *
env.hosts = ['52.201.220.122', '54.90.60.221']


def do_clean(number=0):
    """
    The `do_clean` function cleans up old versions of a
    web application and moves the most recent
    versions to a shared directory.
    """
    created_at = []
    for i in os.listdir("versions"):
        times = datetime.fromtimestamp(os.stat("versions/" + i).st_ctime)
        created_at.append(times)
    created_at = sorted(created_at)
    created_at = created_at[len(created_at) - 2:len(created_at)]
    # print(type(number))
    if int(number) == 0 or int(number) == 1:
        created_at = [created_at[-1]]
    # print(created_at)
    for i in os.listdir("versions"):
        times = datetime.fromtimestamp(os.stat("versions/" + i).st_ctime)
        if times not in created_at:
            local("rm versions/{}".format(i))
            # print(i)
    names = []
    for i in created_at:
        names.append("web_static_" + str(i.year) + str(i.month) +
                     str(i.day) + str(i.hour) + str(i.minute) +
                     str(i.second))
    run("cd /data/web_static/releases/")
    try:
        sudo("mv /data/web_static/releases/test /data/web_static/shared/")
        sudo("mv /data/web_static/releases/{}\
             /data/web_static/shared/".format(names[0]))
        sudo("mv /data/web_static/releases/{}\
             /data/web_static/shared/".format(names[1]))
        if len(names) > 1:
            sudo("rm -r /data/web_static/releases/*")
        # sudo("mkdir /data/web_static/releases/")
        # sudo("chown ubuntu:ubuntu releases")
        sudo("mv /data/web_static/shared/* /data/web_static/releases")
    except IndexError:
        if len(names) > 1:
            sudo("rm -r /data/web_static/releases/*")
        sudo("mv /data/web_static/shared/* /data/web_static/releases")
    # print(list_files)
    # print(names[0])
