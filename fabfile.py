from fabric import task

hosts = ["ubuntu@ec2-52-58-217-51.eu-central-1.compute.amazonaws.com"]


@task(hosts=hosts)
def pull(c):
    code_dir = "/home/ubuntu/feature_requests/feature-requests/"
    c.run("cd {} && git fetch origin".format(code_dir))
    c.run("cd {} && git merge origin/master".format(code_dir))
    print("pull / update ok")


@task(hosts=hosts)
def work(c):
    code_dir = "/home/ubuntu/feature_requests/feature-requests/"
    venv_dir = "/home/ubuntu/feature_requests/venv/bin/"
    flask_app = "FLASK_APP=core"
    c.run("{0}pip install -r {1}requirements.txt".format(venv_dir, code_dir))
    c.run("cd {0} && {1} {2}flask db upgrade".format(code_dir, flask_app, venv_dir))
    print("work ok")


@task(hosts=hosts)
def restart(c):
    c.run("sudo systemctl restart gunicorn")


@task(hosts=hosts)
def full_deploy(c):
    pull(c)
    work(c)
    restart(c)
