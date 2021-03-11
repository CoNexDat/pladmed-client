from utils.command_validator import (
    AnyValidator,
    BetweenValidator,
    MultiValueValidator,
    EmptyValidator
)

from utils.command_manager import (
    CommandManager,
    MultiCommandManager
)

TRACEROUTE_PARAMS = {
    "confidence": CommandManager("-c", BetweenValidator(0, 0.99)),
    "method": CommandManager("-P", MultiValueValidator(["udp-paris", "icmp-paris", "icp"])),
    "dport": CommandManager("-d", AnyValidator()),
    "firsthop": CommandManager("-f", AnyValidator()),
    "maxttl": CommandManager("-m", BetweenValidator(1, 255)),
    "attempts": CommandManager("-q", BetweenValidator(1, 10)),
    "sport": CommandManager("-s", AnyValidator()),
    "wait": CommandManager("-w", BetweenValidator(1, 20)),
    "wait-probe": CommandManager("-W", BetweenValidator(0, 100))
}

PING_PARAMS = {
    "probecount": CommandManager("-c", BetweenValidator(1, 100)),
    "icmp-sum": CommandManager("-C", AnyValidator()),
    "dport": CommandManager("-d", AnyValidator()),
    "sport": CommandManager("-F", AnyValidator()),
    "wait": CommandManager("-i", BetweenValidator(1, 20)),
    "method": CommandManager("-P", MultiValueValidator(["icmp-echo", "icmp-time", "tcp-syn", "tcp-ack", "tcp-ack-sport", "udp", "udp-dport"])),
    "size": CommandManager("-s", BetweenValidator(1, 255)),
    "timeout": CommandManager("-W", BetweenValidator(0, 100))
}

DNS_PARAMS = {
    "address": CommandManager("-b", AnyValidator()),
    "ipv4": CommandManager("-4", EmptyValidator()),
    "ipv6": CommandManager("-6", EmptyValidator()),
    "name": MultiCommandManager("-q", AnyValidator()),
    "type": CommandManager("-P", MultiValueValidator([
        "a", "any", "axfr", "hinfo", "mx", "ns", "soa", "txt"
    ]))
}

GENERAL_PARAMS = {
    "ips": MultiCommandManager("-i", AnyValidator())
}
