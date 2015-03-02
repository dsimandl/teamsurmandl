from fabric.contrib.files import append, exists, sed
from fabric.api import local, env, cd, run
from fabric.colors import green, red

REPO_URL = "https://github.com/dsimandl/teamsurmandl.git"

def backup():
    local('git pull')
    print("Enter files you want to add, or just press return for all files")
    files = raw_input()
    if files is None:
        local('git add .')
    else:
        local('git add %s' % files)
    print("enter your commit comment:")
    comment = raw_input()
    local('git commit -m "%s"' % comment)
    local('git push')

def deploy():
    site_folder = '/home/%s' % env.user
    source_folder = site_folder + '/www/teamsurmandl'
    celery_process = 'celeryd'
    web_server_process = 'nginx'
    gunicorn_process = 'gunicorn-teamsurmandl'
    print(red("Beginning Deploy"))
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, site_folder)
    _update_virtualenv(site_folder, source_folder)
    _update_static_files(source_folder, site_folder)
    _syncdb(source_folder, site_folder)
    _migratedb(source_folder, site_folder)
    _restart_services(celery_process, web_server_process, gunicorn_process)
    print(red("Deploy Complete!"))

def _create_directory_structure_if_necessary(site_folder):
    print(green("Creating inital directory structure if it doesnt exist"))
    for subfolder in ('teamsurmandl', 'www'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        print(green("fetching the git repo for updates"))
        run('cd %s && git fetch' % (source_folder,))
    else:
        print(green("cloning the git repo from master"))
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    print(green("Resetting HARD blow away any local changes"))
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/teamsurmandl/settings/base.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path, 'TEMPLATE_DEBUG = True', 'TEMPLATE_DEBUG = False')
    sed(settings_path, 'MEDIA_ROOT = root("..", "uploads")', 'MEDIA_ROOT = ("/assets/"')
    sed(settings_path, 'STATIC_ROOT = root("..", "static")', 'STATIC_ROOT = root("..", "static/")')

def _update_virtualenv(site_folder, source_folder):
    print(green("Installing requirements..."))
    virtualenv_folder = site_folder + '/teamsurmandl'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python==python2.7 %s'  %(virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder))

def _update_static_files(source_folder, site_folder):
    print(green("Collecting static files..."))
    run('cd %s && %s/teamsurmandl/bin/python2.7 manage.py collectstatic --noinput' % (source_folder,site_folder,))

def _syncdb(source_folder, site_folder):
    print(green("Syncing the database..."))
    run('cd %s && %s/teamsurmandl/bin/python2.7 manage.py syncdb' % (source_folder, site_folder))

def _migratedb(source_folder, site_folder):
    print(green("Migrating the database..."))
    run('cd %s && %s/teamsurmandl/bin/python2.7 manage.py migrate' % (source_folder, site_folder))

def _restart_services(celery_process, web_server_process, gunicorn_process):
    print(green("Restarting the celery worker"))
    run("sudo service %s restart" % celery_process)
    print(green("Restart the uwsgi process"))
    run("sudo service %s restart" % web_server_process)
    print(green("Retart the gunicorn process"))
    run("sudo service %s restart" % gunicorn_process)
