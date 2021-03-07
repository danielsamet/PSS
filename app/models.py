from app import db


class PhonemeRecording(db.Model):
    __tablename__ = "phoneme_recordings"

    id = db.Column(db.Integer, primary_key=True)

    phoneme = db.Column(db.String(3), nullable=False)
    recording_address = db.Column(db.String(2048))

    def __init__(self, phoneme, recording_address):
        self.phoneme = phoneme
        self.recording_address = recording_address

    def __repr__(self):
        return f"<PhonemeRecording {self.phoneme}>"
