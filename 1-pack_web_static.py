#!/usr/bin/python3
"""This is fabric script to compress data """
import fabric


def do_pack():
    """ function to pack data and then return path of result archive
    """

    # create version dir if doesn't exist
    fabric.operations.local('mkdir -p versions')

    # get date and time
    date_time = fabric.operations.local('date +"%Y%m%d%H%M%S"', capture=True)

    archive_name = "versions/web_static_{}".format(date_time)

    # compress data
    command = "tar -cvzf {}.tgz web_static".format(archive_name)
    print(command)
    result = fabric.operations.local(command, capture=True)
    if result:
        return archive_name
    else:
        return None
