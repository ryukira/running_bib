Sistem Autentikasi Chip Bib Lari dengan Warning Alert
Arsitektur Sistem
Sistem ini mengintegrasikan teknologi RFID UHF dengan verifikasi biometrik untuk memastikan bahwa chip bib lari benar-benar digunakan oleh pelari yang terdaftar. Arsitektur terdiri dari beberapa komponen utama:​

Komponen Hardware:
- RFID UHF Chip yang terintegrasi dengan bib (BibTag) dengan frekuensi 860-960 MHz​
- RFID Reader & Antenna di checkpoint start, tengah, dan finish line yang dapat membaca hingga 1000+ tag per detik dengan jarak 10-15 meter​
- Kamera Biometrik di titik registrasi dan checkpoint penting untuk face recognition​
- Fingerprint Scanner untuk autentikasi tambahan saat pengambilan bib​
- Server Backend dengan database peserta dan sistem alert

Komponen Software:
- Registration System - mendaftarkan data pelari dan biometrik
- Authentication Engine - memverifikasi identitas pelari
- Alert System - mendeteksi anomali dan mengirim warning
- Race Timing Software - mencatat waktu dan hasil lomba
- Dashboard Monitoring - untuk panitia memantau real-time

Alur Kerja Sistem
1. Fase Registrasi (Pre-Race)
Saat pelari mendaftar dan mengambil race pack:
Pelari menunjukkan ID resmi dengan foto​
Sistem mengambil foto wajah pelari menggunakan face recognition camera​
Sistem merekam sidik jari pelari menggunakan fingerprint scanner​
Data biometrik (face template dan fingerprint) disimpan di database dan di-link dengan:
Nomor bib unik
ID chip RFID (EPC number)​
Data diri pelari (nama, nomor telepon, emergency contact)
Timestamp registrasi

2. Fase Verifikasi Awal (Race Day Check-in)
Sebelum memasuki area start:
Pelari scan chip RFID mereka di gate entrance
Sistem memicu kamera face recognition untuk mengambil foto real-time​
Sistem melakukan face matching 1:1 antara foto saat registrasi dengan foto real-time​
Jika match confidence > 95%, akses diizinkan dan timestamp tercatat​
Jika match confidence < 95%, sistem trigger WARNING ALERT Level 1:
Notifikasi ke dashboard panitia
Pelari diarahkan ke manual verification desk
Staff melakukan verifikasi ID dan fingerprint secondary authentication​

3. Fase Race Monitoring (During Race)
Checkpoint Detection System:
RFID readers di setiap checkpoint (Start, CP1, CP2, ..., Finish) membaca chip secara otomatis​
Setiap deteksi chip mencatat:
EPC ID (chip ID)
Timestamp yang sangat presisi
Lokasi checkpoint
Reader ID
Anti-Fraud Detection Algorithm:
Sistem menjalankan beberapa validasi otomatis untuk mendeteksi kecurangan:

a) Duplicate Detection Alert
Jika satu chip ID terdeteksi di dua lokasi berbeda dalam waktu yang tidak masuk akal (misal: finish dalam 10 menit untuk half marathon)​
WARNING: "Chip ID #12345 detected at impossible time intervals"

b) Ghost Runner Detection
Jika chip terdeteksi di checkpoint tanpa ada verifikasi biometrik di start line
WARNING: "Chip ID #12345 no face verification at start"

c) Bib Swap Detection
Kamera AI di checkpoint strategis (misal: finish line) mengambil foto pelari
Face recognition mencocokkan dengan database registrasi​
Jika wajah tidak match dengan pemilik bib yang terdaftar:
ALERT LEVEL 2: "Face mismatch detected - Bib #789 may be swapped"​

d) Missing Checkpoint Alert
Jika pelari terdeteksi di finish tetapi melewati checkpoint wajib
WARNING: "Chip ID #12345 missed mandatory checkpoint CP2"

e) Counterfeit Bib Detection
Chip yang tidak terdaftar di database akan trigger alert​
CRITICAL ALERT: "Unknown RFID chip detected - potential counterfeit"

4. Real-Time Alert System
Ketika sistem mendeteksi anomali, alert otomatis dikirim ke:
Dashboard Panitia:
Live monitoring screen menampilkan semua alert dengan color coding (yellow = warning, red = critical)
Detail pelari yang dicurigai (nama, bib number, foto, lokasi terakhir)
Timeline aktivitas chip tersebut

Mobile App Tim Keamanan:
Push notification langsung ke smartphone security team di lapangan
GPS location pelari yang dicurigai
Instruksi tindakan (approach and verify, standby at finish line, etc.)

Automated Response:
Email/SMS ke kontak darurat pelari jika terdeteksi anomali serius
Flag pada hasil sementara dengan status "Under Review"