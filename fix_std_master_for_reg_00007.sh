#!/bin/bash

# for a successful registration (in ANTs, it works well with FLIRT), the std_master.nii file needs some modification
# fslhd std_master.nii:
# qform_code	1
# qto_xyz:1	-1.938667 0.000000 0.000000 184.173340
# qto_xyz:2	0.000000 0.000000 1.938667 0.000000
# qto_xyz:3	0.000000 8.000000 0.000000 0.000000
# qto_xyz:4	0.000000 0.000000 0.000000 1.000000

# we need to change qform_code to zero
# you need to pass the Kevin directory from the command line and have std_master.nii in theis directory

# >>> ./fix_std_master_for_reg_00007.sh /home/in/aeed/Work

fslorient -setqformcode 0 $1/std_master.nii
