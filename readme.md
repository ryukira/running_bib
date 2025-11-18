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

Keamanan dan Privacy
Data Protection:
Data biometrik (face template dan fingerprint) disimpan terenkripsi menggunakan AES-256​
Face template berbentuk mathematical representation, bukan foto asli, sehingga tidak bisa di-reverse​
Data hanya disimpan selama event (+ 30 hari untuk dispute handling), kemudian dihapus sesuai GDPR/privacy regulation

Access Control:
Multi-level authentication untuk staff (role-based access)
Audit log untuk semua akses ke data sensitif
Biometric data hanya accessible oleh authentication engine, tidak oleh human operator
Estimasi Biaya Implementasi
Berdasarkan riset harga komponen:​

Hardware (untuk event 1000 pelari):
1000x RFID UHF BibTag: ~Rp 5.000.000 (@ Rp 5.000/chip)
5x RFID Reader & Antenna kit: ~Rp 50.000.000
3x Face Recognition Camera System: ~Rp 30.000.000
2x Fingerprint Scanner: ~Rp 5.000.000
Server & networking: ~Rp 20.000.000

Software:
Custom development (authentication + alert system): ~Rp 100.000.000 - 150.000.000
Face recognition SDK license (annual): ~Rp 30.000.000
Cloud hosting & database (per event): ~Rp 5.000.000
Total investasi awal: ~Rp 245.000.000 - 295.000.000
Operational cost per event: ~Rp 10.000.000 - 15.000.000

Keuntungan Sistem Ini
Untuk Panitia:
Mencegah kecurangan bib palsu yang merugikan pendapatan​
Meningkatkan kredibilitas dan reputasi event
Data real-time untuk race management
Bukti digital untuk dispute resolution

Untuk Pelari Legitimate:
Fair competition - tidak dirugikan oleh cheater​
Keamanan data pribadi terjaga
Hasil race yang akurat dan terpercaya
Emergency response lebih cepat (biometric linked to emergency contact)

Untuk Keamanan Event:
Deteksi dini anomali atau potensi bahaya
Tracking real-time posisi pelari
Integrasi dengan medical team untuk health monitoring​
Sistem ini mengkombinasikan teknologi RFID yang sudah mature untuk race timing dengan face recognition dan fingerprint authentication yang semakin terjangkau, menciptakan solusi anti-fraud yang komprehensif namun tetap user-friendly untuk race event di untuk race event di Indonesia.​
