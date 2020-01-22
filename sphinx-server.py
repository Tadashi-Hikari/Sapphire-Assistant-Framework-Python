import os, pyaudio, wave, time, io, argparse
from time import localtime, strftime
from pocketsphinx import get_model_path,  get_data_path, Pocketsphinx, AudioFile    

# Check for running mode, based on command line arguments
parser = argparse.ArgumentParser(description="Transcribe audio into text")

# This will be how the assistant launches pocketsphinx
parser.add_argument('--d', dest='daemon', help="Run pocketsphinx as a daemon", default=False, action='store_true')

# This will be how the assistant handles offloaded audio data
parser.add_argument('--b', metavar='Dir', dest='batch', help="Process and transcribe all .wav files in directory \'Dir\'")

# This will likely be how the assitant handles 1 off audio files
parser.add_argument('--f', metavar='File', dest='file', help="Process individual files", nargs='+')

args = parser.parse_args()

# Theres an issue where all of my audio files are 8K sample, instead of 16K
def processAudio(file):
    audio = AudioFile(audio_file=file, buffer_size=1024)
    for phrase in audio:
        print(phrase)

def checkFile(file):
    if file.endswith('.wav') and os.path.exists(file):
        return file
    else:
        print("Not a valid .wav file")
        return None
        
def checkDir(path):
    wav = []
    dirList = os.listdir(path)
    if not dirList:
        print("Invalid path")
        exit()
    for file in dirList:
        file = checkFile(path+file)
        if file != None:
            wav.append(file)

    # If there are no wav files
    if not wav:
        print("Nothing in the directory was a valid .wav file")
        return None
    else:
        return wav

if args.batch is not None:
    validFiles = checkDir(args.batch)
    if validFiles == None:
        print("Error: No valid files")
        exit()
    else:
        for file in validFiles:
            processAudio(file)
elif args.file is not None:
    for file in args.file:
        validFile = checkFile(file)
        if validFile == None:
            print("Error: No valid files")
            exit()
        else:
            processAudio(file)
elif args.daemon is True:
    frames = []

    model_path = get_model_path()
    data_path = get_data_path()
    # This is the configuration for the pocketsphinx object
    config = {
        'hmm': os.path.join(model_path, 'en-us'),
        'lm': os.path.join(model_path, 'en-us.lm.bin'),
        'dict': os.path.join(model_path, 'cmudict-en-us.dict')
    }

    ps = Pocketsphinx(**config)
    
    #PyAudio stuff
    chunk = 1024
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 16000 # Record 16000 samples per second
    ouput = "dump-folder/audio/" # This is where the audio files are kept
    
    p = pyaudio.PyAudio() # Create an interface to PortAudio
    
    # See PyAudio Documentation        
    stream = p.open(format = sample_format,
                    channels = channels,
                    rate = fs,   
                    frames_per_buffer = chunk,
                    input = True)
    
    print("Running as a daemon")
    print("Recording")

    #this is the only one that needs PyAudio it seems
    while True:
        ps.start_utt()
        # When there is silence, assume they stopped speaking
        while stream.get_read_available() > 0:
            data = stream.read(chunk)
            ps.process_raw(data, False, False)
            frames.append(data)            
        ps.end_utt() # This is not part of the While loop

        # This prevents it from printing silence
        if (ps.hypothesis() != ''):
            print(ps.hypothesis())
            frames = []

    stream.stop_stream()
    stream.close()
    p.terminate()

