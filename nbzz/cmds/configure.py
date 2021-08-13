from pathlib import Path
from typing import Dict

import click

from nbzz.util.config import load_config, save_config, str2bool
from nbzz.util.default_root import DEFAULT_ROOT_PATH


def configure(
    root_path: Path,
    set_log_level: str,
    testnet: str,
):
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    change_made = False
    if set_log_level:
        levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
        if set_log_level in levels:
            config["logging"]["log_level"] = set_log_level
            print(f"Logging level updated. Check {DEFAULT_ROOT_PATH}/log/debug.log")
            change_made = True
        else:
            print(f"Logging level not updated. Use one of: {levels}")
    if testnet is not None:
        if testnet == "true" or testnet == "t":
            print("Setting Testnet")
            config["selected_network"] = testnet
            change_made = True

        elif testnet == "false" or testnet == "f":
            print("Setting Mainnet")
            net = "mainnet"
            config["selected_network"] = net
            change_made = True
        else:
            print("Please choose True or False")

    if change_made:
        print("Restart any running nbzz services for changes to take effect")
        save_config(root_path, "config.yaml", config)
    return 0

@click.command("configure", short_help="Modify configuration")
@click.option(
    "--testnet",
    "-t",
    help="configures for connection to testnet",
    type=click.Choice(["true", "t", "false", "f"]),
)
@click.option(
    "--set-log-level",
    "--log-level",
    "-log-level",
    help="Set the instance log level",
    type=click.Choice(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]),
)
@click.pass_context
def configure_cmd(
    ctx,
    set_log_level,
    testnet,
):
    configure(
        ctx.obj["root_path"],
        set_log_level,
        testnet,
    )
