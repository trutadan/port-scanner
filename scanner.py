import socket
import sys
from datetime import datetime


class ValidatorException(Exception):
    def __init__(self, errors):
        self.__errors = errors

    def get_errors(self):
        return self.__errors


def validate_arguments_passed():
    import re

    errors = list()

    if len(sys.argv) != 4:
        errors.append("The command must contain 3 arguments: \"scanner.py <ip> <starting_port> <ending_port>\"")

    target = sys.argv[1]

    ip_pattern = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if not re.search(ip_pattern, target):
        errors.append("Invalid IP address provided!")

    starting_port = sys.argv[2]
    if not starting_port.isnumeric():
        errors.append("Invalid starting port format provided!")

    ending_port = sys.argv[3]
    if not ending_port.isnumeric():
        errors.append("Invalid ending port format provided!")

    if len(errors):
        raise ValidatorException(errors)


class ScannerException(Exception):
    pass


def run_scanner():
    validate_arguments_passed()

    target = sys.argv[1]
    starting_port = int(sys.argv[2])
    ending_port = int(sys.argv[3])

    if starting_port > ending_port:
        ending_port, starting_port = starting_port, ending_port

    if starting_port < 0:
        starting_port = 0
        print("Since the value of the starting port was negative, the custom 0 value has been assigned.")

    if ending_port > 65535:
        ending_port = 65535
        print("Since the value of the starting port was too large, the custom 65535 value has been assigned.")

    starting_datetime = datetime.now()

    import texttable
    starting_banner = texttable.Texttable()
    starting_banner.add_row([f"Scanning target: {target}"])
    time_started = f"Time started: {starting_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
    starting_banner.add_row([time_started])

    print(starting_banner.draw())

    open_ports_counter = 0

    for port in range(starting_port, ending_port + 1):
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        scan_result = target_socket.connect_ex((target, port))

        if scan_result == 0:
            print(f"> port {port} is open")
            open_ports_counter += 1

        target_socket.close()

    ending_banner = texttable.Texttable()
    ending_banner.add_row([f"Open ports found: {open_ports_counter}"])
    scanning_time_spent = f"Scanning time spent: {(datetime.now() - starting_datetime).seconds} seconds".ljust(len(time_started))
    ending_banner.add_row([scanning_time_spent])

    print(ending_banner.draw())


if __name__ == '__main__':
    try:
        run_scanner()

    except ValidatorException as scanner_errors:
        for scanner_error in scanner_errors.get_errors():
            print(scanner_error)

    except KeyboardInterrupt:
        print("Exiting program...")

    except socket.gaierror:
        print("Hostname could not be resolved.")

    except socket.error:
        print("Couldn't connect to the server.")
