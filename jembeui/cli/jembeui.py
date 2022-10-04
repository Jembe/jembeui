from getpass import getuser
import os
import importlib
import click
from click import echo, secho
from jembe.cli.utils import make_python_identifier, extract_project_template
import jembeui as jui


@click.group()
def jembeui():
    """Defines click jembeui group"""


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
@click.option(
    "--template",
    help="Project template",
    prompt="Project template",
    required=True,
    type=click.Choice(["basic", "with_auth"], case_sensitive=False),
)
def startproject(name, description, template="basic"):
    """Starts JembeUI project in current directory"""
    name = make_python_identifier(name)

    ctx = {
        "project_name": name,
        "project_description": description,
        "project_author": getuser(),
        "jembe_version": importlib.metadata.version("jembe"),
        "secret_key": str(repr(os.urandom(24))),
        "jembeui_root": jui.__path__[0],
    }

    extract_project_template(template.lower(), ctx=ctx, root_dir=jui.__path__[0])

    echo()
    echo(
        "New JembeUI project is suceessfully created in current directory!", color=True
    )
    echo()
    echo("To install required development dependencies execute:")
    secho("\t$ pip install -e .[dev]", bold=True)
    secho("\t$ npm install", bold=True)
    if template == "with_auth":
        secho("\t$ flask db upgrade", bold=True)
    echo()
    echo("To start development execute (in separate terminals):")
    secho("\t$ flask run", bold=True)
    secho("\t$ npm run dev", bold=True)
    echo()
    echo("To package project for deployment run:")
    secho("\t$ python -m build", bold=True)
    echo()
    secho(
        "Please read README.md for detail instructions and more information.", bold=True
    )
    echo()
