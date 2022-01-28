# net-switch-tools

Python package for managing network switches

## Usage

```python
import src.manage_switches.All

# Connection info for logging in to switch

coninfo = {
    'ip': 'IP_OF_SWITCH',
    'device_type': 'TYPE_OF_DEVICE', # Refer to NetMiko docs to identify tour switch type
    'username': 'SWITCH_USERNAME',
    'password': 'SWITCH_PASSWORD'
}

# Get list of IPs in a CIDR network range

ip_list = generate_ip_list('192.168.1.0/24')

# Get hostname from IP address, or returns 'Hostname not found' if no hostname

hostname = get_hostname_by_ip('192.168.1.5')

# Ping list of IP addresses from switch

ping_from_switch(coninfo, ip_list)

# Run list of commands on switch. Writes output to file in CWD 'switch_{command_slug}/{switch_ip}

run_commands(coninfo, ['show arp', 'show mac-address'])

# Run functions concurrently. Currently only supports functions that take only an IP address as an argument

multithread(get_hostname_by_ip, ip_list)

# Write results of command that writes dictionary list to a CSV, saves file as {prepend}-{variable_name}.csv

result = [
    {'IP': '192.168.1.1', 'Hostname': 'router.local'},
    {'IP': '192.168.1.2', 'Hostname': 'computer1'},
    {'IP': '192.168.1.1', 'Hostname': 'computer2'},
    {'IP': '192.168.1.1', 'Hostname': 'computer3'},
]

write_result(result, 'w+', 'switch_ip')
```