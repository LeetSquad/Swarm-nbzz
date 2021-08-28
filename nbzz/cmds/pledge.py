import click
from pathlib import Path
from nbzz.cmds.pledge_funcs import pledge


@click.command("pledge", short_help="pledge nbzz")
@click.option("-n", "--number", default=15, help="Number of pledged coins", show_default=True)
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("-p", "--password",  type=str, prompt="input password of bee",help="password of bee")
@click.pass_context
def pledge_cmd(ctx: click.Context, number, password,bee_key_path) -> None:
    pledge(number,password,bee_key_path)
    
