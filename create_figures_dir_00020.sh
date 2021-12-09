#!/bin/bash

# create a dir for functional connectivity directory

# you pass the Kevin dir parent
# >>> ./create_figures_dir_00020.sh /Users/aeed/Documents

Usage() {
    echo ""
    echo "you pass the Kevin dir parent"
    echo ""
    echo "Usage:"
    echo ">>> ./create_figures_dir_00020.sh /Users/aeed/Documents"
    echo ">>> ./create_figures_dir_00020.sh /media/amr/Amr_4TB/Work"
    echo ""
    exit 1
}

[ "$1" = "" ] && Usage


cd ${1}/Kevin


mkdir -p functional_conn_figures
cd functional_conn_figures
mkdir -p run_01/{dim_10,dim_15,dim_20,dim_25,dim_40,dim_50,dim_100}
mkdir -p run_02/{dim_10,dim_15,dim_20,dim_25,dim_40,dim_50,dim_100}
mkdir -p subtraction/{dim_10,dim_15,dim_20,dim_25,dim_40,dim_50,dim_100}
