#!/bin/bash

WORKSPACE_DIR=$1
REPO_NAME=$2

cd $WORKSPACE_DIR

# Adjust permissions as docker volumes is owned by root
sudo chown -R $(id -g):$(id -u) $WORKSPACE_DIR

# Init west workspace if not present
if [ ! -d ".west" ]; then
    west init -l $REPO_NAME
fi

# Fetch upstream modules and setup tools
west update
west zephyr-export
west bridle-export

# Put .clang files in expected location by clangd
ln -s $REPO_NAME/.devcontainer/.clangd
ln -s zephyr/.clang-format

# Python Setup
python3 -m venv .venv
. .venv/bin/activate
west packages pip --install
