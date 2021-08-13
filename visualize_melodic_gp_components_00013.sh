#!/bin/bash
# we have components transformed using ants and those transformed using flirt
# you pass the Kevin dir parent, ants or flirt, and no of dims
# >>> ./visualize_melodic_gp_components_00013.sh /Volumes/Amr_1TB ants 10

Usage() {
    echo ""
    echo "you pass the Kevin dir parent, ants or flirt, and no of dims"
    echo ""
    echo "Usage:"
    echo ">>> ./visualize_melodic_gp_components_00013.sh /Volumes/Amr_1TB ants 10"
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
--zrange -4.147664799169454 235.99990866766535 \
--ncols 10 \
--nrows 4   \
${1}/Kevin/std_master.nii \
${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_${2}/_dim_${3}/melodic_group/melodic_IC.nii.gz
