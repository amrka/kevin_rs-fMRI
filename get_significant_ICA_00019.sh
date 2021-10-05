#!/bin/bash

# get the significant components corrected across components

# you pass the Kevin dir parent
# >>> ./get_significant_ICA_00019.sh /Volumes/Amr_1TB

Usage() {
    echo ""
    echo "you pass the Kevin dir parent"
    echo ""
    echo "Usage:"
    echo ">>> ./get_significant_ICA_00019.sh /Volumes/Amr_1TB"
    echo ">>> ./get_significant_ICA_00019.sh /home/in/aeed/Work"
    echo ">>> ./get_significant_ICA_00019.sh /media/amr/Amr_4TB/Work"
    echo ""
    exit 1
}

[ "$1" = "" ] && Usage


cd ${1}/Kevin


cd ${1}/Kevin/resting_state_melodic/palm_workflow

rm significant_ICA.txt
touch significant_ICA.txt

for img in */*/*_tfce_tstat_mfwep_*.nii.gz;do
  echo $PWD/${img};
  p_98=`fslstats $img -P 98`;
  if [[ ${p_98} > 0.949 ]];then
    echo $PWD/${img} >> significant_ICA.txt
    echo ${p_98} >> significant_ICA.txt
  fi
done
