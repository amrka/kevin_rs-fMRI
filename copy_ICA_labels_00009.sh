#!/bin/bash

# copy the labels txt files from inside the original directory after manual classification to
# an outside directory for convenience

# you pass the Kevin dir parent
# >>> ./copy_ICA_labels_00009.sh /Volumes/Amr_1TB

Usage() {
    echo ""
    echo "you pass the Kevin dir parent"
    echo ""
    echo "Usage:"
    echo ">>> ./copy_ICA_labels_00009.sh /Volumes/Amr_1TB"
    echo ">>> ./copy_ICA_labels_00009.sh /home/in/aeed/Work"
    echo ">>> ./copy_ICA_labels_00009.sh /media/amr/Amr_4TB/Work"
    echo ""
    exit 1
}

[ "$1" = "" ] && Usage


cd ${1}/Kevin
mkdir ICA_labels

cd ${1}/Kevin/resting_state_preproc_func_workingdir/resting_fmri_preproc_func
cp _run_id_run-0?_subject_id_*/_blurfwhm_bx_by_bz_6.5.6.5.6.5/_dim_25/Melodic/melodic.ica/*_run-0?.txt   ../../ICA_labels/
