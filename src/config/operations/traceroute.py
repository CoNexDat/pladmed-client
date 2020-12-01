from utils.command_validator import (
    AnyValidator,
    BetweenValidator,
    MultiValueValidator
)
from utils.command_manager import (
    CommandManager,
    MultiCommandManager
)

DNS_PARAMS = {
    "name": CommandManager("-q", AnyValidator())
}

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

GENERAL_PARAMS = {
    "ips": MultiCommandManager("-i", AnyValidator())
}
