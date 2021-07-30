#!/bin/bash

cd /Volumes/Amr_1TB/Kevin/raw_data_bids

for folder in *;do
    cd $folder
    cd func
    echo $folder
    python3 /Volumes/Amr_1TB/Kevin/kevin_rs-fMRI/add_run_number_00003.py .

    cd ..
    cd ..
done
