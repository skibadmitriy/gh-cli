import os
import click
from pathlib import Path
from github import Github, BadCredentialsException, UnknownObjectException


token_file_path = os.path.join(Path.home(), ".gh-cli")
token_file_name = os.path.join(token_file_path, "token")


def auth(token):
    login_or_token = token
    password = None
    jwt = None
    base_url = "https://api.github.com"
    timeout = 15
    user_agent = "PyGithub/Python"
    per_page = 30
    verify = True
    retry = None
    pool_size = None
    gh = Github(login_or_token,
                password,
                jwt,
                base_url,
                timeout,
                user_agent,
                per_page,
                verify,
                retry,
                pool_size)
    try:
        print("You are logged as {0}".format(gh.get_user().login))
    except BadCredentialsException:
        print("Bad credentials")
        return None
    return gh


def get_token_from_file():
    if os.path.exists(token_file_name):
        file = open(token_file_name, "r")
        token = file.readline().strip(" \t\n\r")
        return token
    else:
        print("Please authorize first")


@click.group()
def cli():
    pass


@cli.command(name="login", short_help="Login to GitHub")
def login():
    current_token = ""
    if not os.path.isdir(token_file_path):
        os.mkdir(token_file_path)
    if os.path.isfile(token_file_name):
        file = open(token_file_name, "r")
        current_token = file.readline().strip(" \t\n\r")
        file.close()
    file = open(token_file_name, "w+")
    token = input("Enter your OAuth GitHub Token [{0}]: ".format(current_token)).strip(" \t\n\r")
    if not token.strip():
        token = current_token
    auth(token)
    file.write(token)
    file.close()


@cli.command(name="repo", short_help="List repo")
def get_repo_list():
    token = get_token_from_file()
    if token is not None:
        gh = auth(token)
        if gh is not None:
            for repo in gh.get_user().get_repos():
                print(repo.name)


@cli.command(name="workflow", short_help="List workflow of repo")
@click.argument("repo_name")
def get_workflow_list(repo_name):
    token = get_token_from_file()
    if token is not None:
        gh = auth(token)
        if gh is not None:
            try:
                print("Workflow list repo {0}".format(repo_name))
                for workflow in gh.get_user().get_repo(repo_name).get_workflows():
                    print(workflow.name)
            except UnknownObjectException:
                print("Not found")


if __name__ == "__main__":
    cli()
