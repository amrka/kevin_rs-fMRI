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
cfg = dict(execution={'remove_unnecessary_outputs': False,
                      'parameterize_dirs': False})  # to hash long names
config.update_config(cfg)


MatlabCommand.set_default_paths('/Users/amr/Downloads/spm12')
MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")


# -----------------------------------------------------------------------------------------------------
# type help message in case of no input from the command line


def help_message():
    print("""Input argument missing \n
    >>> python resting_state_palm_00016.py <directory of Kevin> \n
    Examples (from different OS):
    >>> python resting_state_palm_00016.py /Volumes/Amr_1TB
    >>> python resting_state_palm_00016.py /home/in/aeed/Work
    >>> python resting_state_palm_00016.py /media/amr/Amr_4TB/Work
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


dim_list = ['dim_10', 'dim_15', 'dim_20', 'dim_25', 'dim_40', 'dim_50', 'dim_100']

run_list = ['run-01', 'run-02']
palm_workflow = Workflow(name='palm_workflow')

palm_workflow.base_dir = opj(experiment_dir, working_dir)


datasink_palm = Node(DataSink(), name='datasink_palm')
datasink_palm.inputs.container = output_dir
datasink_palm.inputs.base_directory = experiment_dir
datasink_palm.inputs.parameterization = False

# =====================================================================================================
# In[3]:
# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['dim_id', 'run_id']),
                  name="infosource")
infosource.iterables = [('dim_id', dim_list),
                        ('run_id', run_list)]
# =====================================================================================================

templates = {
    'palm_list': 'palm_ants/{run_id}/{dim_id}/palm_{dim_id}_{run_id}.txt',
}

selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir),
                   name="selectfiles")
# ====================================================================================================


def palm(palm_list, origin_dir):
    import os
    import glob
    from nipype.interfaces.base import CommandLine

    design = '{0}/Kevin/designs/kevin_design.mat'.format(origin_dir)
    contrast = '{0}/Kevin/designs/kevin_design.con'.format(origin_dir)
    template_mask = '{0}/Kevin/std_master_mask.nii'.format(origin_dir)

 # that is the correct mask
    cmd = ("palm {palm_list} \
    -m {template_mask} \
    -d {design} -t {contrast} \
    -T -noniiclass -n 100 -corrcon -corrmod -save1-p -nouncorrected -o dr_stage3")
    # start with 5000 like the rest of resting state

    cl = CommandLine(cmd.format(design=design, contrast=contrast))
    cl.run()

    P_values = []
    for file in glob.glob(os.path.abspath('dr_stage3_tfce_tstat_mfwep_*')):
        P_values.append(file)
    return P_values


palm = Node(name='palm',
                 interface=Function(input_names=['palm_list'],
                                    output_names=['P_values'],
                                    function=palm))

# ====================================================================================================
palm_workflow.connect([

    (infosource, selectfiles, [('dim_id', 'dim_id'),
                               ('run_id', 'run_id')]),

    (selectfiles, palm, [('palm_list', 'palm_list')])

])

palm_workflow.write_graph(graph2use='colored', format='png', simple_form=True)

# for the cluster
if os_name == 'CentOS Linux':
    palm_workflow.run(plugin='SLURM', plugin_args={
        'dont_resubmit_completed_jobs': True, 'max_jobs': 50})

# for the laptop
elif os_name == 'Ubuntu':
    palm_workflow.run('MultiProc', plugin_args={'n_procs': 8})

# for the iMac
elif os_name == 'Darwin':
    palm_workflow.run('MultiProc', plugin_args={'n_procs': 8})
