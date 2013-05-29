from fabric.contrib.files import exists
from fabric.api import cd, run
from os import path


REPO_URL = 'https://github.com/hjwp/book-example.git'
SITES_FOLDER = '/home/harry/sites'

def create_directory_structure(SITES_FOLDER, site_name):
    base_folder = path.join(SITES_FOLDER, site_name)
    run('mkdir -p %s' % (base_folder))
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (base_folder, subfolder))


def get_latest_source(site_name):
    source_folder = path.join(SITES_FOLDER, site_name, 'source')
    if exists(path.join(source_folder, '.git')):
        with cd(source_folder):
            run('git pull')
            run('git reset --hard')
    else:
        with cd(source_folder):
            run('git clone %s %s' % (REPO_URL, source_folder))


def update_virtualenv(site_name):
    source_folder = path.join(SITES_FOLDER, site_name, 'source')
    with cd(source_folder):
        if not exists(path.join(source_folder, '../virtualenv')):
            run('virtualenv ../virtualenv')
        run('../virtualenv/bin/pip install -r requirements.txt')



def update_static_files(site_name):
    source_folder = path.join(SITES_FOLDER, site_name, 'source')
    with cd(source_folder):
        run('python manage.py collectstatic --noinput')


def update_database(site_name):
    source_folder = path.join(SITES_FOLDER, site_name, 'source')
    with cd(source_folder):
        run('python manage.py syncdb --noinput')


