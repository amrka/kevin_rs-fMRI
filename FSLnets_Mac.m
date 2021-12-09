% Set up FSL environment
setenv( 'FSLDIR', '/usr/local/fsl');
fsldir = getenv('FSLDIR');
fsldirmpath = sprintf('%s/etc/matlab',fsldir);
path(path, fsldirmpath);
clear fsldir fsldirmpath;


addpath /Users/aeed/Downloads/FSLNets              % wherever you've put this package
addpath /Users/aeed/Downloads/L1precision            % L1precision toolbox
addpath /Users/aeed/Downloads/pwling                 % pairwise causality toolbox
addpath(sprintf('%s/etc/matlab',getenv('FSLDIR')))
%%
n_dims = 20
% sess = "d0f02a8721eff087f281113015c672685b8a198b"    % run1
sess = "43ddee1b109476bbf41ba6bf431ef9eefb2055bd" % run2

if sess == "d0f02a8721eff087f281113015c672685b8a198b"
  run = 1
elseif  sess == "43ddee1b109476bbf41ba6bf431ef9eefb2055bd"
  run = 2
end

system('n_dims=20; dir=/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_${n_dims}/melodic_group/;/Users/aeed/Documents/Kevin/kevin_rs-fMRI/slices_summary ${dir}melodic_IC 3 /Users/aeed/Documents/Kevin/std_master.nii ${dir}melodic_IC.sum -1')

group_maps="/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + n_dims + "/melodic_group/melodic_IC";     % spatial maps 4D NIFTI file, e.g. from group-ICA No extension needed
   %%% you must have already run the following (outside MATLAB), to create summary pictures of the maps in the NIFTI file:
   %%% slices_summary <group_maps> 4 $FSLDIR/data/standard/MNI152_T1_2mm <group_maps>.sum
% run-01
ts_dir="/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + n_dims + "/" + sess + "/dual_regression/output";                           % dual regression output directory, containing all subjects' timeseries

%%%% [tail: illegal offset -- +] error can be avoided by adding -1 to summary_slices command
%%% it will return one slice image per component instead of three, but here will be no errors
%%% adding -d flag does not pan out very well, the template becomes way too much darker

%%% load timeseries data from the dual regression output directory
ts=nets_load(ts_dir,2,1);
   %%% arg2 is the TR (in seconds)
   %%% arg3 controls variance normalisation: 0=none, 1=normalise whole subject stddev, 2=normalise each separate timeseries from each subject
ts_spectra=nets_spectra(ts);   % have a look at mean timeseries spectra

%%
%%% cleanup and remove bad nodes' timeseries (whichever is NOT listed in ts.DD is *BAD*).
% I wrote a txt file with good components and matched the dim with the line number, so line 10 -> contains the good comp of dim 10 and so on
good_comps_file = '/Users/aeed/Documents/Kevin/kevin_rs-fMRI/good_components.txt';
good_comps = fileread(good_comps_file);
good_comps = regexp(good_comps,'\n','split');

ts.DD=str2num(good_comps{n_dims});  % list the good nodes in your group-ICA output (counting starts at 1, not 0)
% ts.UNK=[10];  optionally setup a list of unknown components (where you're unsure of good vs bad)
ts=nets_tsclean(ts,1);                   % regress the bad nodes out of the good, and then remove the bad nodes' timeseries (1=aggressive, 0=unaggressive (just delete bad)).
                                         % For partial-correlation netmats, if you are going to do nets_tsclean, then it *probably* makes sense to:
                                         %    a) do the cleanup aggressively,
                                         %    b) denote any "unknown" nodes as bad nodes - i.e. list them in ts.DD and not in ts.UNK
                                         %    (for discussion on this, see Griffanti NeuroImage 2014.)
nets_nodepics(ts,group_maps);            % quick views of the good and bad components
ts_spectra=nets_spectra(ts);             % have a look at mean spectra after this cleanup

%%
%%% create various kinds of network matrices and optionally convert correlations to z-stats.
%%% here's various examples - you might only generate/use one of these.
%%% the output has one row per subject; within each row, the net matrix is unwrapped into 1D.
%%% the r2z transformation estimates an empirical correction for autocorrelation in the data.
%netmats0=  nets_netmats(ts,0,'cov');        % covariance (with variances on diagonal)
%netmats0a= nets_netmats(ts,0,'amp');        % amplitudes only - no correlations (just the diagonal)
netmats_F=  nets_netmats(ts,1,'corr');       % full correlation (normalised covariances)
netmats_P=  nets_netmats(ts,1,'icov');       % partial correlation
netmats_rP=  nets_netmats(ts,1,'ridgep', 0.1);     % Ridge Regression partial, with rho=0.1

