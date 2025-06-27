# DNS Changer Utility

A cross-platform Python script to easily change DNS settings with a user-friendly menu interface.

## Features

- 🖥️ **Cross-platform** - Works on Windows, Linux, and macOS
- 📶 **Multiple interface support** - Choose which network interface to configure
- 🔄 **Quick DNS switching** - Change between popular DNS providers instantly
- ⚙️ **Custom DNS support** - Enter your own DNS servers
- 🔄 **Reset functionality** - Restore default DHCP settings
- 📊 **Current DNS view** - See active DNS configuration

## Supported DNS Providers

| Provider   | Primary DNS    | Secondary DNS  |
|------------|----------------|----------------|
| Cloudflare | 1.1.1.1        | 1.0.0.1        |
| Google     | 8.8.8.8        | 8.8.4.4        |
| OpenDNS    | 208.67.222.222 | 208.67.220.220 |
| Shecan     | 185.51.200.2   | 178.22.122.100 |

## Installation

### Prerequisites
- Python 3.6+
- On Linux: `network-manager` and `nmcli`
- On Windows: Administrative privileges

### Method 1: Direct Download
```bash
git clone https://raw.githubusercontent.com/yourusername/dns-changer/main/dns_changer.py](https://github.com/Saeed-Shirazi-1997/dns-der.git
chmod +x dns_changer.py
