# In[1]:
# >>> python resting_state_metaflow_00009.py <directory of Kevin>
import re
import os
import sys
import glob
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
# ========================================================================================================
# type help message in case of no input from the command line


def help_message():
    print("""Input argument missing \n
    >>> python resting_state_metaflow_00009.py <directory of Kevin> \n
    Examples (from different OS):
    >>> python resting_state_metaflow_00009.py /Volumes/Amr_1TB
    >>> python resting_state_metaflow_00009.py /home/in/aeed/Work
    >>> python resting_state_metaflow_00009.py /media/amr/Amr_4TB/Work
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

subject_list = ['A021120',
                'A051120',
                'A231120',
                'A251120',
                'A301020',
                'B201120',
                'B261020',
                'A031120',
                'A061120',
                'A241120',
                'A271020',
                'B191120',
                'B231020'
                ]


run_list = ['run-01',
            'run-02']

output_dir = '{0}/Kevin/resting_state_metaflow_outputdir'.format(origin_dir)
working_dir = '{0}/Kevin/resting_state_metaflow_workingdir'.format(origin_dir)

metaflow = Workflow(name='metaflow')

metaflow.base_dir = opj(experiment_dir, working_dir)


# =====================================================================================================
# In[3]:
# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id', 'run_id']),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list),
                        ('run_id', run_list)]

# =====================================================================================================
# also, after comparison, I choose smoothing with 6.5 isotropic kernel, it looks much better than bigger kernels
# the registration to temp was done using affine (flirt) and non-linear (ants)
# I am going to apply both transformations and compare the output

kernel_size = 6.5
melodic_dim = 25

templates = {
    'Filtered_Smoothed_rs_fMRI': '{0}/Kevin/resting_state_preproc_func_workingdir/resting_fmri_preproc_func/'
                                 '_run_id_{run_id}_subject_id_{subject_id}/_blurfwhm_bx_by_bz_6.5.6.5.6.5/Add_Mean_Image/'
                                 'afni_2d_smoothed_maths_filt_maths.nii.gz'.format(origin_dir),

    'Melodic_Mix': '{0}/Kevin/resting_state_preproc_func_workingdir/resting_fmri_preproc_func/'
                   '_run_id_{run_id}_subject_id_{subject_id}/_blurfwhm_bx_by_bz_6.5.6.5.6.5/_dim_{1}/Melodic/melodic.ica/'
                   'melodic_mix'.format(origin_dir, melodic_dim),

    'labels': '{0}/Kevin/ICA_labels/{subject_id}_{run_id}.txt'.format(origin_dir),

    'coreg_trans': '{0}/Kevin/resting_state_preproc_func_workingdir/resting_fmri_preproc_func/'
                   '_run_id_{run_id}_subject_id_{subject_id}/coregistration/transformComposite.h5'.format(
                       origin_dir),

    'affine_2_temp': '{0}/Kevin/resting_state_preproc_anat_workingdir/resting_fmri_preproc_anat/'
                     '_subject_id_{subject_id}/flirt_aff_T1_2_temp/sub-{subject_id}_X5_T2w_corrected_brain_flirt.mat'.format(
                                     origin_dir),

    'syn_2_temp': '{0}/Kevin/resting_state_preproc_anat_workingdir/resting_fmri_preproc_anat/'
                  '_subject_id_{subject_id}/reg_T1_2_temp/transformComposite.h5'.format(
                                     origin_dir),


}

selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir),
                   name="selectfiles")

# =====================================================================================================
# In[4]:

datasink = Node(DataSink(), name='datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir
datasink.inputs.parameterization = False

substitutions = [('_subject_id_', '')]

datasink.inputs.substitutions = substitutions

# =====================================================================================================
# In[5]:

template_brain = '{0}/Kevin/std_master.nii'.format(origin_dir)
template_mask = '{0}/Kevin/std_master_mask.nii'.format(origin_dir)
TR = 2.0

# =====================================================================================================
# I Have calssified the melodic ICs outputs of each subject to signal or artefact
# this function works when you use the MELODIC layout, classify the components and later use
# the labels file as an input


def get_bad_components(labels):
    fh = open(labels)
    lines = fh.readlines()
    components_str = (lines[len(lines)-1])
    components_list = components_str.split()

    print(components_list)
    return components_list


get_bad_components = Node(name='get_bad_components',
                          interface=Function(input_names=['labels'],
                                             output_names=['components_list'],
                                             function=get_bad_components))

# =====================================================================================================
# In[8]:
# Define the fsl.regfilt Node
regfilt = Node(fsl.FilterRegressor(), name='Filter_Regressors')

# =====================================================================================================
# apply affine flirt transformations
affineApply = Node(fsl.ApplyXFM(), name='affineApply')
affineApply.inputs.reference = template_brain
affineApply.inputs.apply_xfm = True
affineApply.inputs.cost = 'corratio'
affineApply.inputs.bins = 256
affineApply.inputs.searchr_x = [-180, 180]
affineApply.inputs.searchr_y = [-180, 180]
affineApply.inputs.searchr_z = [-180, 180]
affineApply.inputs.dof = 12
affineApply.inputs.interp = 'trilinear'
# =====================================================================================================
# In[10]:
# Merge the trasnforms
merge_transforms = Node(Merge(2), name='merge_transforms')

# =====================================================================================================
# In[9]:
synApply = Node(ants.ApplyTransforms(), name='synApply')
synApply.inputs.dimension = 3

synApply.inputs.input_image_type = 3
synApply.inputs.num_threads = 1
synApply.inputs.float = True

synApply.inputs.reference_image = template_brain

# =====================================================================================================
# In[11]:
# write an appended list of the names of the files that enter the melodic


def write_name(in_file):
    f = open('/home/in/aeed/Work/October_Acquistion/resting_state_metaflow_workingdir/melodic_list_october_acquistions.txt', 'a')
    print(in_file)
    f.write('\n' + in_file)
    f.close()


write_name = Node(name='write_name',
                  interface=Function(input_names=['in_file'],

                                     function=write_name))


# =====================================================================================================
# In[12]:
# Connect the nodes:

metaflow.connect([
    (infosource, selectfiles, [('subject_id', 'subject_id'),
                               ('run_id', 'run_id')]),

    (infosource, get_bad_components, [('subject_id', 'subject_id')]),
    (selectfiles, regfilt, [('Filtered_Smoothed_rs_fMRI', 'in_file')]),
    (selectfiles, regfilt, [('Melodic_Mix', 'design_file')]),

    (selectfiles, get_bad_components, [('labels', 'labels')]),
    (get_bad_components, regfilt, [('components_list', 'filter_columns')]),


    (selectfiles, merge_transforms, [('Anat2Template', 'in1')]),
    (selectfiles, merge_transforms, [('example2Anat', 'in2')]),


    (regfilt, synApply, [('out_file', 'input_image')]),
    (merge_transforms, synApply, [('out', 'transforms')]),

    (synApply, write_name, [('output_image', 'in_file')]),

    # ==================================================================================
    # (synApply, datasink, [('output_image', 'func_filt_temp_space')]),



])


metaflow.write_graph(graph2use='colored', format='png', simple_form=True)

# for the cluster
if os_name == 'CentOS Linux':
    metaflow.run(plugin='SLURM', plugin_args={
        'dont_resubmit_completed_jobs': True, 'max_jobs': 50})

# for the laptop
elif os_name == 'Ubuntu':
    metaflow.run('MultiProc', plugin_args={'n_procs': 8})

# for the iMac
elif os_name == 'Darwin':
    metaflow.run('MultiProc', plugin_args={'n_procs': 8})
