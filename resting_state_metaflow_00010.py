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
    'anat': 'resting_state_preproc_anat_workingdir/resting_fmri_preproc_anat/'
            '_subject_id_{subject_id}/brain_extraction_anat/sub-{subject_id}_X*_T2w_corrected_brain.nii.gz',

    'Filtered_Smoothed_rs_fMRI': 'resting_state_preproc_func_workingdir/resting_fmri_preproc_func/'
                                 '_run_id_{run_id}_subject_id_{subject_id}/_blurfwhm_bx_by_bz_6.5.6.5.6.5/Add_Mean_Image/'
                                 'afni_2d_smoothed_maths_filt_maths.nii.gz',

    'Melodic_Mix': 'resting_state_preproc_func_workingdir/resting_fmri_preproc_func/'
                   '_run_id_{run_id}_subject_id_{subject_id}/_blurfwhm_bx_by_bz_6.5.6.5.6.5/_dim_25/Melodic/melodic.ica/'
                   'melodic_mix',

    'labels': 'ICA_labels/{subject_id}_{run_id}.txt',

    'coreg_trans': 'resting_state_preproc_func_workingdir/resting_fmri_preproc_func/'
                   '_run_id_{run_id}_subject_id_{subject_id}/coregistration/transformComposite.h5',

    'syn_2_temp': 'resting_state_preproc_anat_workingdir/resting_fmri_preproc_anat/'
                  '_subject_id_{subject_id}/reg_T1_2_temp/transformComposite.h5',

    'affine_2_temp': 'resting_state_preproc_anat_workingdir/resting_fmri_preproc_anat/'
                   '_subject_id_{subject_id}/flirt_aff_T1_2_temp/sub-{subject_id}_X*_T2w_corrected_brain_flirt.mat',


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
    components_list = components_str[1:-2].split()

    components_int_list = []
    for element in components_list:
        element = element.replace(',', '')
        components_int_list.append(int(element))

    print(components_int_list)
    return components_int_list


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
# you will have to apply coreg ants trans first
affine_flirt_Apply = Node(fsl.ApplyXFM(), name='affine_flirt_Apply')
affine_flirt_Apply.inputs.reference = template_brain
affine_flirt_Apply.inputs.apply_xfm = True
affine_flirt_Apply.inputs.cost = 'corratio'
affine_flirt_Apply.inputs.bins = 256
affine_flirt_Apply.inputs.searchr_x = [-180, 180]
affine_flirt_Apply.inputs.searchr_y = [-180, 180]
affine_flirt_Apply.inputs.searchr_z = [-180, 180]
affine_flirt_Apply.inputs.dof = 12
affine_flirt_Apply.inputs.interp = 'trilinear'

# =====================================================================================================
# In[9]:
coreg_ants_Apply = Node(ants.ApplyTransforms(), name='coreg_ants_Apply')
coreg_ants_Apply.inputs.dimension = 3

coreg_ants_Apply.inputs.input_image_type = 3
coreg_ants_Apply.inputs.num_threads = 1
coreg_ants_Apply.inputs.float = True

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
    import sys
    import distro
    if distro.name() == 'CentOS Linux':
        # using command line argument inside a node is not going to work with SLURM
        f = open(
            '/home/in/aeed/Work/Kevin/resting_state_metaflow_workingdir/melodic_list_october_acquistions.txt', 'a+')
        print(in_file)
        f.write('\n' + in_file)
        f.close()
    else:
        f = open(
            '{0}/Kevin/resting_state_metaflow_workingdir/melodic_list_october_acquistions.txt'.format(sys.argv[1]), 'a+')
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

    (selectfiles, get_bad_components, [('labels', 'labels')]),

    (get_bad_components, regfilt, [('components_list', 'filter_columns')]),
    (selectfiles, regfilt, [('Filtered_Smoothed_rs_fMRI', 'in_file')]),
    (selectfiles, regfilt, [('Melodic_Mix', 'design_file')]),




    (selectfiles, merge_transforms, [('syn_2_temp', 'in1')]),
    (selectfiles, merge_transforms, [('coreg_trans', 'in2')]),


    (regfilt, synApply, [('out_file', 'input_image')]),
    (merge_transforms, synApply, [('out', 'transforms')]),

    (synApply, write_name, [('output_image', 'in_file')]),


    (regfilt, coreg_ants_Apply, [('out_file', 'input_image')]),
    (selectfiles, coreg_ants_Apply, [('coreg_trans', 'transforms'),
                                     ('anat', 'reference_image')]),

    (coreg_ants_Apply, affine_flirt_Apply, [('output_image', 'in_file')]),
    (selectfiles, affine_flirt_Apply, [('affine_2_temp', 'in_matrix_file')])


    # ==================================================================================
    # (synApply, datasink, [('output_image', 'func_filt_temp_space')]),



])


metaflow.write_graph(graph2use='colored', format='png', simple_form=True)

# for the cluster
if os_name == 'CentOS Linux':
    metaflow.run(plugin='SLURM', plugin_args={
        'dont_resubmit_completed_jobs': True, 'max_jobs': 50, 'sbatch_args': '--mem=40G'})

# for the laptop
elif os_name == 'Ubuntu':
    metaflow.run('MultiProc', plugin_args={'n_procs': 8})

# for the iMac
elif os_name == 'Darwin':
    metaflow.run('MultiProc', plugin_args={'n_procs': 8})
