#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
# usage = fab -f 2-do_deploy_web_static.py do_deploy:archive_path={}
# -i my_ssh_private_key
from fabric.api import run, put, env
import os

env.hosts = ['52.86.198.91', '52.207.52.133']
env.user = 'ubuntu'


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
