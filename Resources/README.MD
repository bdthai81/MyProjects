Data Training/Exploration:
* https://www.tensorflow.org/tutorials/sequences/audio_recognition
    - 80% Training data, 10% validation, 10% testing
    - Need at least several hundred recordings of each sound you would like to recognize
    - Try to ensure that all clips featuring the same word spoken by a single person are put into the same partition.
    - By default 10% of the training examples are picked from the unknown classes (negatives).
    - Mix in random background noise
    - By default 10% of the training data is supplied with silence clips mix with random background

* https://www.kaggle.com/davids1992/speech-representation-and-data-exploration/notebook
    - Great source for visualizing the audio recordings and converting the raw to usable cleaner audio data
    - Features normalization from mean and std
    - Spectrogram and MFCC from librosa
    - VAD
    - Resample audio to 8k Hz