#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
# usage = fab -f 3-deploy_web_static.py deploy -i my_ssh_private_key
from fabric.api import run, put, env, local
from datetime import datetime
import os

env.hosts = ['52.86.198.91', '52.207.52.133']
env.user = 'ubuntu'


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


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/
        # <archive filename without extension> on the web server
        archive_filename = archive_path.split('/')[-1]
        release_dir = '/data/web_static/releases/{}/'\
                      .format(archive_filename[:-4])
        run('mkdir -p {}'.format(release_dir))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_dir))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move extracted files to release folder
        run('mv {}web_static/* {}'.format(release_dir, release_dir))

        # Delete extracted files
        run('rm -rf {}web_static'.format(release_dir))

        # Delete the existing symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version
        run('ln -s {} /data/web_static/current'.format(release_dir))

        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to web servers.

    Returns:
        True if deployment is successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
