#!/bin/bash
# move the filtered 4D images to be used for group ICA and later for dual regression
# we are going to do the analysis using the 4d images transformed using ants and those with affine flirt
# you pass the Kevin dir parent
# >>> ./move_files_for_gp_analysis_00011.sh /Volumes/Amr_1TB

Usage() {
    echo ""
    echo "you pass the Kevin dir parent"
    echo ""
    echo "Usage:"
    echo ">>> ./move_files_for_gp_analysis_00011.sh /Volumes/Amr_1TB"
    echo ">>> ./move_files_for_gp_analysis_00011.sh /home/in/aeed/Work"
    echo ">>> ./move_files_for_gp_analysis_00011.sh /media/amr/Amr_4TB/Work"
    echo ""
    exit 1
}

[ "$1" = "" ] && Usage


mkdir ${1}/Kevin/resting_state_gp_analysis_ants
mkdir ${1}/Kevin/resting_state_gp_analysis_flirt


# you need to include the names of the subjects, otherwise, you will overwrite the images
# since they have the same name

# images registered using non-linear ants
cd ${1}/Kevin/raw_data_bids
for subj in *;do
		echo ${subj}
		imcp ${1}/Kevin/resting_state_metaflow_workingdir/metaflow/_run_id_run-01_subject_id_${subj}/synApply/afni_2d_smoothed_maths_filt_maths_regfilt_trans.nii.gz \
		${1}/Kevin/resting_state_gp_analysis_ants/${subj}_run-01_ants.nii.gz

		imcp ${1}/Kevin/resting_state_metaflow_workingdir/metaflow/_run_id_run-02_subject_id_${subj}/synApply/afni_2d_smoothed_maths_filt_maths_regfilt_trans.nii.gz \
		${1}/Kevin/resting_state_gp_analysis_ants/${subj}_run-02_ants.nii.gz

done


# images registered using affine flirt
cd ${1}/Kevin/raw_data_bids
for subj in *;do
		echo ${subj}
		imcp  ${1}/Kevin/resting_state_metaflow_workingdir/metaflow/_run_id_run-01_subject_id_${subj}/affine_flirt_Apply/afni_2d_smoothed_maths_filt_maths_regfilt_trans_flirt.nii.gz \
		${1}/Kevin/resting_state_gp_analysis_flirt/${subj}_run-01_flirt.nii.gz

		imcp  ${1}/Kevin/resting_state_metaflow_workingdir/metaflow/_run_id_run-02_subject_id_${subj}/affine_flirt_Apply/afni_2d_smoothed_maths_filt_maths_regfilt_trans_flirt.nii.gz \
		${1}/Kevin/resting_state_gp_analysis_flirt/${subj}_run-02_flirt.nii.gz
done

#
# add the group name to the files so it is easier to make group comparisons
python3 ${1}/Kevin/kevin_rs-fMRI/change_files_to_contain_gp_name.py ${1}/Kevin/resting_state_gp_analysis_ants 0 7
python3 ${1}/Kevin/kevin_rs-fMRI/change_files_to_contain_gp_name.py ${1}/Kevin/resting_state_gp_analysis_flirt 0 7

ls ${1}/Kevin/resting_state_gp_analysis_ants/*.nii.gz >> ${1}/Kevin/resting_state_gp_analysis_ants/melodic_list_ants.txt
ls ${1}/Kevin/resting_state_gp_analysis_flirt/*.nii.gz >> ${1}/Kevin/resting_state_gp_analysis_flirt/melodic_list_flirt.txt

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# some of the subjects included in melodic analysis, but were excluded from the dual regression
# only those who have the prefix A_* or B_* will be included in the analysis
# ants
ls ${1}/Kevin/resting_state_gp_analysis_ants/A_*_run-01_ants.nii.gz >> ${1}/Kevin/resting_state_gp_analysis_ants/DR_list_ants_run-01.txt
ls ${1}/Kevin/resting_state_gp_analysis_ants/B_*_run-01_ants.nii.gz >> ${1}/Kevin/resting_state_gp_analysis_ants/DR_list_ants_run-01.txt

ls ${1}/Kevin/resting_state_gp_analysis_ants/A_*_run-02_ants.nii.gz >> ${1}/Kevin/resting_state_gp_analysis_ants/DR_list_ants_run-02.txt
ls ${1}/Kevin/resting_state_gp_analysis_ants/B_*_run-02_ants.nii.gz >> ${1}/Kevin/resting_state_gp_analysis_ants/DR_list_ants_run-02.txt

# flirt
ls ${1}/Kevin/resting_state_gp_analysis_flirt/A_*_run-01_flirt.nii.gz >> ${1}/Kevin/resting_state_gp_analysis_flirt/DR_list_flirt_run-01.txt
ls ${1}/Kevin/resting_state_gp_analysis_flirt/B_*_run-01_flirt.nii.gz >> ${1}/Kevin/resting_state_gp_analysis_flirt/DR_list_flirt_run-01.txt

ls ${1}/Kevin/resting_state_gp_analysis_flirt/A_*_run-02_flirt.nii.gz >> ${1}/Kevin/resting_state_gp_analysis_flirt/DR_list_flirt_run-02.txt
ls ${1}/Kevin/resting_state_gp_analysis_flirt/B_*_run-02_flirt.nii.gz >> ${1}/Kevin/resting_state_gp_analysis_flirt/DR_list_flirt_run-02.txt


#then you create the design
