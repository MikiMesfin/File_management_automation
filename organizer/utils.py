import os
import shutil
import mimetypes
from datetime import datetime

class FileOrganizer:
    def __init__(self, base_path):
        self.base_path = base_path
        self.type_folders = {
            'image': ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
            'document': ['application/pdf', 'application/msword', 
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        'text/plain'],
            'video': ['video/mp4', 'video/mpeg', 'video/quicktime', 'video/x-msvideo'],
            'audio': ['audio/mpeg', 'audio/wav', 'audio/midi', 'audio/x-midi'],
            'archive': ['application/zip', 'application/x-rar-compressed', 
                       'application/x-tar', 'application/gzip']
        }

    def organize_file(self, file_path):
        # Guess the file type using mimetypes
        file_type, _ = mimetypes.guess_type(file_path)
        if file_type is None:
            file_type = 'application/octet-stream'
            
        file_name = os.path.basename(file_path)
        
        # Determine folder based on file type
        target_folder = 'others'
        for folder, types in self.type_folders.items():
            if file_type in types:
                target_folder = folder
                break

        # Create year/month based structure
        date = datetime.now()
        year_month = f"{date.year}/{date.month:02d}"
        target_path = os.path.join(self.base_path, target_folder, year_month)
        
        # Create directory if it doesn't exist
        os.makedirs(target_path, exist_ok=True)
        
        # Handle duplicate filenames
        new_path = os.path.join(target_path, file_name)
        base_name, extension = os.path.splitext(file_name)
        counter = 1
        
        while os.path.exists(new_path):
            new_file_name = f"{base_name}_{counter}{extension}"
            new_path = os.path.join(target_path, new_file_name)
            counter += 1
        
        # Move file to new location
        shutil.move(file_path, new_path)
        
        return new_path 