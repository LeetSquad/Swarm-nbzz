import click


@click.group("keys", short_help="Manage your keys")
@click.pass_context
def keys_cmd(ctx: click.Context):
    """Create, delete, view and use your key pairs"""
    from pathlib import Path

    root_path: Path = ctx.obj["root_path"]
    if not root_path.is_dir():
        raise RuntimeError("Please initialize (or migrate) your config directory with nbzz init")


@keys_cmd.command("show", short_help="Displays Swarm key in bee")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
def show_cmd(bee_key_path):
    from .keys_funcs import show_swarm_key
    show_swarm_key(bee_key_path)

