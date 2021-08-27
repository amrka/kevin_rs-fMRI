#!/bin/bash

# subtract run-02 - run-01 to get the difference to use it in palm

# you pass the Kevin dir parent
# >>> ./subtract_run-02_run-01_00017.sh /Volumes/Amr_1TB

Usage() {
    echo ""
    echo "you pass the Kevin dir parent"
    echo ""
    echo "Usage:"
    echo ">>> ./subtract_run-02_run-01_00017.sh /Volumes/Amr_1TB"
    echo ""
    exit 1
}

[ "$1" = "" ] && Usage

# first create an appropriate directory for the results

mkdir -p ${1}/Kevin/subtraction/{_dim_10,_dim_15,_dim_20,_dim_25,_dim_40,_dim_50,_dim_100}


# run-02 ->'43ddee1b109476bbf41ba6bf431ef9eefb2055bd'
                 
# run-01 ->'d0f02a8721eff087f281113015c672685b8a198b'
