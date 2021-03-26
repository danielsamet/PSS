import os

from flask import url_for

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

    relative_dir = db.Column(db.String(2048))
    name = db.Column(db.String(32))

    phoneme = db.relationship("Phoneme", back_populates="recording", uselist=False)

    def __init__(self, relative_dir, name):
        self.relative_dir = relative_dir
        self.name = name

    def __repr__(self):
        return f"<PhonemeRecording {self.phoneme}:{self.id}>"

    @property
    def local_address(self):
        # TODO: update this
        return os.path.join(self.relative_dir, self.name)

    @property
    def web_address(self):
        return url_for("static", filename=os.path.join(self.relative_dir, self.name).replace("\\", "/"))