% netmats3=  nets_netmats(ts,1,'icov',10);    % L1-regularised partial, with lambda=10

%netmats11= nets_netmats(ts,0,'pwling');     % Hyvarinen's pairwise causality measure
%%
% save matrices fro future use

save("/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + n_dims + "/melodic_group/run-" + run + "_dim_" + n_dims + "_netmats_F.mat", 'netmats_F')
save("/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + n_dims + "/melodic_group/run-" + run + "_dim_" + n_dims + "_netmats_P.mat", 'netmats_P')
save("/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + n_dims + "/melodic_group/run-" + run + "_dim_" + n_dims + "_netmats_rP.mat", 'netmats_rP')

% save('/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + n_dims + "/melodic_group/run-" + run + "_dim_" + n_dims + "_netmats3.mat', 'netmats3')
%%
%%% view of consistency of netmats across subjects; returns t-test Z values as a network matrix
%%% second argument (0 or 1) determines whether to display the Z matrix and a consistency scatter plot
%%% third argument (optional) groups runs together; e.g. setting this to 4 means each group of 4 runs were from the same subject
[Znet_F,Mnet_F]=nets_groupmean(netmats_F,1);      % test whichever netmat you're interested in; returns Z values from one-group t-test and group-mean netmat
[Znet_P,Mnet_P]=nets_groupmean(netmats_P,1);      % test whichever netmat you're interested in; returns Z values from one-group t-test and group-mean netmat
[Znet_rP,Mnet_rP]=nets_groupmean(netmats_rP,1);   % test whichever netmat you're interested in; returns Z values from one-group t-test and group-mean netmat


% [Znet3,Mnet3]=nets_groupmean(netmats3,1);   % test whichever netmat you're interested in; returns Z values from one-group t-test and group-mean netmat
%%
%%% view hierarchical clustering of nodes
%%% arg1 is shown below the diagonal (and drives the clustering/hierarchy); arg2 is shown above diagonal
% it was not working on mac (it shows the hierarchy without the components pics), but worked on linux, becaause the versions of fslnets were different
% obivously in Mac's more recent version, the nets_hierarchy.m script was changed and requires 3 slices images
% the problem was resolved once I replaced that version of nets_hierarchy with the linux one (the other one is renamed _net_hierarchy.m )
nets_hierarchy(Znet_F,Znet_P,ts.DD,"/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + n_dims + "/melodic_group/melodic_IC");
nets_hierarchy(Znet_F,Znet_rP,ts.DD,"/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + n_dims + "/melodic_group/melodic_IC");
nets_hierarchy(Znet_P,Znet_rP,ts.DD,"/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + n_dims + "/melodic_group/melodic_IC");


%%% view interactive netmat web-based display
% for this to work, you need to install XAMPP, and save the index.html in /Applications/XAMPP/htdocs
% it goes without saying, but you need to start the Apache Web Server
% another option without XAMPP, is to navigate to the folder where the index.html is located
% >>> >>> python -m http.server
% then go to the webbrowser and type http://localhost:8000/
% http://127.0.0.1:8000/ sometimes work better
nets_netweb(Znet_F,Znet_P,ts.DD,"/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + n_dims + "/melodic_group/melodic_IC","/Users/aeed/Documents/Kevin/FSLNets_pics/run-" + run + "_dim_" + n_dims + "_netweb_F_P");
nets_netweb(Znet_F,Znet_rP,ts.DD,"/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + n_dims + "/melodic_group/melodic_IC","/Users/aeed/Documents/Kevin/FSLNets_pics/run-" + run + "_dim_" + n_dims + "_netweb_F_rP");


%%% cross-subject GLM, with inference in randomise (assuming you already have the GLM design.mat and design.con files).
%%% arg4 determines whether to view the corrected-p-values, with non-significant entries removed above the diagonal.
%%
design = '/Users/aeed/Documents/Kevin/designs/kevin_design.mat'
contrast = '/Users/aeed/Documents/Kevin/designs/kevin_design.con'
% I adjusted the number of permutations to 10000 from nets_glm.m
[p_uncorrected_F,p_corrected_F]=nets_glm(netmats_F, design, contrast,1); %1 last argument is to show output or not
[p_uncorrected_P,p_corrected_P]=nets_glm(netmats_P, design, contrast,1);
[p_uncorrected_rP,p_corrected_rP]=nets_glm(netmats_rP, design, contrast,1);

% [p_uncorrected3,p_corrected3]=nets_glm(netmats3, design, contrast,1);

% returns matrices of 1-p
%%% OR - GLM, but with pre-masking that tests only the connections that are strong on average across all subjects.
%%% change the "8" to a different tstat threshold to make this sparser or less sparse.
%netmats=netmats3;  [grotH,grotP,grotCI,grotSTATS]=ttest(netmats);  netmats(:,abs(grotSTATS.tstat)<8)=0;
%[p_uncorrected,p_corrected]=nets_glm(netmats,'design.mat','design.con',1);
%
%%% view 6 most significant edges from this GLM
nets_edgepics(ts,group_maps,Znet_F,reshape(p_corrected_F(1,:),ts.Nnodes,ts.Nnodes),6); %
nets_edgepics(ts,group_maps,Znet_P,reshape(p_corrected_P(1,:),ts.Nnodes,ts.Nnodes),6);
nets_edgepics(ts,group_maps,Znet_rP,reshape(p_corrected_rP(1,:),ts.Nnodes,ts.Nnodes),6);

% nets_edgepics(ts,group_maps,Znet3,reshape(p_corrected3(1,:),ts.Nnodes,ts.Nnodes),6);


nets_edgepics(ts,group_maps,Znet_F,reshape(p_corrected_F(2,:),ts.Nnodes,ts.Nnodes),6); %
nets_edgepics(ts,group_maps,Znet_P,reshape(p_corrected_P(2,:),ts.Nnodes,ts.Nnodes),6);
nets_edgepics(ts,group_maps,Znet_rP,reshape(p_corrected_rP(2,:),ts.Nnodes,ts.Nnodes),6);

% nets_edgepics(ts,group_maps,Znet3,reshape(p_corrected3(2,:),ts.Nnodes,ts.Nnodes),6);
%%
%%% simple cross-subject multivariate discriminant analyses, for just two-group cases.
%%% arg1 is whichever netmats you want to test.
%%% arg2 is the size of first group of subjects; set to 0 if you have two groups with paired subjects.
%%% arg3 determines which LDA method to use (help nets_lda to see list of options)
[lda_percentages]=nets_lda(netmats_F,14,7)
[lda_percentages]=nets_lda(netmats_P,14,7)
[lda_percentages]=nets_lda(netmats_rP,14,7)

% [lda_percentages]=nets_lda(netmats3,14,7)


%%% create boxplots for the two groups for a network-matrix-element of interest (e.g., selected from GLM output)
%%% arg3 = matrix row number,    i.e. the first  component of interest (from the DD list)
%%% arg4 = matrix column number, i.e. the second component of interest (from the DD list)
%%% arg5 = size of the first group (set to -1 for paired groups)

%% third argument is number of subjects in gp 1
nets_boxplots(ts,netmats_F,14,7,16);
nets_boxplots(ts,netmats_P,14,7,16);
nets_boxplots(ts,netmats_rP,14,7,16);

%print('-depsc',sprintf('boxplot-%d-%d.eps',IC1,IC2));  % example syntax for printing to file
%%
% get the two groups variable that are used to construct the boxplots
IC1=14, IC2=7
Ngroup1 = 16 %number of animals in group 1
netmat= netmats_rP


i=(IC1-1)*ts.Nnodes + IC2;

% get values for boxplots, padding with NaN for unequal groups (otherwise boxplot doesn't work)
grot1=netmat(1:Ngroup1,i); grot2=netmat(Ngroup1+1:end,i);
grotl=max(length(grot1),length(grot2));
grot1=[grot1;nan(grotl-length(grot1),1)]; grot2=[grot2;nan(grotl-length(grot2),1)];
grot_both = [grot1, grot2]
%csvwrite('/Users/aeed/Dropbox/thesis/resting/FSLNets_pics/regularized_partial_corr_14_7.csv', grot_both)
