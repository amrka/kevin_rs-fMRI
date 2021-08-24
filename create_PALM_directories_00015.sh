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


# There is an easier way rather than copying and pasting, but I am tired
# ==================================================================================================
# generate lists with -i flag to use with palm instead of inputting manually
# 10
for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_10\
/d0f02a8721eff087f281113015c672685b8a198b/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-01/dim_10/palm_dim_10_run-02.txt;
done

for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_10\
/43ddee1b109476bbf41ba6bf431ef9eefb2055bd/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-02/dim_10/palm_dim_10_run-02.txt;
done

# =============================================15=============================================
# 15
for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_15\
/d0f02a8721eff087f281113015c672685b8a198b/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-01/dim_15/palm_dim_15_run-02.txt;
done

for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_15\
/43ddee1b159476bbf41ba6bf431ef9eefb2055bd/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-02/dim_15/palm_dim_15_run-02.txt;
done

# =============================================20=============================================
# 20
for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_20\
/d0f02a8721eff087f281113015c672685b8a198b/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-01/dim_20/palm_dim_20_run-02.txt;
done

for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_20\
/43ddee1b159476bbf41ba6bf431ef9eefb2055bd/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-02/dim_20/palm_dim_20_run-02.txt;
done

# =============================================25=============================================
# 25
for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_25\
/d0f02a8721eff087f281113015c672685b8a198b/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-01/dim_25/palm_dim_25_run-02.txt;
done

for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_25\
/43ddee1b159476bbf41ba6bf431ef9eefb2055bd/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-02/dim_25/palm_dim_25_run-02.txt;
done
# =============================================40=============================================
# 40
for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_40\
/d0f02a8721eff087f281113015c672685b8a198b/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-01/dim_40/palm_dim_40_run-02.txt;
done

for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_40\
/43ddee1b159476bbf41ba6bf431ef9eefb2055bd/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-02/dim_40/palm_dim_40_run-02.txt;
done
# =============================================50=============================================
# 50
for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_50\
/d0f02a8721eff087f281113015c672685b8a198b/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-01/dim_50/palm_dim_50_run-02.txt;
done

for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_50\
/43ddee1b159476bbf41ba6bf431ef9eefb2055bd/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-02/dim_50/palm_dim_50_run-02.txt;
done
# =============================================100=============================================
# 100
for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_100\
/d0f02a8721eff087f281113015c672685b8a198b/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-01/dim_100/palm_dim_100_run-02.txt;
done

for img in ls ${1}/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_100\
/43ddee1b159476bbf41ba6bf431ef9eefb2055bd/dual_regression/output/dr_stage2_ic*.nii.gz;do

    echo "-i $img" >> ${1}/Kevin/palm_ants/run-02/dim_100/palm_dim_100_run-02.txt;
done
