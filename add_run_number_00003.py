# change the names of the bold files to contain run number


import os
import re
import sys
dir = sys.argv[1]

file_list = os.listdir(dir)
print(file_list)
# to get the acquistion number
acq_pattern = '_X(.*?)_bold.nii.gz'

# to get the subject_name
subj_pattern = "sub-(.*?)_X"

print("Current directory -> {0}".format(dir))

subj_no = re.search(subj_pattern, file_list[0]).group(1)
print("This is subject -> {0}".format(subj_no))


if int(re.search(acq_pattern, file_list[0]).group(1)) > int(re.search(acq_pattern, file_list[1]).group(1)):
    os.rename(file_list[0], "sub-{0}-X{1}-rs_bold_run2.nii.gz".format(subj_no,
                                                                      re.search(acq_pattern, file_list[0]).group(1)))
    os.rename(file_list[1], "sub-{0}-X{1}-rs_bold_run1.nii.gz".format(subj_no,
                                                                      re.search(acq_pattern, file_list[1]).group(1)))
else:
    os.rename(file_list[0], "sub-{0}-X{1}-rs_bold_run1.nii.gz".format(subj_no,
                                                                      re.search(acq_pattern, file_list[0]).group(1)))
    os.rename(file_list[1], "sub-{0}-X{1}-rs_bold_run2.nii.gz".format(subj_no,
                                                                      re.search(acq_pattern, file_list[1]).group(1)))
