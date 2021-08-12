# This script to change images' name to include the group name instead of doing it manually,
# You have to pass the folder name from the bash script, and start and end of the number
# The image's name format is A021120_run-01_ants.nii.gz
# A021120_run-01_ants.nii.gz >>>> python change_files_to_contain_gp_name.py $PWD 0 7

# N.B the script has no number because it is called from inside a script not itself


import os
import re
import sys

# type help message in case of no input from the command line


def help_message():
    print("""Input argument missing \n
    # This script to change images' name to include the group name instead of doing it manually,
    # You have to pass the folder name from the bash script, and start and end of the number \n

    >>> python change_files_to_contain_gp_name.py <directory to change names> start end \n
    Examples (different OS):
    >>> python change_files_to_contain_gp_name.py /Volumes/Amr_1TB/Kevin/resting_state_gp_analysis_ants 0 7
    >>> python change_files_to_contain_gp_name.py /Volumes/Amr_1TB/Kevin/resting_state_gp_analysis_flirt 0 7 \n

    >>> python change_files_to_contain_gp_name.py /home/in/aeed/Work/Kevin/resting_state_gp_analysis_ants 0 7
    >>> python change_files_to_contain_gp_name.py /home/in/aeed/Work/Kevin/resting_state_gp_analysis_flirt 0 7 \n

    >>> python change_files_to_contain_gp_name.py /media/amr/Amr_4TB/Work/Kevin/resting_state_gp_analysis_ants 0 7
    >>> python change_files_to_contain_gp_name.py /media/amr/Amr_4TB/Work/Kevin/resting_state_gp_analysis_flirt 0 7

    """)


if len(sys.argv) < 2:
    help_message()
    exit(0)

dir = sys.argv[1]
os.chdir(dir)
start = int(sys.argv[2])
end = int(sys.argv[3])

# WT gp
A = ['A021120',
     'A241120',
     'A251120',
     'B201120']

# OT-Chr2 gp
B = ['A051120',
     'A061120',
     'A231120',
     'A271020',
     'B191120',
     'B231020']

for image in os.listdir(dir):
    print(image)
    number = image[start:end]
    print(number)
    if number in A:
        os.rename(image, 'A_%s' % image)

    elif number in B:
        os.rename(image, 'B_%s' % image)
