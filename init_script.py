from app import create_app, db
from app.models import Phoneme, PhonemeExample
from app.phoneme_example_dict import phoneme_words

application = create_app(skip_dir_building=True)
with application.app_context():
    for index, symbol in enumerate(phoneme_words):
        phoneme = Phoneme(symbol, index + 1)
        db.session.add(phoneme)

        for word in phoneme_words[symbol]:
            phoneme.examples.append(PhonemeExample(word, ",".join(application.words[word.upper()])))

    db.session.commit()
