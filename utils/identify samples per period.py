import wave
import os

def read_wav(filename):
    with wave.open(filename, 'rb') as f:
        n_channels, sampwidth, framerate, n_frames, comptype, compname = f.getparams()
        frames = f.readframes(n_frames)
        # Convert byte data to int16
        int_values = [int.from_bytes(frames[i:i+2], byteorder='little', signed=True) for i in range(0, len(frames), 2)]
        return int_values

def zero_crossings(data):
    crossings = []
    for i in range(1, len(data)):
        if data[i-1] * data[i] < 0:
            crossings.append(i)
    return crossings

def most_common(lst):
    freq_map = {}
    for i in lst:
        if i in freq_map:
            freq_map[i] += 1
        else:
            freq_map[i] = 1
    max_count = max(freq_map.values())
    for period, count in freq_map.items():
        if count == max_count:
            return period, count

def analyze_wav(filename):
    data = read_wav(filename)

    # Find zero crossings
    crossings = zero_crossings(data)
    total_samples = len(data)
    total_periods = (len(crossings) + 1) // 2
    periods = [crossings[i+1] - crossings[i] for i in range(len(crossings) - 1)]
    period, count = most_common(periods)

    status = "INCONSISTANT" if len(set(periods)) > 1 else ""
    frequency = 44100 / (2 * period)  # Factor of 2 for square wave
    return f"{filename}: {frequency:.2f} Hz (samples per period: {period}, count: {count}), first four: {periods[:4]}  {status}"

def main():
    directory = input("Enter the path to the folder containing .wav files: ")
    wav_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.wav')]

    for filename in wav_files:
        result = analyze_wav(filename)
        print(result)
        print()

if __name__ == "__main__":
    main()
