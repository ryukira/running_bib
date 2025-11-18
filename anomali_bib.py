# Sistem Deteksi Anomali Chip Bib

class BibAuthenticationSystem:
    def __init__(self):
        self.database = Database()
        self.face_recognition = FaceRecognitionEngine()
        self.alert_manager = AlertManager()
    
    def register_runner(self, runner_id, name, photo, fingerprint):
        """Registrasi pelari dengan data biometrik"""
        face_template = self.face_recognition.encode_face(photo)
        chip_id = self.generate_unique_chip_id()
        
        runner_data = {
            'runner_id': runner_id,
            'name': name,
            'bib_number': self.assign_bib_number(),
            'chip_id': chip_id,
            'face_template': face_template,
            'fingerprint_template': fingerprint,
            'registration_time': datetime.now(),
            'verified': False
        }
        
        self.database.save_runner(runner_data)
        return chip_id, runner_data['bib_number']
    
    def verify_at_checkpoint(self, chip_id, checkpoint_location, timestamp, photo=None):
        """Verifikasi chip di checkpoint dengan optional face verification"""
        runner = self.database.get_runner_by_chip(chip_id)
        
        if not runner:
            # Chip tidak terdaftar - potential counterfeit
            self.alert_manager.send_critical_alert(
                alert_type="COUNTERFEIT_CHIP",
                message=f"Unknown chip ID {chip_id} detected at {checkpoint_location}",
                location=checkpoint_location,
                timestamp=timestamp
            )
            return False
        
        # Log checkpoint passage
        self.database.log_checkpoint(chip_id, checkpoint_location, timestamp)
        
        # Validasi waktu antar checkpoint
        if not self.validate_checkpoint_timing(chip_id, checkpoint_location, timestamp):
            self.alert_manager.send_warning_alert(
                alert_type="IMPOSSIBLE_TIMING",
                runner_name=runner['name'],
                bib_number=runner['bib_number'],
                message=f"Impossible time detected between checkpoints",
                details=self.get_checkpoint_history(chip_id)
            )
        
        # Face verification jika ada foto
        if photo is not None:
            match_confidence = self.face_recognition.match_faces(
                photo, 
                runner['face_template']
            )
            
            if match_confidence < 0.95:  # Threshold 95%
                self.alert_manager.send_alert(
                    alert_type="FACE_MISMATCH",
                    severity="HIGH",
                    runner_name=runner['name'],
                    bib_number=runner['bib_number'],
                    chip_id=chip_id,
                    location=checkpoint_location,
                    match_confidence=match_confidence,
                    photo_url=self.upload_evidence_photo(photo)
                )
                return False
        
        return True
    
    def validate_checkpoint_timing(self, chip_id, current_checkpoint, current_time):
        """Validasi apakah waktu antar checkpoint masuk akal"""
        history = self.database.get_checkpoint_history(chip_id)
        
        if len(history) == 0:
            return True
        
        last_checkpoint = history[-1]
        time_diff = (current_time - last_checkpoint['timestamp']).total_seconds()
        distance = self.get_distance_between_checkpoints(
            last_checkpoint['location'], 
            current_checkpoint
        )
        
        # Minimum waktu tempuh (asumsi: tidak mungkin lebih cepat dari 3 min/km)
        min_time_required = (distance / 1000) * 180  # seconds
        
        # Maximum waktu tempuh (asumsi: tidak mungkin lebih lambat dari 12 min/km)
        max_time_required = (distance / 1000) * 720  # seconds
        
        if time_diff < min_time_required or time_diff > max_time_required:
            return False
        
        return True
    
    def check_missing_checkpoints(self, chip_id, current_checkpoint):
        """Cek apakah ada checkpoint wajib yang dilewati"""
        mandatory_checkpoints = self.get_mandatory_checkpoints()
        passed_checkpoints = self.database.get_passed_checkpoints(chip_id)
        
        expected_checkpoints = []
        for cp in mandatory_checkpoints:
            if self.is_before(cp, current_checkpoint):
                expected_checkpoints.append(cp)
        
        missing = set(expected_checkpoints) - set(passed_checkpoints)
        
        if missing:
            runner = self.database.get_runner_by_chip(chip_id)
            self.alert_manager.send_warning_alert(
                alert_type="MISSING_CHECKPOINT",
                runner_name=runner['name'],
                bib_number=runner['bib_number'],
                message=f"Missed mandatory checkpoints: {', '.join(missing)}"
            )
            return False
        
        return True


class AlertManager:
    def __init__(self):
        self.notification_service = NotificationService()
    
    def send_critical_alert(self, alert_type, message, location, timestamp):
        """Kirim alert kritikal ke semua channel"""
        alert = {
            'severity': 'CRITICAL',
            'type': alert_type,
            'message': message,
            'location': location,
            'timestamp': timestamp,
            'status': 'ACTIVE'
        }
        
        # Dashboard update
        self.notification_service.update_dashboard(alert)
        
        # Mobile push notification ke security team
        self.notification_service.push_to_mobile(
            recipients=['security_team'],
            title='CRITICAL: Counterfeit Chip Detected',
            body=message
        )
        
        # SMS ke race director
        self.notification_service.send_sms(
            recipients=['race_director'],
            message=f"CRITICAL ALERT: {message}"
        )
        
        # Log ke database
        self.notification_service.log_alert(alert)
    
    def send_warning_alert(self, alert_type, runner_name, bib_number, message, details=None):
        """Kirim warning alert untuk investigasi"""
        alert = {
            'severity': 'WARNING',
            'type': alert_type,
            'runner_name': runner_name,
            'bib_number': bib_number,
            'message': message,
            'details': details,
            'timestamp': datetime.now(),
            'status': 'PENDING_REVIEW'
        }
        
        # Dashboard update dengan highlight
        self.notification_service.update_dashboard(alert)
        
        # Email ke timing team
        self.notification_service.send_email(
            recipients=['timing_team@race.com'],
            subject=f'Warning: Bib #{bib_number} - {alert_type}',
            body=self.format_alert_email(alert)
        )
        
        # Log untuk review
        self.notification_service.log_alert(alert)
    
    def send_alert(self, alert_type, severity, runner_name, bib_number, chip_id, 
                   location, match_confidence, photo_url):
        """Kirim alert untuk face mismatch"""
        alert = {
            'severity': severity,
            'type': alert_type,
            'runner_name': runner_name,
            'bib_number': bib_number,
            'chip_id': chip_id,
            'location': location,
            'match_confidence': match_confidence,
            'evidence_photo': photo_url,
            'timestamp': datetime.now(),
            'action_required': 'MANUAL_VERIFICATION'
        }
        
        # Update dashboard dengan foto bukti
        self.notification_service.update_dashboard_with_photo(alert)
        
        # Kirim ke field marshall terdekat
        self.notification_service.push_to_nearest_official(
            location=location,
            alert=alert
        )
        
        # Flag hasil pelari untuk review
        self.notification_service.flag_result_for_review(bib_number)
