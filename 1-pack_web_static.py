#!/usr/bin/python3
# usage: fab -f 1-pack_web_static.py do_pack
""" Function that compress a folder """
from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """Create a .tgz archive from the contents of the web_static folder."""
    t = datetime.now()
    timestamp = t.strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    if not os.path.exists("versions"):
        local("mkdir versions")

    try:
        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None
