#!/bin/bash

cd /media/amr/Amr_4TB/Work/Kevin/raw_data_bids

for folder in *;do
    cd $folder
    cd func
    echo $folder
    python3 /media/amr/Amr_4TB/Work/Kevin/kevin_rs-fMRI/add_run_number_00003.py .

    cd ..
    cd ..
done
