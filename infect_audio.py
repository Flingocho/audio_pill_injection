from pydub import AudioSegment
from os import path, makedirs, listdir
import argparse
import os


def process_audio(base_audio_path, pill_audio_path, output_dir, num_copies):

    if not path.exists(output_dir):
        try:
            makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        except Exception as e:
            print(f"Error creating output directory {output_dir}: {e}")
            return

    try:
        # load audio files
        audio1 = AudioSegment.from_file(base_audio_path)
        pill = AudioSegment.from_file(pill_audio_path)
    except FileNotFoundError as e:
        print(f"Error: One of the audio files was not found. Please check paths.")
        print(e)
        return
    except Exception as e:
        print(f"Error loading audio files: {e}")
        return

    # define the initial temporal position of pill
    time_ms = 5000 # time in milliseconds
    copy_counter = 0

    # make n_copies with different temporal positions
    print(f"Generating {num_copies} copies with infect_audio by Flingocho...")
    base_filename = os.path.splitext(os.path.basename(base_audio_path))[0] # Get base filename without extension
    for i in range(1, num_copies+1):
        result = audio1.overlay(pill, position=time_ms)
        # Use the original filename for the output
        output_file_path = path.join(output_dir, f"{base_filename}_infected_{i}.mp3")
        try:
            result.export(output_file_path, format="mp3")
        except Exception as e:
            print(f"Error exporting file {output_file_path}: {e}")
            # Decide if you want to break or continue
            break 
        time_ms += 1000 # add 1 second in milliseconds
        copy_counter +=1

    if copy_counter > 0:
        print(f"The {copy_counter} copies have been created in {output_dir}!")
    else:
        print("No copies were created.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Overlay pill_standard.wav onto an audio file from input_audio/ folder.")
    parser.add_argument("-n", "--num_copies", type=int, default=1, help="Number of copies to generate (default: 1).")

    args = parser.parse_args()

    # Determine the script's directory to build relative paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_audio_dir = os.path.join(script_dir, "input_audio")
    pill_audio_path = os.path.join(script_dir, "pill_standard.wav")
    output_folder_path = os.path.join(script_dir, "output_audio")

    # Find the audio file in input_audio_dir
    try:
        input_files = [f for f in listdir(input_audio_dir) if os.path.isfile(os.path.join(input_audio_dir, f))]
        if not input_files:
            print(f"Error: No files found in {input_audio_dir}")
            exit()
        if len(input_files) > 1:
            print(f"Warning: Multiple files found in {input_audio_dir}. Using the first one: {input_files[0]}")
        base_audio_filename = input_files[0]
        base_audio_full_path = os.path.join(input_audio_dir, base_audio_filename)
    except FileNotFoundError:
        print(f"Error: Input directory not found at {input_audio_dir}")
        exit()
    except Exception as e:
        print(f"Error accessing input directory {input_audio_dir}: {e}")
        exit()

    if not os.path.exists(pill_audio_path):
        print(f"Error: Pill audio not found at {pill_audio_path}")
        exit()

    process_audio(base_audio_full_path, pill_audio_path, output_folder_path, args.num_copies)