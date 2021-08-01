# In[1]:
# >>> python resting_state_preproc_func_00006.py <directory of Kevin>
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
                # 'A231120',
                # 'A251120',
                # 'A301020',
                # 'B201120',
                # 'B261020',
                # 'A031120',
                # 'A061120',
                # 'A241120',
                # 'A271020',
                # 'B191120',
                # 'B231020'
                ]



run_list = ['run-01',
            'run-02']


output_dir =  '{0}/Kevin/resting_state_preproc_outputdir'.format(origin_dir)
working_dir = '{0}/Kevin/resting_state_preproc_workingdir'.format(origin_dir)

resting_fmri_preproc = Workflow(name='resting_fmri_preproc')
resting_fmri_preproc.base_dir = opj(experiment_dir, working_dir)

# =====================================================================================================
# In[3]:
# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id','run_id']),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list),
                             ('run_id', run_list)]


# -----------------------------------------------------------------------------------------------------
# In[4]:

#anatomical images
templates_anat = {
'anat': 'resting_state_preproc_anat_workingdir/resting_fmri_preproc_anat/_subject_id_{subject_id}/brain_extraction_anat/sub-{subject_id}_X*_T2w_corrected_brain'
             }

selectfiles_anat = Node(SelectFiles(templates_anat,
                   base_directory=experiment_dir),
                   name="selectfiles_anat")

#functional runs
templates_func = {
'func': 'raw_data_bids/{subject_id}/func/sub-{subject_id}-X*-rs_bold_{run_id}.nii.gz'
             }

selectfiles_func = Node(SelectFiles(templates_func,
                   base_directory=experiment_dir),
                   name="selectfiles_func")
# ========================================================================================================
# In[5]:

datasink = Node(DataSink(), name='datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_subject_id_', ''), ('_blurfwhm_bx_by_bz_', 'fwhm-')]
#substitutions = [('_subject_id_', '')]
datasink.inputs.substitutions = substitutions


# fsl.FSLCommand.set_default_output_type('NIFTI') #very stupid idea, it will inflate the size of the folder


# ========================================================================================================
# In[6]:

#
template_brain = '{0}/Kevin/std_master.nii'.format(origin_dir)
template_mask = '{0}/Kevin/std_master_mask.nii'.format(origin_dir)
# custom maded template, see creating_rs_template_00002.sh script
epi_brain = '{0}/Kevin/rs-temp/epi_temp_snapped.nii.gz'.format(origin_dir)
epi_mask = '{0}/Kevin/rs-temp/epi_temp_mask.nii.gz'.format(origin_dir)

TR = 2.0

# =======================================================================================================
# In[9]:
# Extract one fmri image to use for brain extraction, the same one you will use for mcflirt as reference
roi = Node(fsl.ExtractROI(), name='extract_one_fMRI_volume')

roi.inputs.t_min = 450
roi.inputs.t_size = 1

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
reg_T1_2_temp.inputs.num_threads = 4
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
# In[14]:
coreg = reg_T1_2_temp.clone(name='coregistration')
coreg.inputs.transforms = ['Rigid']
coreg.inputs.metric = ['GC']
# ========================================================================================================
# In[15]:
# mcflirt -in ${folder} -out ${folder}_mcf  -refvol example_func -plots -mats  -report;

McFlirt = Node(fsl.MCFLIRT(), name='McFlirt')
McFlirt.inputs.save_plots = True
McFlirt.inputs.save_mats = True
McFlirt.inputs.save_rms = True


# ========================================================================================================
# In[16]:

# Getting motion parameters from Mcflirt and plotting them

def Plot_Motion(motion_par, rms_files):

    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('Agg')

    movement = np.loadtxt(motion_par)
    abs_disp = np.loadtxt(rms_files[0])
    rel_disp = np.loadtxt(rms_files[1])
    plt.figure(figsize=(8, 10), dpi=300)

    plt.subplot(311)
    plt.title('Translations in mm')
    plt.plot(movement[:, :3])
    plt.legend(['x', 'y', 'z'])

    plt.subplot(312)
    plt.title('Rotations in radians')
    plt.plot(movement[:, 3:])
    plt.legend(['x', 'y', 'z'])

    plt.subplot(313)
    plt.title('Displacement in mm')
    plt.plot(abs_disp)
    plt.plot(rel_disp)
    plt.legend(['abs', 'rel'])

    plt.savefig('Motion')


Plot_Motion = Node(name='Plot_Motion',
                   interface=Function(input_names=['motion_par', 'rms_files'],
                                      function=Plot_Motion))

# =======================================================================================================

#Remove skull using antsBrainExtraction.sh, i am using the epi study-based template that I build and remove
#the skull manually using ITKsnap
brain_extraction_roi = Node(ants.BrainExtraction(), name='brain_extraction_roi')
brain_extraction_roi.inputs.dimension = 3
brain_extraction_roi.inputs.brain_template = epi_brain
brain_extraction_roi.inputs.brain_probability_mask = epi_mask
brain_extraction_roi.inputs.num_threads = 4

# =======================================================================================================

# apply the mask from brain_extraction_roi to all 4D
brain_extraction_4D = Node(fsl.ApplyMask(), name='brain_extraction_4D')

# ========================================================================================================
# In[17]:

# apply the trasnfromation to all the EPI volumes

