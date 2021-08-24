#!/bin/bash

# creating directories to save the results of running PALM


# you pass the Kevin dir parent
# >>> ./create_PALM_directories_00015.sh /Volumes/Amr_1TB

Usage() {
    echo ""
    echo "you pass the Kevin dir parent"
    echo ""
    echo "Usage:"
    echo ">>> ./create_PALM_directories_00015.sh /Volumes/Amr_1TB"
    echo ">>> ./create_PALM_directories_00015.sh /home/in/aeed/Work"
    echo ">>> ./create_PALM_directories_00015.sh /media/amr/Amr_4TB/Work"
    echo ""
    exit 1
}

[ "$1" = "" ] && Usage


cd ${1}/Kevin

mkdir palm_ants
mkdir -p palm_ants/run-01/{dim_10,dim_15,dim_20,dim_25,dim_40,dim_50,dim_100}
mkdir -p palm_ants/run-02/{dim_10,dim_15,dim_20,dim_25,dim_40,dim_50,dim_100}




for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_10/43ddee1b109476bbf41ba6bf431ef9eefb2055bd/dual_regression/output/dr_stage2_ic*.nii.gz;do echo "-i $img"; done
