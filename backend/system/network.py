import subprocess
import re


class Network:
    is_public = False
    is_firewall_enabled = False
    wifi_info = {}

    def __run_ps_command(self, command):
        obj = {}
        # Run the command using PowerShell
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        # Output the result
        output = result.stdout.strip()
        output = output.replace("Public Profile Settings:", "")
        # print(output)

        for line in output.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                obj[key] = value
            if line.startswith("State"):
                match = re.search(r'(\S+)\s+(\S+)', line)

                if match:
                    state_key = match.group(1)
                    state_value = match.group(2)

                    # Format the output as State:"ON"
                    obj = {state_key: state_value}

        return obj

    def __init__(self):
        self.get_network_info()

    def get_network_info(self):
        net_info_command = "netsh wlan show interfaces"

        self.wifi_info = self.__run_ps_command(net_info_command)
        net_status_command = " Get-NetConnectionProfile"
        net_stat = self.__run_ps_command(net_status_command)
        self.is_public = True if net_stat.get("NetworkCategory") == "Public" else False
        self.wifi_info["isPublic"] = self.is_public
        firewall_stat = self.__run_ps_command("netsh advfirewall show currentprofile")
        self.is_firewall_enabled = True if (firewall_stat.get("State") == "ON") else False
        self.wifi_info["isFirewallEnabled"] = self.is_firewall_enabled


    def is_authenticated(self):
        return self.wifi_info.get("Authentication") != "Open"

    def get_network_ssid(self):
        return self.wifi_info.get("SSID")

    def get_signal_quality(self):
        signal = self.wifi_info.get("Signal", "0%").replace("%", "")
        signal = int(signal)
        if signal >= 90:
            return "Excellent"
        elif signal >= 80:
            return "Good"
        elif signal >= 70:
            return "Ok"
        else:
            return "Bad"

    def is_firewall(self):
        return self.is_firewall_enabled

