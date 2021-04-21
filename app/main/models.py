import os

from flask import url_for

from app import db


class Phoneme(db.Model):
    __tablename__ = "phonemes"

    id = db.Column(db.Integer, primary_key=True)

    symbol = db.Column(db.String(3), nullable=False)
    number = db.Column(db.Integer)

    recordings = db.relationship("PhonemeRecording", back_populates="phoneme")

    examples = db.relationship("PhonemeExample", back_populates="phoneme")

    def __init__(self, symbol, number):
        self.symbol = symbol
        self.number = number

    def __repr__(self):
        return f"<Phoneme {self.number}:{self.symbol}>"


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

    relative_dir = db.Column(db.String(2048))
    name = db.Column(db.String(32))  # filename

    phoneme_id = db.Column(db.Integer, db.ForeignKey("phonemes.id"))
    phoneme = db.relationship("Phoneme", back_populates="recordings")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="phoneme_recording_objects")

    def __init__(self, relative_dir, name, phoneme_id=None):
        self.relative_dir = relative_dir
        self.name = name

        self.phoneme_id = phoneme_id

    def __repr__(self):
        return f"<PhonemeRecording {self.user}:{self.phoneme}>"

    @property
    def local_address(self):
        # TODO: update this
        return os.path.join(self.relative_dir, self.name)

    @property
    def web_address(self):
        return url_for("main.user_data", filename=os.path.join(self.relative_dir, self.name).replace("\\", "/"))
