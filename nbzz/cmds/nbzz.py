import click

from nbzz import __version__
from nbzz.cmds.configure import configure_cmd
from nbzz.cmds.init import init_cmd
from nbzz.cmds.alias import alias_cmd
from nbzz.cmds.lockup import lockup_cmd
from nbzz.cmds.pledge import pledge_cmd
from nbzz.cmds.gatekeeper import gatekeeper_cmd
from nbzz.cmds.start import start_cmd,status_cmd
from nbzz.cmds.stop import stop_cmd
from nbzz.cmds.wallet import wallet_cmd
from nbzz.util.default_root import DEFAULT_ROOT_PATH

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def monkey_patch_click() -> None:
    # this hacks around what seems to be an incompatibility between the python from `pyinstaller`
    # and `click`
    #
    # Not 100% sure on the details, but it seems that `click` performs a check on start-up
    # that `codecs.lookup(locale.getpreferredencoding()).name != 'ascii'`, and refuses to start
    # if it's not. The python that comes with `pyinstaller` fails this check.
    #
    # This will probably cause problems with the command-line tools that use parameters that
    # are not strict ascii. The real fix is likely with the `pyinstaller` python.

    import click.core

    click.core._verify_python3_env = lambda *args, **kwargs: 0  # type: ignore


@click.group(
    help=f"\n  Manage nbzz blockchain infrastructure ({__version__})\n",
    epilog="Try 'nbzz start node' or 'nbzz show -s'",
    context_settings=CONTEXT_SETTINGS,
)
@click.option("--root-path", default=DEFAULT_ROOT_PATH, help="Config file root", type=click.Path(), show_default=True)
@click.pass_context
def cli(ctx: click.Context, root_path: str) -> None:
    from pathlib import Path

    ctx.ensure_object(dict)
    ctx.obj["root_path"] = Path(root_path)


@cli.command("version", short_help="Show nbzz version")
def version_cmd() -> None:
    print(__version__)



# @cli.command("run_daemon", short_help="Runs nbzz daemon")
# @click.pass_context
# def run_daemon_cmd(ctx: click.Context) -> None:
#     from nbzz.daemon.server import async_run_daemon
#     import asyncio

#     asyncio.get_event_loop().run_until_complete(async_run_daemon(ctx.obj["root_path"]))


cli.add_command(wallet_cmd)
cli.add_command(alias_cmd)
cli.add_command(configure_cmd)
cli.add_command(init_cmd)
cli.add_command(pledge_cmd)
cli.add_command(gatekeeper_cmd)
cli.add_command(start_cmd)
cli.add_command(status_cmd)
cli.add_command(stop_cmd)
cli.add_command(lockup_cmd)


def main() -> None:
    monkey_patch_click()
    cli()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
