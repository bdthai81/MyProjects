############################################
# Data Wrangling: transforming raw to 44100 sample rate audio .wav files
# Run python3 script with the folder of audio files path you wish to convert to wave files.
# This app will create a subfolder that will contain all the converted audio files
# python3 convertToWave.py <folder_dir_path_1> <folder_dir_path_2> 
############################################

# import modules
import sys
import os

# Variables
# sample rate: 44100 hz is standard range use for speech systems
set_sample_rate = 44100
# set the list of directory paths to convert
dirpath_list = sys.argv[1:]
# set results subfolder name
subfolder_name = "results"

# Convert audio files
for dirpath in dirpath_list:
    # load files within directory
    files = os.listdir(dirpath)    
    files_mp3 = [f for f in files if f[-3:] == 'mp3']
    files_wav = [f for f in files if f[-3:] == 'wav']

    # create subdirectory to store converted files
    if not os.path.exists(f"{dirpath}/{subfolder_name}"):
        os.makedirs(f"{dirpath}/{subfolder_name}")
    
    print(f"Converting {len(files_mp3)} mp3 & {len(files_wav)} wav files in the directory: {dirpath}")
    for file_name in files_mp3:
        os.system(f'ffmpeg -i "{dirpath}/{file_name}" -ar {set_sample_rate} "{dirpath}/{subfolder_name}/{file_name[:-4]}.wav"')
    for file_name in files_wav:
        os.system(f'ffmpeg -i "{dirpath}/{file_name}" -ar {set_sample_rate} "{dirpath}/{subfolder_name}/{file_name[:-4]}.wav"')