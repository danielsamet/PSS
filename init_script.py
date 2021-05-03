from app import create_app, db, get_words
from app.main.models import Phoneme, PhonemeExample
from app.main.phonemes.phoneme_example_dict import phoneme_words

application = create_app()
with application.app_context():
    application.words = get_words()
    for index, symbol in enumerate(phoneme_words):
        phoneme = Phoneme(symbol, index + 1)
        db.session.add(phoneme)

        for word in phoneme_words[symbol]:
            phoneme.examples.append(PhonemeExample(word, ",".join(application.words[word.upper()])))

        print(symbol, "done")

    print("Complete")
    db.session.commit()
