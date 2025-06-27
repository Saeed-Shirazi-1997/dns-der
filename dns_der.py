import os
import sys
import subprocess
from time import sleep

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def change_dns(interface, dns_servers):
    if os.name == 'nt':  # Windows
        for i, server in enumerate(dns_servers, 1):
            subprocess.run(f'netsh interface ipv4 set dns name="{interface}" static {server} validate=no', shell=True)
            if i == 1:  # Set primary DNS
                pass
            else:  # Set secondary DNS
                subprocess.run(f'netsh interface ipv4 add dns name="{interface}" {server} index={i} validate=no', shell=True)
    else:  # Linux/Mac
        for server in dns_servers:
            subprocess.run(f'sudo nmcli con mod {interface} ipv4.dns "{server}"', shell=True)
        subprocess.run(f'sudo nmcli con up {interface}', shell=True)

def reset_dns(interface):
    if os.name == 'nt':  # Windows
        subprocess.run(f'netsh interface ipv4 set dns name="{interface}" dhcp', shell=True)
    else:  # Linux/Mac
        subprocess.run(f'sudo nmcli con mod {interface} ipv4.dns ""', shell=True)
        subprocess.run(f'sudo nmcli con up {interface}', shell=True)

def get_interfaces():
    if os.name == 'nt':  # Windows
        result = subprocess.run('netsh interface show interface', shell=True, capture_output=True, text=True)
        interfaces = []
        for line in result.stdout.split('\n')[3:]:
            if line.strip():
                parts = line.split()
                if len(parts) > 3 and parts[3] == "Connected":
                    interfaces.append(parts[-1])
        return interfaces
    else:  # Linux/Mac
        result = subprocess.run('nmcli connection show', shell=True, capture_output=True, text=True)
        interfaces = []
        for line in result.stdout.split('\n')[1:]:
            if line.strip():
                interfaces.append(line.split()[0])
        return interfaces

def show_menu():
    clear_screen()
    print("""
    ██████╗ ███╗   ██╗███████╗    ██████╗ ███████╗██████╗ 
    ██╔══██╗████╗  ██║██╔════╝    ██╔══██╗██╔════╝██╔══██╗
    ██║  ██║██╔██╗ ██║███████╗    ██║  ██║█████╗  ██████╔╝
    ██║  ██║██║╚██╗██║╚════██║    ██║  ██║██╔══╝  ██╔══██╗
    ██████╔╝██║ ╚████║███████║    ██████╔╝███████╗██║  ██║
    ╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝
    
    DNS Changer Script
    ----------------------------
    1. Set Cloudflare DNS (1.1.1.1, 1.0.0.1)
    2. Set Google DNS (8.8.8.8, 8.8.4.4)
    3. Set OpenDNS (208.67.222.222, 208.67.220.220)
    4. Set Shecan DNS (185.51.200.2, 178.22.122.100)
    5. Set Custom DNS
    6. Reset DNS to DHCP
    7. Show Current DNS
    0. Exit
    ----------------------------
    """)

def get_current_dns(interface):
    if os.name == 'nt':  # Windows
        result = subprocess.run(f'netsh interface ipv4 show dnsservers "{interface}"', shell=True, capture_output=True, text=True)
        return result.stdout
    else:  # Linux/Mac
        result = subprocess.run(f'nmcli device show {interface} | grep IP4.DNS', shell=True, capture_output=True, text=True)
        return result.stdout

def main():
    if not is_admin():
        print("This script requires administrator privileges. Please run as admin.")
        if os.name == 'nt':
            print("On Windows: Right-click and select 'Run as administrator'")
        else:
            print("On Linux/Mac: Use sudo")
        sleep(3)
        sys.exit(1)

    interfaces = get_interfaces()
    if not interfaces:
        print("No network interfaces found!")
        sleep(2)
        sys.exit(1)

    if len(interfaces) == 1:
        selected_interface = interfaces[0]
    else:
        print("Available network interfaces:")
        for i, interface in enumerate(interfaces, 1):
            print(f"{i}. {interface}")
        
        try:
            choice = int(input("Select interface: "))
            selected_interface = interfaces[choice-1]
        except (ValueError, IndexError):
            print("Invalid selection!")
            sleep(1)
            return

    dns_options = {
        1: ["1.1.1.1", "1.0.0.1"],
        2: ["8.8.8.8", "8.8.4.4"],
        3: ["208.67.222.222", "208.67.220.220"],
        4: ["185.51.200.2", "178.22.122.100"]  # Shecan DNS
    }

    while True:
        show_menu()
        try:
            choice = int(input("Select option: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            sleep(1)
            continue

        if choice == 0:
            print("Exiting...")
            break
        elif choice in dns_options:
            print(f"Changing DNS to {dns_options[choice]}...")
            change_dns(selected_interface, dns_options[choice])
            print("Done!")
            sleep(2)
        elif choice == 5:
            custom_dns = input("Enter DNS servers separated by commas (e.g., 1.1.1.1,1.0.0.1): ")
            dns_servers = [s.strip() for s in custom_dns.split(',') if s.strip()]
            if dns_servers:
                print(f"Changing DNS to {dns_servers}...")
                change_dns(selected_interface, dns_servers)
                print("Done!")
            else:
                print("No valid DNS servers entered!")
            sleep(2)
        elif choice == 6:
            print("Resetting DNS to DHCP...")
            reset_dns(selected_interface)
            print("Done!")
            sleep(2)
        elif choice == 7:
            print(f"\nCurrent DNS for {selected_interface}:")
            print(get_current_dns(selected_interface))
            input("\nPress Enter to continue...")
        else:
            print("Invalid option! Please enter a number between 0-7.")
            sleep(1)

if __name__ == "__main__":
    main()