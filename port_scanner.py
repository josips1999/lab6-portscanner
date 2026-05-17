#!/usr/bin/env python3
"""Simple TCP port scanner using Python sockets.

Supports single port, port ranges, and multiple hosts. Uses threads
to scan ports in parallel and reports open ports and common service names.
"""
import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple


def scan_port(host: str, port: int, timeout: float) -> Tuple[int, bool, str]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        try:
            service = socket.getservbyport(port, 'tcp')
        except OSError:
            service = ''
        return port, True, service
    except (socket.timeout, ConnectionRefusedError, OSError):
        return port, False, ''
    finally:
        s.close()


def scan_host_ports(host: str, ports: List[int], timeout: float, workers: int) -> List[Tuple[int, str]]:
    open_ports = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(scan_port, host, p, timeout): p for p in ports}
        for fut in as_completed(futures):
            port, ok, service = fut.result()
            if ok:
                open_ports.append((port, service))
    open_ports.sort()
    return open_ports


def parse_ports(args) -> List[int]:
    if args.port:
        p = int(args.port)
        if not (1 <= p <= 65535):
            raise argparse.ArgumentTypeError('port out of range')
        return [p]
    start = int(args.start)
    end = int(args.end)
    if not (1 <= start <= 65535 and 1 <= end <= 65535 and start <= end):
        raise argparse.ArgumentTypeError('invalid port range; must be 1-65535')
    return list(range(start, end + 1))


def main():
    parser = argparse.ArgumentParser(description='Simple TCP port scanner')
    parser.add_argument('--hosts', '-H', required=True,
                        help='Comma-separated list of hosts (names or IPs)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--port', '-p', help='Single port to scan')
    group.add_argument('--range', nargs=2, metavar=('START', 'END'))
    parser.add_argument('--start', default=1, help=argparse.SUPPRESS)
    parser.add_argument('--end', default=1024, help=argparse.SUPPRESS)
    parser.add_argument('--timeout', '-t', type=float, default=0.5,
                        help='Socket timeout in seconds (default: 0.5)')
    parser.add_argument('--workers', '-w', type=int, default=100,
                        help='Number of parallel worker threads (default: 100)')

    args = parser.parse_args()

    # Support --range START END as convenience (maps to hidden start/end)
    if args.range:
        args.start, args.end = args.range

    ports = parse_ports(args)
    hosts = [h.strip() for h in args.hosts.split(',') if h.strip()]

    socket.setdefaulttimeout(args.timeout)

    for host in hosts:
        try:
            resolved = socket.gethostbyname(host)
        except socket.gaierror:
            print(f'Could not resolve host: {host}')
            continue

        print(f'Scanning {host} ({resolved}) ports {ports[0]}-{ports[-1]}')
        open_ports = scan_host_ports(resolved, ports, args.timeout, args.workers)
        if open_ports:
            print(f'Open ports on {host}:')
            for port, service in open_ports:
                if service:
                    print(f' - {port} ({service})')
                else:
                    print(f' - {port}')
        else:
            print(f'No open TCP ports found on {host} in the scanned range.')
        print()


if __name__ == '__main__':
    main()
