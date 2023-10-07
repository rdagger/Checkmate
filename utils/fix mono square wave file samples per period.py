import wave
import numpy as np
from collections import Counter
import struct

notes = [
    ("G0", 24.50), ("G#0/Ab0", 25.96), ("A0", 27.50), ("A#0/Bb0", 29.14), ("B0", 30.87),
    ("C1", 32.70), ("C#1/Db1", 34.65), ("D1", 36.71), ("D#1/Eb1", 38.89), ("E1", 41.20),
    ("F1", 43.65), ("F#1/Gb1", 46.25), ("G1", 49.00), ("G#1/Ab1", 51.91), ("A1", 55.00),
    ("A#1/Bb1", 58.27), ("B1", 61.74),
    ("C2", 65.41), ("C#2/Db2", 69.30), ("D2", 73.42), ("D#2/Eb2", 77.78), ("E2", 82.41),
    ("F2", 87.31), ("F#2/Gb2", 92.50), ("G2", 98.00), ("G#2/Ab2", 103.83), ("A2", 110.00),
    ("A#2/Bb2", 116.54), ("B2", 123.47),
    ("C3", 130.81), ("C#3/Db3", 138.59), ("D3", 146.83), ("D#3/Eb3", 155.56), ("E3", 164.81),
    ("F3", 174.61), ("F#3/Gb3", 185.00), ("G3", 196.00), ("G#3/Ab3", 207.65), ("A3", 220.00),
    ("A#3/Bb3", 233.08), ("B3", 246.94),
    ("C4", 261.63), ("C#4/Db4", 277.18), ("D4", 293.66), ("D#4/Eb4", 311.13), ("E4", 329.63),
    ("F4", 349.23), ("F#4/Gb4", 369.99), ("G4", 392.00), ("G#4/Ab4", 415.30), ("A4", 440.00),
    ("A#4/Bb4", 466.16), ("B4", 493.88),
    ("C5", 523.25), ("C#5/Db5", 554.37), ("D5", 587.33), ("D#5/Eb5", 622.25), ("E5", 659.26),
    ("F5", 698.46), ("F#5/Gb5", 739.99), ("G5", 783.99), ("G#5/Ab5", 830.61), ("A5", 880.00),
    ("A#5/Bb5", 932.33), ("B5", 987.77),
    ("C6", 1046.50), ("C#6/Db6", 1108.73), ("D6", 1174.66), ("D#6/Eb6", 1244.51), ("E6", 1318.51),
    ("F6", 1396.91), ("F#6/Gb6", 1479.98), ("G6", 1567.98), ("G#6/Ab6", 1661.22), ("A6", 1760.00),
    ("A#6/Bb6", 1864.66), ("B6", 1975.53),
    ("C7", 2093.00), ("C#7/Db7", 2217.46), ("D7", 2349.32), ("D#7/Eb7", 2489.02), ("E7", 2637.02),
    ("F7", 2793.83), ("F#7/Gb7", 2959.96), ("G7", 3135.96), ("G#7/Ab7", 3322.44), ("A7", 3520.00),
    ("A#7/Bb7", 3729.31), ("B7", 3951.07),
    ("C8", 4186.01), ("C#8/Db8", 4434.92), ("D8", 4698.64), ("D#8/Eb8", 4978.03), ("E8", 5274.04),
    ("F8", 5587.65), ("F#8/Gb8", 5919.91), ("G8", 6271.93), ("G#8/Ab8", 6644.88), ("A8", 7040.00),
    ("A#8/Bb8", 7458.62), ("B8", 7902.13)
]


class WavePeriod:
    def __init__(self):
        self.position = 0
        self.first_half_count = 0
        self.second_half_count = 0
        self.first_half_discrepancy = 0
        self.second_half_discrepancy = 0
        self.first_half_samples = []
        self.second_half_samples = []

    def __str__(self):
        return (f"Position: {self.position}, "
                f"First Half Period Sample Count: {self.first_half_count}, "
                f"Second Half Period Sample Count: {self.second_half_count}, "
                f"First Half Discrepancy: {self.first_half_discrepancy}, "
                f"Second Half Discrepancy: {self.second_half_discrepancy}")


def read_wav(filename):
    with wave.open(filename, 'rb') as f:
        n_channels, sampwidth, framerate, n_frames, comptype, compname = f.getparams()
        frames = f.readframes(n_frames)
        return np.frombuffer(frames, dtype=np.int16)

def zero_crossings(data):
    return np.where(np.diff(np.sign(data)))[0]

def get_closest_note(frequency, notes):
    # Finding the note with the minimum difference in frequency
    closest_note, note_freq = min(notes, key=lambda note: abs(note[1] - frequency))
    difference = abs(note_freq - frequency)
    return closest_note, note_freq, difference

