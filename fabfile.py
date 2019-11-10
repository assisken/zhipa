import os

from fabric import Connection, task, Config

host = os.getenv('DEPLOY_HOST')
port = os.getenv('DEPLOY_PORT')
user = os.getenv('DEPLOY_USER')
password = os.getenv('DEPLOY_PASSWORD')
key = os.getenv('DEPLOY_KEY')
project_dir = os.getenv('PROJECT_DIR')
service = os.getenv('SERVICE_NAME')
python = os.getenv('PYTHON')
ci = os.getenv('CI')

config = Config({
    'sudo': {
        'password': password,
        'prompt': '[sudo]\n'
    }
})


@task
def deploy(ctx):
    if not ci:
        print('Run is allowed only in CI!')
        exit(1)

    with Connection(host=host, port=int(port), user=user, config=config,
                    connect_kwargs={'key_filename': key, 'look_for_keys': False}) as con:
        with con.cd(os.path.join('$HOME', project_dir)):
            con.run('git checkout master')
            con.run('git pull origin master')
            with con.prefix(f'source {os.path.join("$HOME", project_dir, ".env", "bin", "activate")}'):
                con.run('pip3.7 install -r requirements.txt')
                con.run(f'{python} manage.py migrate --noinput')
                con.run(f'{python} manage.py collectstatic --noinput')
        con.sudo(f'systemctl stop {service}')
        con.sudo(f'systemctl start {service}')
