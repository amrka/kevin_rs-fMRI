% subtract timeseries from the 2 runs before and after

% dlmread()
% writematrix(A, filename)

% /Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + dims +"/43ddee1b109476bbf41ba6bf431ef9eefb2055bd/dual_regression/output/dr_stage1_subject00001.txt

% /Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + dims +"/d0f02a8721eff087f281113015c672685b8a198b/dual_regression/output/dr_stage1_subject00001.txt

dimensions = [10, 15, 20, 25, 40, 50, 100]

for dims = dimensions
  run_02_folder = "/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + dims +"/43ddee1b109476bbf41ba6bf431ef9eefb2055bd/dual_regression/output"

  run_01_folder = "/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + dims +"/d0f02a8721eff087f281113015c672685b8a198b/dual_regression/output"

  timeseries = dir(fullfile(run_02_folder,'*.txt'));
  k = 0
  for k = 1:length(timeseries)
      baseFileName = timeseries(k).name;
      run_02_ts = dlmread("/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + dims +"/43ddee1b109476bbf41ba6bf431ef9eefb2055bd/dual_regression/output/" + baseFileName)


      run_01_ts = dlmread("/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + dims +"/d0f02a8721eff087f281113015c672685b8a198b/dual_regression/output/" + baseFileName)

      subtract_ts = run_02_ts - run_01_ts


      writematrix(subtract_ts, "/Users/aeed/Documents/Kevin/resting_state_melodic/melodic_workflow/_subject_id_ants/_dim_" + dims +"/subtract/dual_regression/output/" + baseFileName, 'Delimiter','space')
  end
end
