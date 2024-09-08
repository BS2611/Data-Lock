import json
import os
from backend.system.scanfile import ScanFile
from backend.system.process import Process
from backend.system.network import Network
from backend.data.breach import Breach



def execute():
    while True:
        print("\n1. Files")
        print("2. Processes")
        print("3. Network")
        print("4. Check Involved in Data Breaches Or Not")
        choice = input("Enter the Choice number or type 'exit' to exit: ").strip().lower()

        if choice == 'exit' or choice == '-1':
            break

        if choice in ['1', 'file']:
            filescn = ScanFile()
            change_path = input("Scanning your downloads. Do you want to change the path (y/n)? ").strip().lower()

            if change_path == 'y':
                new_path = input("Enter path: ").strip()
                if os.path.exists(new_path):
                    filescn = ScanFile(new_path)
                else:
                    print("Invalid path. Please try again.")
                    continue

            suspicious_files = filescn.searchExecutablesSuspiciousFiles()
            print("These are the suspicious files:")
            for item in suspicious_files:
                print(item)

        elif choice in ['2', 'processes']:
            pr = Process()
            js =pr.getData()
            data = json.loads(js)
            formatted_text =''
            for item in data:
                formatted_text += f"Process Name: {item['ProcessName']}\n"
                formatted_text += f"Process ID: {item['ProcessId']}\n"
                formatted_text += f"Path: {item['Path']}\n"
                formatted_text += f"Publisher: {item['Publisher']}\n"
                formatted_text += "\n"  # Add a blank line between entries
            print(formatted_text)

        elif choice in ['3', 'network']:
            net = Network()
            print(f"Your network name is {net.get_network_ssid()}")
            if(net.is_public):
                print("Network type : Public")
            else:
                print("Network type : Private")
                if(net.is_authenticated()):
                    print("Your Network Is Protected!")
                else:
                    print("Your Network Is Not Protected, Be Careful!")
            print(f'Signal Stength: {net.get_signal_quality()}')
            if (net.is_firewall_enabled):
                print("Firewall is enabled, Suspicious Apps can't send your data to their servers")
            else:
                print("Firewall is not enabled, Suspicious Apps can send your data to their servers")


        elif choice in ['4', 'data breaches']:
            choice = input("Enter your emaild id")
            br = Breach(choice.trim())
            breaches = br.getBreaches()
            if breaches:
                print("Your data was compromised in")
                for item in breaches:
                    print(item)
            else:
                print("Your data was not compromised")




        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == '__main__':
    execute()
