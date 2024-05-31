import joblib

model = joblib.load('models/model_rf_coba.sav')

class Dokter:
    def __init__(self, nama_dokter, gender_dokter, spesialis):
        self.nama_dokter = nama_dokter
        self.gender_dokter = gender_dokter
        self.spesialis = spesialis