from utils.command_validator import (
    AnyValidator,
    EmptyValidator,
    MultiValueValidator
)

from utils.command_manager import (
    CommandManager
)

DNS_PARAMS = {
    "address": CommandManager("-b", AnyValidator()),
    "ipv4": CommandManager("-4", EmptyValidator()),
    "ipv6": CommandManager("-6", EmptyValidator()),
    "name": CommandManager("-q", AnyValidator()),
    "type": CommandManager("-P", MultiValueValidator([
        "a", "any", "axfr", "hinfo", "mx", "ns", "soa", "txt"
    ]))
}
