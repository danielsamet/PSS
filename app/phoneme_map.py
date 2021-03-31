import os


def generate_phoneme_map(static_dir):
    phoneme_map = dict()

    britfone_address = os.path.join(static_dir, "britfone.main.3.0.1.csv")
    with open(britfone_address, mode="r", encoding="utf-8") as csv_file:
        for line in csv_file:
            line = line[:-1].split(", ")
            word = line[0].lower().replace("(1)", "").replace("(2)", "").replace("(3)", "").replace("(4)", "")
            phoneme_map[word] = line[1].split(" ")

    return phoneme_map
