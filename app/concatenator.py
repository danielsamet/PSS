"""
Concatenation is processed in three steps, each step feeds into the next:

1) parse_text: text is parsed to generate a list of words

2) parse_words: words are parsed and converted into a list of phoneme tokens

3) generate_audio: audio is generated based on the list of phonemes
"""
import os
import random
import string
import subprocess

from flask import current_app

from app import create_app
from app.models import Phoneme


def parse_text(text):
    """
    raw text is passed in here and parsed into a list of words

    Notes:
    - spaces are represented by an empty list item
    """

    words = []

    for word in text.split(" "):
        words.append(word.lower())
        words.append(" ")

    return words[:-1]


def parse_words(words):
    """
    word list is parsed and converted into a list of phonemes

    Notes:
    - spaces are represented by an empty list item
    """

    phonemes = []

    for word in words:
        if word == " ":
            phonemes.append(" ")  # add space until the last word
        else:
            for phoneme in current_app.phoneme_map[word]:
                phonemes.append(phoneme)

    return phonemes


def generate_audio(phonemes):
    """
    returns file address for generated audio
    """

    phoneme_recordings = {}
    for phoneme_needed in set(phonemes) - {" "}:
        print(phoneme_needed)
        local_address = Phoneme.query.filter_by(symbol=phoneme_needed).first().recording.local_address
        phoneme_recordings[phoneme_needed] = os.path.join(current_app.config.get("STATIC_DIR"), local_address).replace(
            "\\", "/")

    inputs_str = " ".join([f"-i \"{phoneme_recordings[phoneme]}\"" for phoneme in phonemes if phoneme != " "])

    if len(phonemes) > 1:
        filter_str, filter_counter = "", 0
        for index in range(len(phonemes) - 1):
            if phonemes[index] == " ":
                continue

            filter_str += f"[{filter_counter if index == 0 else f'a{filter_counter:02}'}][{filter_counter + 1}]"

            apad = 4000 if phonemes[index + 1] == " " else 1000
            filter_str += f"acrossfade=ns=2300:c1=tri:c2=tri, apad=pad_len={apad}, atempo=0.95"

            if index < len(phonemes) - 2:
                filter_str += f"[a{filter_counter + 1:02}];"

            filter_counter += 1

        print(filter_str)

        filter_str = "-filter_complex \"" + filter_str + "\""
    else:
        filter_str = ""

    output_rel_dir = os.path.join("recording", "output")
    output_dir = os.path.join(current_app.config.get("STATIC_DIR"), output_rel_dir)
    output_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) \
                      + f".{current_app.config.get('AUDIO_FILE_EXT')}"
    output_full = os.path.join(output_dir, output_filename).replace("\\", "/")

    execute_str = f"ffmpeg {inputs_str} {filter_str} \"{output_full}\""

    print("\n")
    print(execute_str)

    subprocess.call(execute_str)

    return {
        "relative_address": os.path.join(output_rel_dir, output_filename),
        "absolute_address": output_full
    }


def tts(input_text):
    words = parse_text(input_text)
    phonemes = parse_words(words)
    return generate_audio(phonemes)


if __name__ == '__main__':
    # Tests

    with create_app(skip_dir_building=True).app_context():
        # tts("you")
        tts("how are you doing today")
