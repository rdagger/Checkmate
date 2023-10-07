"""Game sound generation."""
from pygame import mixer, time
from os import path

DURATIONS = {
    "human4": .067,
    "human3": .084,
    "human2": .096,
    "computer": .033
}

DIRECTIONS = {
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0),
    'up': (0, -1)
}

SAMPLE_RATE = 44100  # 44.1 kHz
SOUND_EFFECTS = ['1', '2', '3', 'explode']


class GameSounds():
    """Class to generate, load and play sounds."""
    def __init__(self):
        """Game sounds constructor.

        Args:
            human_speed(int): FPS for human player
        """
        mixer.pre_init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=256)
        mixer.init()
        mixer.set_num_channels(24)
        self.sound_effects = {}
        self.load_sound_effects()
        self.tones = {}
        self.load_tones()
        self.current_sound = ""
        self.current_sound_length = 0
        self.tone_channel = len(SOUND_EFFECTS)

    def _bytes_to_integers(self, wave):
        """Convert raw bytes to integers.

        Args:
            wave(byte sequence): The raw wave data to convert
        Returns:
            [int]: Converted data
        """
        return [int.from_bytes(wave[i:i+2],
                               byteorder='little', signed=True)
                for i in range(0, len(wave), 2)]

    def clear_tone_channel(self):
        """Stops any player movement tones playing on the tone channel."""
        channel = mixer.Channel(self.tone_channel)
        channel.stop()
        self.current_sound = ""

    def get_wave_period_length(self, wave):
        """Get the period length of wave data.

        Args:
            wave(byte sequence): The raw wave to analyze
        Returns:
            (int): Period length of wave form
        """
        wave_data = self._bytes_to_integers(wave)
        crossings = []
        for i in range(1, len(wave_data)):
            if wave_data[i-1] * wave_data[i] < 0:
                crossings.append(i)
        # Calculate periods between zero crossings
        periods = [crossings[i+1] - crossings[i]
                   for i in range(len(crossings) - 1)]
        # Find most common period
        freq_map = {}
        for i in periods:
            if i in freq_map:
                freq_map[i] += 1
            else:
                freq_map[i] = 1
        max_count = max(freq_map.values())
        period_length = next(period for period, count in freq_map.items()
                             if count == max_count)
        if len(set(periods)) > 1:
            raise ValueError("Invalid square wave period length")
        return 2 * period_length

    def load_sound_effects(self):
        """Load all game sound effects"""
        for effect in SOUND_EFFECTS:
            self.sound_effects[effect] = mixer.Sound(path.join("sounds",
                                                     effect + ".mp3"))

    def load_tones(self):
        """Load and trim tones used for player movement."""
        for player_type, duration in DURATIONS.items():
            for player in [1, 2, 3, 4]:
                for direction, coords in DIRECTIONS.items():
                    sound = mixer.Sound(path.join("sounds",
                                        f"P{player}_{direction}.wav"))
                    raw = mixer.Sound.get_raw(sound)
                    bytes_per_sample = round(len(raw) / (
                        sound.get_length() * SAMPLE_RATE))
                    trimmed_sound = self.trim_wave(raw, duration,
                                                   bytes_per_sample)
                    self.tones[f"{player}_{coords}_{player_type}"] = (
                        trimmed_sound)

    def play(self, effects, delay=None, maxtime=0):
        """Play sound effect(s).

        Args:
            effects(string or [string]): Effect(s) to play.
            delay(None or int): Sets a delay in milliseconds if specified.
            maxtime(integer): The maximum time to play the sound (0=None)
        """
        self.clear_tone_channel()  # Stop any playing player movement tones
        if isinstance(effects, str):  # Handle single effect
            effects = [effects]
        # Play effect(s)
        for effect in effects:
            channel_number = SOUND_EFFECTS.index(effect)  # Use unique channels
            channel = mixer.Channel(channel_number)
            if channel is None:  # Do not play if no channels available
                return
            channel.play(self.sound_effects[effect], maxtime=maxtime)
            if delay is not None:
                time.wait(delay)
                channel.stop()

    def play_mult(self, effects, volume=.5):
        """Play sound effects for player movements.

        Args:
            effects(string or [string]): Effect(s) to play.
            volume(float): Volume level from 0.0 (silent) to 1.0 (max)
        Returns:
            (float): Length of combined sound in milliseconds
        """
        # Skip if speciifed sound effects are already playing
        if self.current_sound == effects:
            return self.current_sound_length

        tones = [self.tones[key] for key in effects]
        sound = mixer.Sound(buffer=b''.join(tones))
        sound.set_volume(volume)
        channel = mixer.Channel(self.tone_channel)
        if channel is None:  # Do not play if no channels available
            return
        channel.play(sound, -1)  # Play sound effects and loop
        self.current_sound = effects  # Store current sound effect
        self.current_sound_length = sound.get_length() * 1000
        return self.current_sound_length

    def trim_wave(self, wave, duration, bytes_per_sample):
        """Trim the duration of raw wave data.

        Args:
            wave(byte sequence): The raw wave data to trim
            duration(float): Desired duration in seconds
            bytes_per_sample(int): Number of bytes per sample
        """
        bytes_for_duration = int(SAMPLE_RATE * bytes_per_sample * duration)
        bytes_per_period = self.get_wave_period_length(wave)
        # Calculate how many periods can fit within the desired duration
        number_of_periods = bytes_for_duration // bytes_per_period
        # Calculate bytes corresponding to these periods
        bytes_to_truncate = number_of_periods * bytes_per_period
        return wave[:bytes_to_truncate]
