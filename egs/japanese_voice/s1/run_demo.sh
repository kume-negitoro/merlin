#!/bin/bash
# usage: cd merlin/egs/japanese_voice/s1, then run `bash run_demo.sh`

train_tts=true
run_tts=true
logging_enabled=true
voice_name="japanese_voice"
demo_voice=jsut_ver1.1
demo_voice_rename=${demo_voice}_data
demo_voice_type=basic5000
data_url=http://ss-takashi.sakura.ne.jp/corpus/jsut_ver1.1.zip

demo_label=jsut-lab-0.1.0
demo_label_rename=${demo_label}_data
label_url=https://github.com/r9y9/jsut-lab/archive/v0.1.0.zip

if [ "$logging_enabled" = true ]; then
    exec > >(tee ${voice_name}_$(date '+%Y%m%d_%H-%M-%S').log) 2>&1
fi

if [ ! -d ${demo_voice_rename} ]; then

    if [ ! -f ${demo_voice_rename}.zip ]; then
        echo "downloading voice data......"
        wget $data_url -O ${demo_voice_rename}.zip
    fi

    unzip ${demo_voice_rename}.zip
    mv ${demo_voice} ${demo_voice_rename}
    mkdir -p database/wav
    cp ${demo_voice_rename}/${demo_voice_type}/wav/* database/wav
fi

if [ ! -d ${demo_label_rename} ]; then

    if [ ! -f ${demo_label_rename}.zip ]; then
        echo "downloading label data......"
        wget $label_url -O ${demo_label_rename}.zip
    fi

    unzip ${demo_label_rename}.zip
    mv ${demo_label} ${demo_label_rename}
    mkdir -p database/labels/label_phone_align
    cp ${demo_label_rename}/${demo_voice_type}/lab/* database/labels/label_phone_align

    rm -rf database/prompt-lab
    mkdir -p database/prompt-lab
    ls -1 database/labels/label_phone_align/* \
        | (xargs readlink -f) 2>/dev/null \
        | head -n 100 \
        | xargs -I % cp % database/prompt-lab
fi


# train tts system
if [ "$train_tts" = true ]; then
    # step 1: run setup and check data
    time ./01_setup.sh $voice_name

    # step 2: prepare labels
    time ./02_prepare_labels.sh database/labels database/prompt-lab

    if [ ! -d 'database/feats' ]; then
        # step 3: extract acoustic features
        time ./03_prepare_acoustic_features.sh database/wav database/feats
    else
        echo "---Step3 database/feats dir exists! skip this step!----"
    fi

    # step 4: prepare config files for training and testing
    time ./04_prepare_conf_files.sh conf/global_settings.cfg

    # step 5: train duration model
    time ./05_train_duration_model.sh conf/duration_${voice_name}.conf
    
    # step 6: train acoustic model
    time ./06_train_acoustic_model.sh conf/acoustic_${voice_name}.conf

fi

# run tts
if [ "$run_tts" = true ]; then

    # step 7: run text to speech
   time ./07_run_merlin.sh conf/test_dur_synth_${voice_name}.conf conf/test_synth_${voice_name}.conf

fi

echo "done...!"
