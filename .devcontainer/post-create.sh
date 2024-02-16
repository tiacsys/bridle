#!/bin/bash

WORKSPACE_DIR=$1
REPO_NAME=$2

cd $WORKSPACE_DIR

if [ ! -d ".west" ]; then
    west init -l $REPO_NAME
fi

west update
west bridle-export


pip3 install --upgrade --requirement zephyr/scripts/requirements.txt
pip3 install --upgrade --requirement $REPO_NAME/scripts/requirements.txt