func_2_template = Node(ants.ApplyTransforms(), name='func_2_template')
func_2_template.inputs.dimension = 3

func_2_template.inputs.input_image_type = 3
func_2_template.inputs.num_threads = 1
func_2_template.inputs.float = True

# ========================================================================================================
# 2D smoothing
smoothing_2d = Node(afni.Merge(), name='smoothing_2d')
smoothing_2d.inputs.out_file = 'afni_2d_smoothed.nii.gz'
smoothing_2d.inputs.doall = True
smoothing_2d.iterables = ('blurfwhm_bx_by_bz', [[0, 0, 0], [6.5, 6.5, 6.5], [8, 8, 8], [6.5, 6.5, 0]])

# ========================================================================================================
# In[18]:

# Getting median intensity
Median_Intensity = Node(fsl.ImageStats(), name='Median_Intensity')
# Put -k before -p 50
Median_Intensity.inputs.op_string = '-k %s -p 50'

# Scale median intensity


def Scale_Median_Intensity(median_intensity):
    scaling = 10000/median_intensity
    return scaling


Scale_Median_Intensity = Node(name='Scale_Median_Intensity',
                              interface=Function(input_names=['median_intensity'],
                                                 output_names=['scaling'],
                                                 function=Scale_Median_Intensity))
# ========================================================================================================
# In[20]:

# Global Intensity Normalization by multiplying by the scaling value
# the grand-mean intensity normalisation factor ( to give a median brain intensity of 10000 )
# grand mean scaling
Intensity_Normalization = Node(fsl.BinaryMaths(), name='Intensity_Normalization')
Intensity_Normalization.inputs.operation = 'mul'

# ========================================================================================================
# In[21]:

#   fslmaths ${folder}_mcf_2highres_intnorm -bptf 25 -1 -add tempMean ${folder}_mcf_2highres_tempfilt;
# sigma[vol] = filter_width[secs]/(2*TR[secs])
high_pass_filter = Node(fsl.TemporalFilter(), name='high_pass_filter')
high_pass_filter.inputs.highpass_sigma = 25  # 100s / (2*2(TR))
# ========================================================================================================
# In[22]

# Get the mean image
Get_Mean_Image = Node(fsl.MeanImage(), name='Get_Mean_Image')
Get_Mean_Image.inputs.dimension = 'T'

# Add the mean image to the filtered image
Add_Mean_Image = Node(fsl.BinaryMaths(), name='Add_Mean_Image')
Add_Mean_Image.inputs.operation = 'add'


# ========================================================================================================
# In[23]:

melodic = Node(fsl.MELODIC(), name='Melodic')
melodic.inputs.out_dir = 'melodic.ica'
melodic.inputs.approach = 'concat'
melodic.inputs.no_bet = True
melodic.inputs.bg_threshold = 10.0
melodic.inputs.tr_sec = 2.00
melodic.inputs.mm_thresh = 0.5
melodic.inputs.out_all = True
melodic.inputs.report = True
melodic.iterables = ('dim', [15, 20, 25])


# ========================================================================================================
# In[24]:


resting_fmri_preproc.connect([


    (infosource, selectfiles_anat,[('subject_id','subject_id')]),
    (infosource, selectfiles_func, [('subject_id','subject_id'),
                                    ('run_id','run_id')]),

    (selectfiles_func, roi, [('func', 'in_file')]),

    (selectfiles_func, McFlirt, [('Func', 'in_file')]),
    (roi, McFlirt, [('roi_file', 'ref_file')]),
    #
    (McFlirt, Plot_Motion, [('par_file', 'motion_par'),
                            ('rms_files', 'rms_files')]),

    (roi, brain_extraction_roi, [('roi_file','anatomical_image')]),
    #
    (brain_extraction_roi, coreg, [('BrainExtractionBrain', 'moving_image')]),
    (selectfiles_anat, coreg, [('anat', 'fixed_image')]),

    (McFlirt, brain_extraction_4D, [('out_file','in_file')]),
    (brain_extraction_roi, brain_extraction_4D, [('BrainExtractionMask','mask_file')]),


    (brain_extraction_4D, smoothing_2d, [('out_file', 'in_files')]),
    #
    #
    (brain_extraction_4D, Median_Intensity, [('out_file', 'in_file')]),
    (brain_extraction_roi, Median_Intensity, [('BrainExtractionMask', 'mask_file')]),

    (Median_Intensity, Scale_Median_Intensity, [('out_stat', 'median_intensity')]),

    (Scale_Median_Intensity, Intensity_Normalization, [('scaling', 'operand_value')]),
    (smoothing_2d, Intensity_Normalization, [('out_file', 'in_file')]),


    (Intensity_Normalization, Get_Mean_Image, [('out_file', 'in_file')]),
    (Intensity_Normalization, high_pass_filter, [('out_file', 'in_file')]),

    (high_pass_filter, Add_Mean_Image, [('out_file', 'in_file')]),
    (Get_Mean_Image, Add_Mean_Image, [('out_file', 'operand_file')]),

    (Add_Mean_Image, melodic, [('out_file', 'in_files')]),

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

resting_fmri_preproc.write_graph(graph2use='colored', format='png', simple_form=True)

# resting_fmri_preproc.run(plugin='SLURM',plugin_args={'dont_resubmit_completed_jobs': True, 'max_jobs':50})
resting_fmri_preproc.run('MultiProc', plugin_args={'n_procs': 8})