def main():
    filename = input("Enter the path to the mono square wave wav file: ")
    data = read_wav(filename)

    # Find zero crossings
    crossings = zero_crossings(data)
    total_samples = len(data)
    total_periods = (len(crossings) + 1) // 2

    # Calculate periods
    periods = np.diff(crossings)

    # Most prevalent period
    period_counts = Counter(periods)
    common_periods = period_counts.most_common()

    # If there's inconsistency in periods
    if len(common_periods) > 1:
        print("Inconsistent samples per period detected!")
        print("Most prevalent samples per period:", common_periods[0][0])

        """
        # Offering choices
        for i, (period, count) in enumerate(common_periods, 1):
            frequency = 44100 / (2 * period)  # Factor of 2 for square wave
            print(f"{i}. {frequency} Hz (samples per period: {period}, count: {count})")
        """
        # Offering choices
        for i, (period, count) in enumerate(common_periods, 1):
            frequency = 44100 / (2 * period)  # Factor of 2 for square wave
            closest_note, note_freq, difference = get_closest_note(frequency, notes)
            print(f"{i}. {frequency:.2f} Hz (samples per period: {period}, count: {count}, "
                  f"closest note: {closest_note} at {note_freq:.2f} Hz, difference: {difference:.2f} Hz)")


        
        choice = int(input("Pick a frequency: "))
        target_period = common_periods[choice-1][0]

        wave_periods = []
        pointer = 0
        index = 0
        for i in range(0, len(crossings), 2):
            index += 1
            midway= crossings[i]
            ending = crossings[i + 1] - 1 if i + 1 < len(crossings) else total_samples - 1
            wp = WavePeriod()
            wp.position = index
            wp.first_half_samples = data[pointer:midway + 1]
            wp.second_half_samples = data[midway + 1:ending + 2]
            wp.first_half_count = len(wp.first_half_samples)
            wp.second_half_count = len(wp.second_half_samples)
            wp.first_half_discrepancy = wp.first_half_count - target_period
            wp.second_half_discrepancy = wp.second_half_count - target_period
            pointer = ending + 2
            wave_periods.append(wp)

        
        # Fix samples per period
        for wp in wave_periods:
            while wp.first_half_discrepancy !=0 or wp.second_half_discrepancy != 0:
                # Check for offseting values
                if wp.first_half_discrepancy < 0 and wp.second_half_discrepancy > 0:
                    # Move the first element of wp.second_half_samples to the end of wp.first_half_samples
                    wp.first_half_samples = np.append(wp.first_half_samples, -wp.second_half_samples[0])
                    wp.second_half_samples = np.delete(wp.second_half_samples, 0)
                elif wp.first_half_discrepancy > 0 and wp.second_half_discrepancy < 0:
                    # Insert the last element of wp.first_half_samples at the beginning of wp.second_half_samples
                    wp.second_half_samples = np.insert(wp.second_half_samples, 0, -wp.first_half_samples[-1])
                    # Remove the last element from wp.first_half_samples
                    wp.first_half_samples = np.delete(wp.first_half_samples, -1)
                elif wp.first_half_discrepancy < 0:
                    # Calculate the integer value halfway between 0 and the last element of wp.first_half_samples
                    mid_value = wp.first_half_samples[-1] // 2
                    # Append the calculated value to wp.first_half_samples
                    wp.first_half_samples = np.append(wp.first_half_samples, mid_value)
                elif wp.second_half_discrepancy < 0:
                    # Calculate the integer value halfway between 0 and the last element of wp.second_half_samples
                    mid_value = wp.second_half_samples[-1] // 2
                    # Append the calculated value to wp.first_half_samples
                    wp.second_half_samples = np.append(wp.second_half_samples, mid_value)
                elif wp.first_half_discrepancy > 0:
                    wp.first_half_samples = np.delete(wp.first_half_samples, 0)
                elif wp.second_half_discrepancy > 0:
                    wp.second_half_samples = np.delete(wp.second_half_samples, 0)

                # Update
                wp.first_half_count = len(wp.first_half_samples)
                wp.second_half_count = len(wp.second_half_samples)
                wp.first_half_discrepancy = wp.first_half_count - target_period
                wp.second_half_discrepancy = wp.second_half_count - target_period

                print(wp)
                print(f"first: {wp.first_half_samples[0]} to {wp.first_half_samples[-1]}")
                print(f"second: {wp.second_half_samples[0]} to {wp.second_half_samples[-1]}")

        # Create the fixed wave data
        fixed_data = np.concatenate([np.concatenate([wp.first_half_samples, wp.second_half_samples]) for wp in wave_periods])

        # Save the fixed wave
        fixed_bytes = struct.pack('<' + 'h'*len(fixed_data), *fixed_data)
        with wave.open(filename[:-4] + '_fixed.wav', 'wb') as out_f:
            out_f.setnchannels(1)
            out_f.setsampwidth(2)
            out_f.setframerate(44100)
            out_f.writeframes(fixed_bytes)
        print(f"Fixed wave saved as {filename[:-4]}_fixed.wav")

    else:
        print("No inconsistencies found!")

if __name__ == "__main__":
    while True:
        main()
