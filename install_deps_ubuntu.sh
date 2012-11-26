#!/bin/bash
sudo apt-get update
cat requirements.apt | xargs sudo apt-get install -y

sudo apt-get install -y python-pip
sudo pip install virtualenv