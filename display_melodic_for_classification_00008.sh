#!/bin/bash
# you pass the Kevin dir parent, the run number as (run-01 or run-02), and the subject number
# >>> display_melodic_for_classification_00008.sh /Volumes/Amr_1TB run-01 A251120

Usage() {
    echo ""
    echo "you pass the Kevin dir parent, the run number as (run-01 or run-02), and the subject number"
    echo ""
    echo "Usage:"
    echo ">>> display_melodic_for_classification_00008.sh /Volumes/Amr_1TB run-01 A251120"
    echo ""
    exit 1
}

[ "$1" = "" ] && Usage

fsleyes \
--autoDisplay \
--scene melodic \
--hideCursor \
--displaySpace world  \
--zaxis 1 \
--sliceSpacing 5.0 \
--zrange -98.64418029785156 101.3553237915039 \
--ncols 10 \
--nrows 4   \
${1}/Kevin/resting_state_preproc_func_workingdir/resting_fmri_preproc_func/_run_id_${2}_subject_id_${3}/_blurfwhm_bx_by_bz_6.5.6.5.6.5/_dim_25/Melodic/melodic.ica


kevin dir
run-01
subject name
