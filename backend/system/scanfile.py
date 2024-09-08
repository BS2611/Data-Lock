import os
import re
import subprocess
import json
class ScanFile:
    file_types = ['.exe', '.bat']
    directory = r'C:\\Users\\bhav\Downloads'
    excludedPaths =""
    data_path =os.path.join(os.path.dirname(__file__), '..', '..', 'data.json')
    def __init__(self):
        data=""
        with open(self.data_path, 'r') as file:
            data = json.load(file)
        self.excludedPaths =data.get("excludedPaths")
        print(self.excludedPaths)

    def __init__(self,path):
        self.directory =path
        data = ""
        with open(self.data_path, 'r') as file:
            data = json.load(file)
        self.excludedPaths = data.get("excludedPaths")
        print(self.excludedPaths)
    def isSigned(self, file_path):
        is_signed = False
        # Escape double quotes in the path for PowerShell
        escaped_file_path = file_path.replace('"', '`"')
        # Command to run in PowerShell
        command = f'(Get-AuthenticodeSignature "{escaped_file_path}").Status'

        # Run the command using PowerShell
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)

        # Output the result
        status = result.stdout.strip()
        if not status:
            status = 'No output or empty'

        if str(status).lower() =="valid":
            is_signed =True
        return is_signed

    def is_double_extension(self, filename):
        # Regex to detect double extensions
        double_extension_pattern = r'\.[^.\\/:*?"<>|\r\n]+?\.(exe|bat|cmd|com)$'
        return re.search(double_extension_pattern, filename.lower())
    def searchExecutablesSuspiciousFiles(self):
        suspicious_files =[]
        for root, dirs, files in os.walk(self.directory):
            if any(excluded_path in root for excluded_path in self.excludedPaths):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                if any(file.endswith(item) for item in self.file_types):
                    # Corrected the line to join the root and file paths
                    print({file_path:self.isSigned(file_path)})
                    suspicious_files.append(file_path)

                elif self.is_double_extension(file):
                    suspicious_files.append(file_path)
        return suspicious_files
