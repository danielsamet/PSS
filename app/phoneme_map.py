def generate_phoneme_map():
    phoneme_map = dict()

    with open("static/britfone.main.3.0.1.csv", mode="r", encoding="utf-8") as csv_file:
        for line in csv_file:
            line = line[:-1].split(", ")
            word = line[0].lower().replace("(1)", "").replace("(2)", "").replace("(3)", "").replace("(4)", "")
            phoneme_map[word] = line[1].split(" ")

    return phoneme_map
