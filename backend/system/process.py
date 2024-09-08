import subprocess
import json

class Process:
    def run_powershell_script(self,script_path):
        # Command to execute the PowerShell script
        command = ['powershell', '-ExecutionPolicy', 'Bypass', '-File', script_path]

        print(f"Executing command: {' '.join(command)}")  # Print the command for debugging

        try:
            # Run the PowerShell script and capture the output
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            output = result.stdout
            if not output.strip():
                raise ValueError("No output received from PowerShell script.")
            return output
        except subprocess.CalledProcessError as e:
            print(f"Error running PowerShell script: {e}")
            print(f"Return code: {e.returncode}")  # Print the return code
            print(f"Stderr: {e.stderr}")  # Print the stderr for debugging
            return None
        except ValueError as e:
            print(e)
            return None

    def parse_json_output(self,output):
        try:
            # Parse the output as a single JSON array
            unknown_processes = json.loads(output)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            unknown_processes = []

        return unknown_processes
    def getData(self):
        # Path to the PowerShell script
        script_path = '.\check_unknown_publishers.ps1'

        # Run the PowerShell script
        output = self.run_powershell_script(script_path)

        if output:
            # Parse the JSON output
            unknown_processes = self.parse_json_output(output)

            return  unknown_processes
        else:
            return None