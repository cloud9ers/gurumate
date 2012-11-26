#!/bin/bash

#assuming the machine has virtualenv and pip installed
if [ ! -d cache ]
  then
   mkdir cache
fi

virtualenv --distribute environment

#export PYTHONPATH=

pip install --download-cache=cache -E environment -r requirements.pip
