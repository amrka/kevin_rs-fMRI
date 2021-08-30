#!/bin/bash

# creating directories to save the results of running PALM of subtracting run-02 - run-01


# you pass the Kevin dir parent
# >>> ./create_subtract_PALM_directories_00018.sh /Volumes/Amr_1TB

Usage() {
    echo ""
    echo "you pass the Kevin dir parent"
    echo ""
    echo "Usage:"
    echo ">>> ./create_subtract_PALM_directories_00018.sh /Volumes/Amr_1TB"
    echo ">>> ./create_subtract_PALM_directories_00018.sh /home/in/aeed/Work"
    echo ">>> ./create_subtract_PALM_directories_00018.sh /media/amr/Amr_4TB/Work"
    echo ""
    exit 1
}

[ "$1" = "" ] && Usage


cd ${1}/Kevin

mkdir -p palm_ants/subtract/{dim_10,dim_15,dim_20,dim_25,dim_40,dim_50,dim_100}


# ==================================================================================================
# generate lists with -i flag to use with palm instead of inputting manually
# 10
for img in `ls ${1}/subtraction/_dim_10/subtraction_dim_*_dr_stage2_ic*.nii.gz`;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/subtract/dim_10/palm_dim_10_subtract.txt;
done

# =============================================15=============================================
# 15
for img in `ls ${1}/subtraction/_dim_15/subtraction_dim_*_dr_stage2_ic*.nii.gz`;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/subtract/dim_15/palm_dim_15_subtract.txt;
done

# =============================================20=============================================
# 20
for img in `ls ${1}/subtraction/_dim_20/subtraction_dim_*_dr_stage2_ic*.nii.gz`;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/subtract/dim_20/palm_dim_20_subtract.txt;
done

# =============================================25=============================================
# 25
for img in `ls ${1}/subtraction/_dim_25/subtraction_dim_*_dr_stage2_ic*.nii.gz`;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/subtract/dim_25/palm_dim_25_subtract.txt;
done

# =============================================40=============================================
# 40
for img in `ls ${1}/subtraction/_dim_40/subtraction_dim_*_dr_stage2_ic*.nii.gz`;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/subtract/dim_40/palm_dim_40_subtract.txt;
done

# =============================================50=============================================
# 50
for img in `ls ${1}/subtraction/_dim_50/subtraction_dim_*_dr_stage2_ic*.nii.gz`;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/subtract/dim_50/palm_dim_50_subtract.txt;
done

# =============================================100=============================================
# 100
for img in `ls ${1}/subtraction/_dim_100/subtraction_dim_*_dr_stage2_ic*.nii.gz`;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/subtract/dim_100/palm_dim_100_subtract.txt;
done
