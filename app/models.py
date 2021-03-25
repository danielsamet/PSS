from app import db


class Phoneme(db.Model):
    __tablename__ = "phonemes"

    id = db.Column(db.Integer, primary_key=True)

    symbol = db.Column(db.String(3), nullable=False)
    number = db.Column(db.Integer)

    recording_id = db.Column(db.Integer, db.ForeignKey("phoneme_recordings.id"))
    recording = db.relationship("PhonemeRecording", back_populates="phoneme")

    examples = db.relationship("PhonemeExample", back_populates="phoneme")

    def __init__(self, symbol, number):
        self.symbol = symbol
        self.number = number

    def __repr__(self):
        return f"<PhonemeRecording {self.number}:{self.symbol}>"


class PhonemeExample(db.Model):
    __tablename__ = "phoneme_examples"

    id = db.Column(db.Integer, primary_key=True)

    word = db.Column(db.String(32))
    phoneme_breakdown = db.Column(db.String(256))  # comma separated phonemes

    phoneme_id = db.Column(db.Integer, db.ForeignKey("phonemes.id"))
    phoneme = db.relationship("Phoneme", back_populates="examples")

    def __init__(self, word, breakdown):
        self.word = word
        self.phoneme_breakdown = breakdown

    def __repr__(self):
        return f"<PhonemeExample {self.phoneme}:{self.id} - {self.word}>"


class PhonemeRecording(db.Model):
    __tablename__ = "phoneme_recordings"

    id = db.Column(db.Integer, primary_key=True)

    recording_address = db.Column(db.String(2048))

    phoneme = db.relationship("Phoneme", back_populates="recording")

    def __init__(self, recording_address):
        self.recording_address = recording_address

    def __repr__(self):
        return f"<PhonemeRecording {self.phoneme}:{self.id}>"
