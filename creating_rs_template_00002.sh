#!/bin/bash

# create a template from functional images to use for antsBrainextraction
# I did not create one for antamoical images, since the result was not very good, also BET works well


mkdir /home/in/aeed/Kevin/rs-temp

imcp \
/home/in/aeed/Kevin/raw_data_bids/A031120/func/sub-A031120_X8_bold.nii.gz \
/home/in/aeed/Kevin/rs-temp/

cd /home/in/aeed/Kevin/rs-temp
# use only 50 volumes out of 900
fslroi sub-A031120_X8_bold.nii.gz  sub 450 50
imrm sub-A031120_X8_bold.nii.gz
fslsplit sub.nii.gz -t

imrm sub.nii.gz

buildtemplateparallel.sh \
-d 3 \
-c 5 \
-j 200 \
-r 1 \
-o epi_templ vol*.nii.gz

# the skull mask was drawn manually using itksnap (epi_temp_mask.nii.gz), then
# fslmaths epi_templtemplate.nii.gz -mul epi_temp_mask.nii.gz epi_temp_snapped
