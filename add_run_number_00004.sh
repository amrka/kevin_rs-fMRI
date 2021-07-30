#!/bin/bash

cd /home/in/aeed/Work/Kevin/raw_data_bids

for folder in *;do
    cd $folder
    cd func
    echo $folder
    python /home/in/aeed/Work/Kevin/kevin_rs-fMRI/add_run_number_00003.py .

    cd ..
    cd ..
done
