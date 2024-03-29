import os

from app.config import Config


def get_words():
    words = {}

    with open(os.path.join(Config.STATIC_DIR, "britfone.main.3.0.1.csv"),
              mode="r", encoding="utf-8") as csv_file:
        for line in csv_file:
            line = line[:-1].split(", ")
            words[line[0]] = line[1].split(" ")

    return words
