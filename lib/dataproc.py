

def submit_ssh_job(
    git_repo,
    project_id,
    region,
    cluster_name,
    git_sha='HEAD',
    command='main.py params1 param2'
):
    """
    This is split in two parts: first, preparing the dataproc instance, second: run the job. This is so we can separate
    the logs and for easier debugging
    :param git_repo: repository containing the code of the job. Advised to use a fixed commit, or tag. Default to HEAD
    :param project_id
    :param region
    :param cluster_name
    :param command: the command to run when at the root folder of the repository, with optional arguments
    """
    import subprocess

    # Prepare the dataproc instance:
    # - install needed python tools
    # - clone the repo
    # - prepare the virtualenv
    # - install requirements
    setup = """
sudo apt install -y python3-distutils
cd /tmp
rm -rf job
git clone {git_repo} job
cd job
git checkout {git_sha}
virtualenv -p python3 venv
source venv/bin/activate

if test -f requirements.txt; then
    pip install -r requirements.txt
fi
""".format(git_repo=git_repo, git_sha=git_sha)

    cmd = ['/data/emmanuel/Downloads/google-cloud-sdk/bin/gcloud',
           'compute', 'ssh', cluster_name+'-m', '--project='+project_id, '--zone='+region,
           '--', setup]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout_setup, _ = process.communicate()

    # Need to log this to Cloud Logging:
    print(stdout_setup.decode())

    if process.returncode != 0:
        raise RuntimeError("Something happened during setup, check the logs")

    cmd = ['/data/emmanuel/Downloads/google-cloud-sdk/bin/gcloud',
           'compute', 'ssh', cluster_name+'-m', '--project='+project_id, '--zone='+region,
           '--',
           'cd /tmp/job && source venv/bin/activate && python {command}'.format(command=command)]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = process.communicate()

    # Need to log this in Cloud Logging / Database, for user access and debugging
    print(stdout.decode())

    if process.returncode != 0:
        raise RuntimeError("Something happened while running job, check the logs")


