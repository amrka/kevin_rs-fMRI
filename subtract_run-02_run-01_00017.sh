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
    echo ">>> ./subtract_run-02_run-01_00017.sh /home/in/aeed/Work"
    echo ">>> ./subtract_run-02_run-01_00017.sh /media/amr/Amr_4TB/Work"
    echo ""
    exit 1
}

[ "$1" = "" ] && Usage

# first create an appropriate directory for the results

mkdir -p ${1}/Kevin/subtraction/{_dim_10,_dim_15,_dim_20,_dim_25,_dim_40,_dim_50,_dim_100}


# run-02 ->'43ddee1b109476bbf41ba6bf431ef9eefb2055bd'

# run-01 ->'d0f02a8721eff087f281113015c672685b8a198b'

# N.B I checked that fslmaths subtraction works on all volumes of 4D images
for img in ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_*/43ddee1b109476bbf41ba6bf431ef9eefb2055bd/dual_regression/output/dr_stage2_ic*.nii.gz;do
    # extract the dim instead of looping over all of them or worse, copying the code many times
    dim=`echo $img | sed s?\$1/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_?? | sed s?/43ddee1b109476bbf41ba6bf431ef9eefb2055bd/dual_regression/output/.*??`
    echo $dim

    echo $img

    echo "${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_${dim}/d0f02a8721eff087f281113015c672685b8a198b/dual_regression/output/`basename ${img}`"

    fslmaths \
    ${img} \
    -sub \
    ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_${dim}/d0f02a8721eff087f281113015c672685b8a198b/dual_regression/output/`basename ${img}` \
    ${1}/Kevin/subtraction/_dim_${dim}/subtraction_dim_${dim}_`basename ${img}`

    echo "${1}/Kevin/subtraction/_dim_${dim}/subtraction_dim_${dim}_`basename ${img}`"
done
