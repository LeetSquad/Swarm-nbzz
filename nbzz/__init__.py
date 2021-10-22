from pkg_resources import DistributionNotFound, get_distribution, resource_filename

try:
    __version__ = get_distribution("nbzz-blockchain").version
except DistributionNotFound:
    # package is not installed

    __version__ = "2.0.0"

PYINSTALLER_SPEC_PATH = resource_filename("nbzz", "pyinstaller.spec")