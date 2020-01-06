#!/bin/bash

if test "$#" -ne 0; then
    echo "Usage: ./merlin_synthesis.sh"
    exit 1
fi

global_config_file=conf/global_settings.cfg

if [ ! -f  $global_config_file ]; then
    echo "Please run steps from 1-5..."
    exit 1
else
    source $global_config_file
fi

### define few variables here
testDir=experiments/${Voice}/test_synthesis

### Step 2: synthesize speech   ###
echo "Step 2: synthesizing speech..."
./scripts/submit.sh ${MerlinDir}/src/run_merlin.py conf/test_dur_synth_${Voice}.conf
./scripts/submit.sh ${MerlinDir}/src/run_merlin.py conf/test_synth_${Voice}.conf

echo "deleting intermediate synthesis files..."
./scripts/remove_intermediate_files.sh $global_config_file

echo "synthesized audio files are in: experiments/${Voice}/test_synthesis/wav"

