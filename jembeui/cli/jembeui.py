from getpass import getuser
import importlib
import click
from click import echo, secho
import os
from jembe.cli.utils import make_python_identifier, extract_project_template


@click.group()
def jembeui():
    pass


@jembeui.command()
@click.option(
    "--name",
    help="Name",
    prompt="Project Name",
    required=True,
    default=lambda: make_python_identifier(os.path.basename(os.getcwd())),
)
@click.option(
    "--description", help="Description", prompt=True, required=False, default=""
)
def startproject(name, description):
    """Starts JembeUI project in current directory"""
    name = make_python_identifier(name)

    import jembeui

    ctx = {
        "project_name": name,
        "project_description": description,
        "project_author": getuser(),
        "jembe_version": importlib.metadata.version("jembe"),
        "secret_key": str(os.urandom(24).__repr__()),
        "jembeui_root": jembeui.__path__[0],
    }

    extract_project_template("basic", ctx=ctx, root_dir=jembeui.__path__[0])

    echo()
    echo("New JembeUI project is suceessfully created in current directory!", color=True)
    echo()
    echo("To install required development dependencies execute:")
    secho("\t$ pip install -e .[dev]", bold=True)
    secho("\t$ npm install", bold=True)
    secho("\t$ flask db init", bold=True)
    echo()
    echo("To start development execute (in separate terminals):")
    secho("\t$ flask run", bold=True)
    secho("\t$ npm run dev", bold=True)
    echo()
    echo("To package project for deployment run:")
    secho("\t$ python -m build", bold=True)
    echo()
