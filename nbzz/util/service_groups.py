from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "nbzz_harvester nbzz_timelord_launcher nbzz_timelord nbzz_farmer nbzz_full_node nbzz_wallet".split(),
    "node": "nbzz_full_node".split(),
    "harvester": "nbzz_harvester".split(),
    "farmer": "nbzz_harvester nbzz_farmer nbzz_full_node nbzz_wallet".split(),
    "farmer-no-wallet": "nbzz_harvester nbzz_farmer nbzz_full_node".split(),
    "farmer-only": "nbzz_farmer".split(),
    "timelord": "nbzz_timelord_launcher nbzz_timelord nbzz_full_node".split(),
    "timelord-only": "nbzz_timelord".split(),
    "timelord-launcher-only": "nbzz_timelord_launcher".split(),
    "wallet": "nbzz_wallet nbzz_full_node".split(),
    "wallet-only": "nbzz_wallet".split(),
    "introducer": "nbzz_introducer".split(),
    "simulator": "nbzz_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
