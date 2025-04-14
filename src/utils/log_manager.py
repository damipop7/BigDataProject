import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from datetime import datetime

class LogManager:
    """Manages log files and rotation"""
    
    def __init__(self, log_dir='logs'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create .gitkeep to preserve empty directory
        (self.log_dir / '.gitkeep').touch()
        
    def setup_logger(self, name, log_file, level=logging.INFO):
        """Setup a new logger with rotation"""
        logger = logging.getLogger(name)
        
        # Avoid duplicate handlers
        if logger.handlers:
            return logger
            
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            self.log_dir / log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=30
        )
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.setLevel(level)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
        
    def cleanup_old_logs(self, days=30):
        """Remove logs older than specified days"""
        current_time = datetime.now()
        for log_file in self.log_dir.glob('*.log.*'):
            if (current_time - datetime.fromtimestamp(log_file.stat().st_mtime)).days > days:
                log_file.unlink()