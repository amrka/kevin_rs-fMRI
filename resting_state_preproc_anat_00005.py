# In[1]:
# >>> python resting_state_preproc_anat_00005.py <directory of Kevin>
import re
import os
import sys
import glob
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
# In[2]:
# instead of having to change the script between different copmuters and os
# we pass the directory with the name from the bash
origin_dir = sys.argv[1]

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


output_dir = '{0}/Kevin/resting_state_preproc_anat_outputdir'.format(origin_dir)
working_dir = '{0}/Kevin/resting_state_preproc_anat_workingdir'.format(origin_dir)

resting_fmri_preproc_anat = Workflow(name='resting_fmri_preproc_anat')
resting_fmri_preproc_anat.base_dir = opj(experiment_dir, working_dir)

# =====================================================================================================
# In[3]:
# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id']),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list)]


# -----------------------------------------------------------------------------------------------------
# In[4]:

# anatomical images
templates_anat = {
    'anat': 'raw_data_bids/{subject_id}/anat/sub-{subject_id}_X*_T2w.nii.gz'
}

selectfiles_anat = Node(SelectFiles(templates_anat,
                                    base_directory=experiment_dir),
                        name="selectfiles_anat")
# ========================================================================================================
# In[5]:

datasink = Node(DataSink(), name='datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_subject_id_', '')]
datasink.inputs.substitutions = substitutions


# fsl.FSLCommand.set_default_output_type('NIFTI') #very stupid idea, it will inflate the size of the folder


# ========================================================================================================
# In[6]:

# todo: solve the issue with the template
template_brain = '{0}/Kevin/std_master.nii'.format(origin_dir)
template_mask = '{0}/Kevin/std_master_mask.nii'.format(origin_dir)

# =======================================================================================================
# In[8]:

biasfield_correction_anat = Node(ants.N4BiasFieldCorrection(), name='biasfield_correction_anat')
biasfield_correction_anat.inputs.dimension = 3
biasfield_correction_anat.inputs.save_bias = True
# biasfield_correction_anat.inputs.output_image = 'anat_bet_biasfield_corrected.nii.gz' #better not to,
# it confuses the Registration
# =======================================================================================================
# In[8]:

brain_extraction_anat = Node(fsl.BET(), name='brain_extraction_anat')
brain_extraction_anat.inputs.mask = True
brain_extraction_anat.inputs.frac = 0.5


# ========================================================================================================
# In[13]:

# normalizing the anatomical_bias_corrected image to the common anatomical template
# Here only we are calculating the paramters, we apply them later.
# I will not use this function here, I will create a seperate anatomical pipeline
# I just left it in order not to break the clone

reg_T1_2_temp = Node(ants.Registration(), name='reg_T1_2_temp')
reg_T1_2_temp.inputs.args = '--float'
reg_T1_2_temp.inputs.collapse_output_transforms = True
reg_T1_2_temp.inputs.fixed_image = template_brain
reg_T1_2_temp.inputs.initial_moving_transform_com = True
reg_T1_2_temp.inputs.num_threads = 8
reg_T1_2_temp.inputs.output_inverse_warped_image = True
reg_T1_2_temp.inputs.output_warped_image = True
reg_T1_2_temp.inputs.sigma_units = ['vox']*3
reg_T1_2_temp.inputs.transforms = ['Rigid', 'Affine', 'SyN']
reg_T1_2_temp.inputs.winsorize_lower_quantile = 0.005
reg_T1_2_temp.inputs.winsorize_upper_quantile = 0.995
reg_T1_2_temp.inputs.convergence_threshold = [1e-08, 1e-08, 1e-08]
reg_T1_2_temp.inputs.convergence_window_size = [10, 10, 10]
reg_T1_2_temp.inputs.metric = ['MI', 'MI', 'CC']
reg_T1_2_temp.inputs.metric_weight = [1.0]*3
reg_T1_2_temp.inputs.number_of_iterations = [[1000, 500, 250, 100],
                                             [1000, 500, 250, 100],
                                             [100, 70, 50, 20]]
reg_T1_2_temp.inputs.radius_or_number_of_bins = [32, 32, 4]
reg_T1_2_temp.inputs.sampling_percentage = [0.25, 0.25, 1]
reg_T1_2_temp.inputs.sampling_strategy = ['Regular',
                                          'Regular',
                                          'None']
reg_T1_2_temp.inputs.shrink_factors = [[8, 4, 2, 1]]*3
reg_T1_2_temp.inputs.smoothing_sigmas = [[3, 2, 1, 0]]*3
reg_T1_2_temp.inputs.transform_parameters = [(0.1,),
                                             (0.1,),
                                             (0.1, 3.0, 0.0)]
reg_T1_2_temp.inputs.use_histogram_matching = True
reg_T1_2_temp.inputs.write_composite_transform = True
reg_T1_2_temp.inputs.verbose = True
reg_T1_2_temp.inputs.output_warped_image = True
reg_T1_2_temp.inputs.float = True

# ========================================================================================================
# Using affine reg with FLIRT in parallel, NOT IN PLACE OF antsREgistration (previsou command)
# so I can compare the output
# the performance of FLIRT affine is better than antsRegistration affine
flirt_aff_T1_2_temp = Node(fsl.FLIRT(), name='flirt_aff_T1_2_temp')
flirt_aff_T1_2_temp.inputs.reference = template_brain
flirt_aff_T1_2_temp.inputs.cost = 'corratio'
flirt_aff_T1_2_temp.inputs.bins = 256
flirt_aff_T1_2_temp.inputs.searchr_x = [-90, 90]
flirt_aff_T1_2_temp.inputs.searchr_y = [-90, 90]
flirt_aff_T1_2_temp.inputs.searchr_z = [-90, 90]
flirt_aff_T1_2_temp.inputs.dof = 12
flirt_aff_T1_2_temp.inputs.interp = 'trilinear'

# ========================================================================================================
resting_fmri_preproc_anat.connect([


    (infosource, selectfiles_anat, [('subject_id', 'subject_id')]),

    (selectfiles_anat, biasfield_correction_anat, [('anat', 'input_image')]),
    (biasfield_correction_anat, brain_extraction_anat, [('output_image', 'in_file')]),
    (brain_extraction_anat, reg_T1_2_temp, [('out_file', 'moving_image')]),

    (brain_extraction_anat, flirt_aff_T1_2_temp, [('out_file', 'in_file')]),
    # # ======================================datasink============================================
    # (Add_Mean_Image, datasink, [('out_file', 'preproc_img')]),
    # # does not work for this particular node
    # (coreg, datasink, [('composite_transform', 'func_2_anat_transformations')]),
    #
    # (brain_extraction_roi, datasink, [('out_file', 'bold_brain')]),
    #
    #
    # (erode_anat, datasink, [('out_file', 'anat_brain')]),
    # (reg_T1_2_temp, datasink, [('composite_transform', 'anat_2_temp_transformations'),
    #                            ('warped_image', 'anat_2_temp_image')]),
    #
    # (melodic, datasink, [('out_dir', 'melodic')])

])

resting_fmri_preproc_anat.write_graph(graph2use='colored', format='png', simple_form=True)

# resting_fmri_preproc_anat.run(plugin='SLURM', plugin_args={
#                               'dont_resubmit_completed_jobs': True, 'max_jobs': 50})
resting_fmri_preproc_anat.run('MultiProc', plugin_args={'n_procs': 8})
