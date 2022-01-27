import os

from netmiko import ConnectHandler
from halo import Halo


class Connection(object):
    """
    Takes dict as argument and returns connection.
    Dict format:
    {'ip': SwitchIPAddress,
    'device_type': SwitchType,  (refer to netmiko documentation for details)
    'username': SwitchUsername,
    'password': SwitchPassword
    }
    """

    def __init__(self, coninfo: dict):
        self.coninfo = coninfo

    def connect(self):
        return ConnectHandler(**self.coninfo)


def ping_from_switch(switch_ip: str, ip_list: list[str], coninfo: dict) -> None:
    """
    Pings list of IPs from switch. Used primarily for populating ARP table.
    :param coninfo: Dictionary of connection info
    :param switch_ip: IP of switch to ping from
    :param ip_list: List of IP addresses to ping
    :return: None
    """
    spinner = Halo(spinner='dots')
    spinner.start(f'\nConnecting to {switch_ip}')
    connection = Connection(coninfo).connect()
    spinner.succeed()
    spinner.stop()
    for ip in ip_list:
        spinner.start(f'\nPinging {ip} from switch {switch_ip}')
        connection.send_command(f'ping {ip}')
        spinner.succeed()
        spinner.stop()
    connection.disconnect()


def run_commands(ip: str, commands: list[str], coninfo: dict) -> None:
    """
    Cycles through a list of 'show' commands to run on a switch
    :param coninfo: Dictionary with connecion info
    :param ip: Address of switch as String
    :param commands: Command to run on switch
    :return: None
    """
    spinner = Halo(spinner='dots')
    spinner.start(f'Connecting to {ip}')
    connection = Connection(coninfo).connect
    spinner.succeed()
    spinner.stop()
    for command in commands:
        spinner.start(f'\nRunning "{command}" on switch at {ip}. This might take a bit.')
        return_data = connection.send_command(command)
        spinner.succeed()
        spinner.stop()
        command = command.replace(' ', '_').replace('-', '_')
        spinner.start(f'\nWriting {command} to switch_{command}/{ip}')
        if not os.path.exists(f'switch_{command}'):
            os.mkdir(f'switch_{command}')
        with open(f'switch_{command}/{ip}', 'w+') as f:
            f.write(return_data)
        spinner.succeed(f'\nCommand "show {command}" on {ip} completed and written to switch_{command}/{ip}')
        spinner.stop()
    spinner.start(f'\nClosing connection to {ip}')
    connection.disconnect()
    spinner.succeed()
    spinner.stop()
