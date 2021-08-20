#!/bin/bash

# we need to compare three things:
# 1 -> difference between 2 groups at t2
# 2 -> difference between 2 groups at t1
# 3 -> t2-t1 between two groups
#
# we have two groups (4 and 6) each has two timepoints
#
# so one unpaired ttest design should do

# you pass the Kevin dir parent
# >>> ./create_designs.sh.sh /Volumes/Amr_1TB

Usage() {
    echo ""
    echo "you pass the Kevin dir parent"
    echo ""
    echo "Usage:"
    echo ">>> ./create_designs.sh /Volumes/Amr_1TB"
    echo ">>> ./create_designs.sh /home/in/aeed/Work"
    echo ">>> ./create_designs.sh /media/amr/Amr_4TB/Work"
    echo ""
    exit 1
}

[ "$1" = "" ] && Usage


mkdir ${1}/Kevin/designs

cd ${1}/Kevin/designs

design_ttest2 kevin_design 4 6 
