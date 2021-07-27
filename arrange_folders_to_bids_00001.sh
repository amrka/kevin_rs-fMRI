#!/bin/bash

# arrange the raw data folders to match the bids format:

cd /Volumes/Amr_1TB/Kevin
mkdir raw_data_bids

# A251120/
    # ├── 1
    # .
    # .
    # .
    # ├── 9
    # ├── A251120_A251120_5014567.subject
    # ├── AdjResult
    # ├── AdjStatePerStudy
    # ├── Anatomical_fMRI_IsotX5P1.nii
    # ├── B0Map-ADJ_B0MAPX7P1.nii
    # ├── BET
    # ├── EPIGEAx_Isot05mmX10P1.nii
    # ├── EPIGEAx_Isot05mmX11P1.nii
    # ├── EPIGEAx_Isot05mmX12P1.nii
    # ├── EPIGEAx_Isot05mmX13P1.nii
    # ├── EPIGEAx_Isot05mmX14P1.nii
    # ├── EPIGEAx_Isot05mmX15P1.nii
    # ├── EPIGEAx_Isot05mmX16P1.nii
    # ├── EPIGEAx_Isot05mmX17P1.nii
    # ├── EPIGEAx_Isot05mmX18P1.nii
    # ├── EPIGEAx_Isot05mmX6P1.nii
    # ├── EPIGEAx_Isot05mmX8P1.nii
    # ├── EPIGEAx_Isot05mmX9P1.nii
    # ├── ResultState
    # ├── ScanProgram.scanProgram
    # ├── T2_TurboRAREX2P1.nii
    # ├── T2_TurboRAREX3P1.nii
    # ├── T2_TurboRAREX4P1.nii
    # ├── firstvol.nii.gz
    # ├── firstvol_bet.nii.gz
    # ├── firstvol_mask.nii.gz
    # └── subject


# anatomical images have pixdim1 = 1.250000, pixdim2 = 1.250000, pixdim3 = 5.000000 (after augmentation)
# rs-fMRI data has dim4 = 900 and there are 2 of them (before and after)
# the after has a bigger-digit name than the before
cd Kevin_rs_fMRI_raw_data

for subj in *;do
    cd $subj
    echo $subj
    mkdir -p ../../raw_data_bids/${subj}/{anat,func}
    # empty array to hold the resting state sessions
    rs_array=()
    # loop over images in alphabetic order, 2nd rs session will be ahead
    for img in *.nii;do
        pixdim1=`fslval $img pixdim1`
        pixdim2=`fslval $img pixdim2`
        pixdim3=`fslval $img pixdim3`
        dim4=`fslval $img dim4`
        # each img is named -> EPIGEAx_Isot05mmX16P1.nii xpt the anatomical

        if [ $pixdim1 == 1.250000 ] && [ $pixdim2 == 1.250000 ] && [ $pixdim3 == 5.000000 ]; then
            echo $img
            # to get the no of img
            img_no=`echo "$img" | sed  's/Anatomical_fMRI_IsotX/''/g' | sed 's/'P1.nii'/''/g'`
            cp $img ../../raw_data_bids/${subj}/anat/sub-${subj}_X${img_no}_T2w.nii.gz
        elif [ $dim4 == 900 ] && [ $pixdim1 == 5.000000 ] && [ $pixdim2 == 5.000000 ] && [ $pixdim3 == 5.000000 ];then
            echo $img
            img_no=`echo "$img" | sed  's/EPIGEAx_Isot05mmX/''/g' | sed 's/'P1.nii'/''/g'`
            cp $img ../../raw_data_bids/${subj}/func/sub-${subj}_X${img_no}_bold.nii.gz
        fi
        # for rs in ${rs_array[@]};do
        #     img_no=`echo "$img" | sed  's/EPIGEAx_Isot05mmX/''/g' | sed 's/'P1.nii'/''/g'`
        #     cp $img ../../raw_data_bids/${subj}/func/sub-${subj}_X${img_no}_bold.nii.gz
        # done
    done
    cd ..
done
# rs_array+=($img)
