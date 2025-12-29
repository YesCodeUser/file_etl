from datetime import datetime

class ValidationResult:
    def __init__(self, file_path):
        self.file_path = file_path

        self.errors = []
        self.system_error = None
        self.valid_rows = []

        self.amount_rows = 0
        self.amount_valid_rows = 0
        self.amount_invalid_rows = 0
        self.status = None
        self.processed_at = datetime.now().strftime('%d.%m.%Y %H:%M')