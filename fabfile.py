from fabric.context_managers import settings
from fabric.contrib.files import exists
from fabric.api import cd, env, local, run
from os import listdir, path
import shutil
import unittest
from mock import patch


REPO_URL = 'https://github.com/hjwp/book-example.git'
SITES_FOLDER = '/home/harry/sites'

def _create_directory_structure(site_name):
    base_folder = path.join(SITES_FOLDER, site_name)
    run('mkdir -p %s' % (base_folder))
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (base_folder, subfolder))


def _update_files(source_folder):
    if exists('.git'):
        run('git pull')
        run('git reset --hard')
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))

    if not exists('../virtualenv'):
        run('virtualenv ../virtualenv')
    run('../virtualenv/bin/pip install -r requirements.txt')

    run('python manage.py collectstatic --noinput')
    run('python manage.py syncdb --noinput')


def update():
    print 'running against', env.host
    _create_directory_structure(env.host)

    source_folder = path.join(SITES_FOLDER, env.host, 'source')
    with cd(source_folder):
        _update_files()



class FabFileTest(unittest.TestCase):
    def tearDown(self):
        if path.exists('/tmp/fabfiletest'):
            shutil.rmtree('/tmp/fabfiletest')

    @patch('fabfile.run', local)
    @patch('fabfile.SITES_FOLDER', '/tmp/fabfiletest')
    def test_update_creates_folders(self):
        _create_directory_structure('www.testhosts.com')

        self.assertEqual(
            listdir('/tmp/fabfiletest'),
            ['www.testhosts.com']
        )
        self.assertItemsEqual(
            listdir('/tmp/fabfiletest/www.testhosts.com'),
            ['database', 'source', 'static', 'virtualenv']
        )


    @patch('fabfile.run')
    @patch('fabfile.exists')
    def test_update_files(self, mock_run, mock_cd):
        _create_directory_structure('www.testhosts.com')

        self.assertEqual(
            listdir('/tmp/fabfiletest'),
            ['www.testhosts.com']
        )
        self.assertItemsEqual(
            listdir('/tmp/fabfiletest/www.testhosts.com'),
            ['database', 'source', 'static', 'virtualenv']
        )


