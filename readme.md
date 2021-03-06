# net-switch-tools

Python package for managing network switches

## Usage

```python
import manage_switches.All

# Connection info for logging in to switch

coninfo = {
    'ip': 'IP_OF_SWITCH',
    'device_type': 'TYPE_OF_DEVICE', # Refer to NetMiko docs for switch type
    'username': 'SWITCH_USERNAME',
    'password': 'SWITCH_PASSWORD'
}

# Get list of IPs in a CIDR network range

ip_list = generate_ip_list('192.168.1.0/24')

# Get hostname from IP address, or returns 'Hostname not found' if no hostname

hostname = get_hostname_by_ip('192.168.1.5')

# Ping list of IP addresses from switch

ping_from_switch(coninfo, ip_list)

# Run commands on switch. Writes output to D 'switch_{command_slug}/{switch_ip}

run_commands(coninfo, ['show arp', 'show mac-address'])

# Run functions concurrently. Supports functions that take IP address as an arg

multithread(get_hostname_by_ip, ip_list)

# Write results of command CSV, saves file as {prepend}-{variable_name}.csv

result = [
    {'IP': '192.168.1.1', 'Hostname': 'router.local'},
    {'IP': '192.168.1.2', 'Hostname': 'computer1'},
    {'IP': '192.168.1.1', 'Hostname': 'computer2'},
    {'IP': '192.168.1.1', 'Hostname': 'computer3'},
]

write_result(result, 'w+', 'switch_ip')

# Reformat MAC address to a1-a1-a1-a1-a1-a1 format

fixed_mac = reformat_mac('a1:a1:a1:a1:a1:a1')

```

## Example
```python
import sys

import manage_switches.All

from secret import IP_RANGE, USERNAME, PASSWORD, DEVICE_TYPE


def write_arp_tables(ip: str):
    """
    Retrieves ARP table from switch. Writes remote device IP, remote device
    MAC, remote device hostname, switch ip, and switch port the remote
    device is connected too into a CSV file.
    :param ip: IP address of switch as string
    :return: Success string 'Success on {ip}'
    """
    spinner = Halo(spinner='dots')
    try:
        coninfo = {
            'ip': ip,
            'device_type': DEVICE_TYPE,
            'username': USERNAME,
            'password': PASSWORD
        }
        commands = ['show arp']
        run_commands(coninfo, commands)
        arp_list = []
        spinner.start(f'\nGetting ARP table from switch at {ip}')
        with open(f'switch_show_arp/{ip}', 'r') as f:
            raw_arp_table = f.read()
        spinner.succeed()
        spinner.stop()
        spinner.start(f'\nFormatting ARP table and writing to file.')
        fixed_arp_list = [x.strip() for x in raw_arp_table.split("\n")[6:-2]]
        # You'll need to figure this out for your specific switch output
        for item in fixed_arp_list:
            item = item.replace('     ', ' ')
                .replace('    ', ' ')
                .replace('   ', ' ')
                .replace('  ', ' ')
            item = item.split(' ')
            if len(item) > 3:
                arp_list.append({
                    'IP': item[0],
                    'MAC': reformat_mac(item[1]),
                    'Hostname': get_hostname_by_ip(item[0]),
                    'Switch IP': ip,
                    'Switch Port': item[3]
                })
        write_result_csv(arp_list, 'a+', prepend=ip)
        spinner.succeed(f'\nFile written to {ip}-srp_list.csv')
        spinner.stop()
        return f'Success on {ip}'
    except (KeyboardInterrupt, SystemExit):
        spinner.stop()


def populate_arp_table(ip: str):
    """
    Logs into switch, pings every address in IP_RANGE to populate ARP table
    :param ip: IP address of switch as string
    :return: Success string 'Success on {ip}'
    """
    try:
        coninfo = {
            'ip': ip,
            'device_type': DEVICE_TYPE,
            'username': USERNAME,
            'password': PASSWORD
        }
        ip_list = generate_ip_list(IP_RANGE)
        ping_from_switch(coninfo, ip_list)
        return f'Success on {ip}'
    except (KeyboardInterrupt, SystemExit):
        sys.exit()


if __name__ == '__main__':
    switch_ips = []
    ip_list = generate_ip_list(IP_RANGE)
    with open('SwitchAddresses.csv', 'r') as f:
        for row in csv.reader(f):
            switch_ips.append(row[0])
    multithread(populate_arp_table, switch_ips)
    multithread(write_arp_tables, switch_ips)

```