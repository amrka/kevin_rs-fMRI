# In[1]:

import re
import os
import sys
import distro
from nipype.interfaces.matlab import MatlabCommand
import matplotlib.pyplot as plt
import numpy as np
from nipype.pipeline.engine import Workflow, Node, MapNode
from nipype.interfaces.io import SelectFiles, DataSink
from os.path import join as opj
from nipype.interfaces.utility import IdentityInterface, Function, Select, Merge
import nipype.interfaces.spm as spm
import nipype.interfaces.ants as ants
import nipype.interfaces.afni as afni
import nipype.interfaces.fsl as fsl
from nipype import config
cfg = dict(execution={'remove_unnecessary_outputs': False})
config.update_config(cfg)


MatlabCommand.set_default_paths('/Users/amr/Downloads/spm12')
MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")


# -----------------------------------------------------------------------------------------------------
# type help message in case of no input from the command line


def help_message():
    print("""Input argument missing \n
    >>> python resting_state_gp_ICA_DR_00012.py <directory of Kevin> \n
    Examples (from different OS):
    >>> python resting_state_gp_ICA_DR_00012.py /Volumes/Amr_1TB
    >>> python resting_state_gp_ICA_DR_00012.py /home/in/aeed/Work
    >>> python resting_state_gp_ICA_DR_00012.py /media/amr/Amr_4TB/Work
    """)


if len(sys.argv) < 2:
    help_message()
    exit(0)

# instead of having to change the script between different copmuters and os
# we pass the directory with the name from the bash
origin_dir = sys.argv[1]


# we get the name of the operating sytem to determine how to run ('MultiProc' or 'SLURM')
os_name = distro.name()


experiment_dir = '{0}/Kevin/'.format(origin_dir)

output_dir = '{0}/Kevin/resting_state_melodic'.format(origin_dir)
working_dir = '{0}/Kevin/resting_state_melodic'.format(origin_dir)

melodic_workflow = Workflow(name='melodic_workflow')

melodic_workflow.base_dir = opj(experiment_dir, working_dir)


datasink_melodic = Node(DataSink(), name='datasink_melodic')
datasink_melodic.inputs.container = output_dir
datasink_melodic.inputs.base_directory = experiment_dir
datasink_melodic.inputs.parameterization = False


# -----------------------------------------------------------------------------------------------------
# In[3]:
template_brain = '{0}/Kevin/std_master.nii'.format(origin_dir)
template_mask = '{0}/Kevin/std_master_mask.nii'.format(origin_dir)

subjects_ants = '{0}/Kevin/resting_state_gp_analysis_ants/melodic_list_ants.txt'.format(origin_dir)
subjects_flirt = '{0}/Kevin/resting_state_gp_analysis_ants/melodic_list_ants.txt'.format(origin_dir)


melodic_group = Node(fsl.MELODIC(), name='melodic_group')

melodic_group.iterables = ('in_files', [subjects_ants, subjects_flirt])
melodic_group.inputs.approach = 'concat'
melodic_group.inputs.bg_image = template_brain
melodic_group.inputs.bg_threshold = 10.0
melodic_group.iterables = ('dim', [10, 15, 20, 25, 40, 50, 100])
melodic_group.inputs.tr_sec = 2.0
melodic_group.inputs.mm_thresh = 0.5
melodic_group.inputs.out_all = True
melodic_group.inputs.report = True
melodic_group.inputs.mask = template_mask
melodic_group.inputs.no_bet = True


# ========================================================================================================

# get the group_IC_maps from melodic to feed into mdual regression
# the default output from melodic is directory
def get_IC(out_dir):
    import os
    group_IC = os.path.abspath('{0}/melodic_IC.nii.gz'.format(out_dir))

    return group_IC


get_IC = Node(Function(input_names=['out_dir'],
                       output_names=['group_IC'],
                       function=get_IC),
              name='get_IC')


# -----------------------------------------------------------------------------------------------------
# In[4]:
# dual_regression \
# /media/amr/AMR_FAWZY/Octuber_MELODIC/resting_state_Melodic+DualRegression_10_IC/melodic_IC.nii.gz \
# 1 \
# /media/amr/AMR_FAWZY/Octuber_MELODIC/resting_state_Melodic+DualRegression_10_IC/design.mat \
# /media/amr/AMR_FAWZY/Octuber_MELODIC/resting_state_Melodic+DualRegression_10_IC/design.con \
# 5000 \
# /media/amr/HDD/Work/October_Acquistion/Dual_Regression_10 \
# `cat /media/amr/AMR_FAWZY/Octuber_MELODIC/Melodic_Subjects_10.txt` -v;

# design = '/home/in/aeed/Work/October_Acquistion/resting_state/Design_october_Acquistion_dual_regression.mat'
# contrast = '/home/in/aeed/Work/October_Acquistion/resting_state/Design_october_Acquistion_dual_regression.con'
#
#
# dual_regression = Node(fsl.model.DualRegression(), name='dual_regression')
# dual_regression.inputs.design_file = design
# dual_regression.inputs.con_file = contrast
# dual_regression.inputs.des_norm = True
# dual_regression.inputs.n_perm = 5000
# dual_regression.inputs.in_files = [
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_242.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_243.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_244.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_245.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_252.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_253.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_255.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_281.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_282.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_286.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_287.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_362.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_363.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_364.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_365.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/A_rsfMRI_filtered_366.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_229.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_230.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_232.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_233.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_234.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_235.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_236.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_237.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_261.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_262.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_263.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_264.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_273.nii.gz',
# '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_gp_ICA_DR/B_rsfMRI_filtered_274.nii.gz',]
#
#
#

# -----------------------------------------------------------------------------------------------------
# In[5]:


melodic_workflow.connect([
    (melodic_group, get_IC, [('out_dir', 'out_dir')]),
    # (get_IC, dual_regression, [('group_IC', 'group_IC_maps_4D')]),

])

# for the cluster
if os_name == 'CentOS Linux':
    melodic_workflow.run(plugin='SLURM', plugin_args={
        'dont_resubmit_completed_jobs': True, 'max_jobs': 50, 'sbatch_args': '--mem=40G'})

# for the laptop
elif os_name == 'Ubuntu':
    melodic_workflow.run('MultiProc', plugin_args={'n_procs': 8})

# for the iMac
elif os_name == 'Darwin':
    melodic_workflow.run('MultiProc', plugin_args={'n_procs': 8})
