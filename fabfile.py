import os

from fabric import Connection, task, Config
# from invoke.config import Config

host = os.getenv('DEPLOY_HOST')
port = os.getenv('DEPLOY_PORT')
user = os.getenv('DEPLOY_USER')
password = os.getenv('DEPLOY_PASSWORD')
project_dir = os.getenv('PROJECT_DIR')

config = Config({
    'sudo': {
        'password': password,
        'prompt': '[sudo] '
    },
    'reject-unknown-hosts': True
})


@task
def deploy(ctx):
    with Connection(host=host, port=int(port), user=user,
                    connect_kwargs={'password': password}, config=config) as con:
        with con.cd(os.path.join('$HOME', project_dir)):
            con.run('git checkout master')
            con.run('git pull')
