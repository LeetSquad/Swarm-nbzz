# Nbzz

## Installing

Follow below install instructions for Ubuntu 20.04 LTS.This software only supports 64 bit operating systems.

```bash

sudo apt update
sudo apt upgrade -y

# Install Git
sudo apt install git -y

# Checkout the source and install
git clone https://github.com/LeetSquad/Swarm-nbzz.git nbzz
cd nbzz

sh install.sh

. ./activate

```
All configuration data is stored in a directory structure at the `$NBZZ_ROOT` environment variable or at `~/.nbzz/stagenet/`. You can find databases, and logs there. Optionally, you can set `$NBZZ_ROOT` to the .nbzz directory in your home directory with export `NBZZ_ROOT=~/.nbzz` and if you add it to your `.bashrc` or `.zshrc` to it will remain set across logouts and reboots. If you set `$NBZZ_ROOT` you will have to migrate configuration items by hand or unset the variable for `nbzz init` to work with unset NBZZ_ROOT.

## To Update/Upgrade from previous version

```bash
cd nbzz
. ./activate
nbzz stop -d all
deactivate
git fetch
git checkout latest
git status
# git status should say "nothing to commit, working tree clean", 
# if you have uncommitted changes, RELEASE.dev0 will be reported.

sh install.sh

. ./activate

nbzz init

```

## Running


Once installed, run `nbzz init`.  
nbzz running in the goerli testnet ,to running nbzz ,you do need some geth.  
then `cd /path_to_bee/` ,you will see keys dir in there.  
then run `nbzz faucet -p you-bee-password` to get some nbzz for pledge.  
then run `nbzz pledge -p you-bee-password` to pledge some nbzz for start   
mining.