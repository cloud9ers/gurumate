#!/bin/bash
#source environment/bin/activate
export PYTHONPATH=.:$PYTHONPATH
nosetests -s 
exit 0
