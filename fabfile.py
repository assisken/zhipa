import os

from fabric import Connection, task, Config

host = os.getenv('DEPLOY_HOST')
port = os.getenv('DEPLOY_PORT')
user = os.getenv('DEPLOY_USER')
password = os.getenv('DEPLOY_PASSWORD')
project_dir = os.getenv('PROJECT_DIR')
service = os.getenv('SERVICE_NAME')
python = os.getenv('PYTHON')
ci = os.getenv('CI')


@task
def deploy(ctx):
    if not ci:
        print('Run is allowed only in CI!')
        exit(1)

    config = Config({
        'sudo': {
            'password': password,
            'prompt': '[sudo] '
        },
        'reject-unknown-hosts': True,
        'shell': '/bin/bash -lic'
    })

    print(config)
    with Connection(host=host, port=int(port), user=user,
                    connect_kwargs={'password': password}, config=config) as con:
        with con.cd(os.path.join('$HOME', project_dir)):
            print(host, port, user)
            con.run('git checkout master')
            con.run('git pull origin master')
            with con.prefix(f'source {os.path.join("$HOME", project_dir, ".env", "bin", "activate")}'):
                con.run('pip3.7 install -r requirements.txt')
                con.run(f'{python} manage.py migrate --noinput')
                con.run(f'{python} manage.py collectstatic --noinput')
        print(config)
        con.run(f'echo "{config}" > dep.txt')
        con.sudo(f'systemctl stop {service}')
        con.sudo(f'systemctl start {service}')
