#!/usr/bin/python3
"""This is fabric script to deploy data to servers """
import fabric
from fabric.api import *
from fabric.operations import run, put, local
env.hosts = [
    '54.226.5.216',
    '54.87.171.248'
]
# Set the username
env.user = "ubuntu"

# Set the password [NOT RECOMMENDED]
# env.password = "passwd"


def do_pack():
    """ function to pack data and then return path of result archive
    """

    # create version dir if doesn't exist
    fabric.operations.local('mkdir -p versions')

    # get date and time
    date_time = fabric.operations.local('date +"%Y%m%d%H%M%S"', capture=True)

    archive_name = "versions/web_static_{}.tgz".format(date_time)

    # compress data
    command = "tar -cvzf {} web_static".format(archive_name)
    print(command)
    result = fabric.operations.local(command, capture=True)
    if result:
        return archive_name
    else:
        print("returning none")
        return None


def do_deploy(archive_path):
    """ function to deploy data to servers and return true if successful
    """

    # check if archive_path exists
    import os
    if not os.path.isfile(archive_path):
        print("Path doesn't exist")
        return False
    else:
        # Upload the archive to the /tmp/ directory of the web server
        # fabric.operations.run("mkdir -p /tmp/versions/")

        archive = archive_path[9:]
        result = put(archive_path, "/tmp/{}".format(archive))
        if result.failed:
            return False
        # Uncompress the archive on the web server
        dest_path = archive_path[9:-4]
        # print (dest_path)
        if run("mkdir -p /data/web_static/releases/{}".
                format(dest_path)).failed:
            return False
        if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
                archive, dest_path)).failed:
            return False
        # Delete the archive from the web server
        if run("rm -rf /tmp/{}".format(archive)).failed:
            return False
        # Delete the symbolic link /data/web_static/current from the web server
        if run("rm  -f /data/web_static/current".format(archive)).failed:
            return False
        # Move the location of unpacked to one level  up
        prev_path = "/data/web_static/releases/{}/web_static/*".format(
                dest_path)
        next_path = "/data/web_static/releases/{}/".format(dest_path)
        if run("cp -r {} {}".format(prev_path, next_path)).failed:
            return False
        # Create a new the symbolic link on the web server
        if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
                format(dest_path)).failed:
            return False
        return True


def deploy():
    """ archive data and distribute it to servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    else:
        print("archive path : {}".format(archive_path))
        return do_deploy(archive_path)
