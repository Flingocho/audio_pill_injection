from pydub import AudioSegment
from pydub.generators import Square # Changed from Sine to Square
import os

def generate_pill():
    """
    Generates a 25kHz square wave tone for 100ms and saves it as pill_standard.wav.
    """
    frequency_hz = 25000
    duration_ms = 100
    # Output filename is now fixed to pill_standard.wav
    output_filename = "pill_standard.wav" 

    # Create a square wave generator, setting sample_rate here
    square_wave = Square(frequency_hz, sample_rate=44100)

    # Generate the audio segment for the specified duration
    # sample_rate is now part of the generator itself
    audio_segment = square_wave.to_audio_segment(duration=duration_ms)
    
    # Determine the script's directory to save the pill in the correct location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_output_path = os.path.join(script_dir, output_filename)

    # Export the audio to a file
    try:
        audio_segment.export(full_output_path, format="wav")
        print(f"Successfully generated square wave pill: {full_output_path}")
        return full_output_path
    except Exception as e:
        print(f"Error exporting audio: {e}")
        return None

# Directly call the function to generate the tone when the script is run
if __name__ == "__main__":
    print(f"Generating a 25kHz square wave pill (100ms) as pill_standard.wav...")
    generate_pill()
