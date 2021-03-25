from app import db


class PhonemeRecording(db.Model):
    __tablename__ = "phoneme_recordings"

    id = db.Column(db.Integer, primary_key=True)

    symbol = db.Column(db.String(3), nullable=False)
    number = db.Column(db.Integer)
    recording_address = db.Column(db.String(2048))

    def __init__(self, symbol, number, recording_address):
        self.symbol = symbol
        self.number = number
        self.recording_address = recording_address

    def __repr__(self):
        return f"<PhonemeRecording {self.number}:{self.symbol}>"
