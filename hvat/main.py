import click
from hvac import Client

from hvat.config import read_config
from hvat.initialization import init_and_push


@click.group()
@click.option(
    "--config", default="/etc/hvat/hvat.yaml", help="Location of config file to use"
)
@click.pass_context
def cli(ctx, config):
    ctx.ensure_object(dict)
    config = read_config(config)
    ctx.obj["config"] = config


@cli.command()
@click.pass_context
def init(ctx):
    config = ctx.obj["config"]

    client = Client(config["vault_url"])
    init_and_push(client, config)


cli.add_command(init)

if __name__ == "__main__":
    cli(obj={})
