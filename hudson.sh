#!/bin/bash
source environment/bin/activate
nosetests --exclude-dir=environment/ --with-xunit
exit 0
