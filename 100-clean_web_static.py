#!/usr/bin/python3
# Fabfile to deletes out-of-date archives.
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run
from fabric.api import cd

env.hosts = ["54.87.171.248", "54.226.5.216"]


def do_clean(number=0):
    """ Deletes out of date archives
        Args:
            number: (int) as number of archives to keep
    """

    n = int(number)
    if n <= 1:
        n = 1
    files_str = local("ls -t versions", capture=True)
    files = files_str.split()
    for file in files[n:]:
        local("rm versions/{}".format(file))
    # clean server
    remote_files_str = run("ls -t /data/web_static/releases")
    remote_files = remote_files_str.split()
    for file in remote_files[n:]:
        run("rm -r /data/web_static/releases/{}".format(file))
