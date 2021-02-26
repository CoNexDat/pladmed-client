from math import floor

UDP_PACKET = 64 # Bytes

def rates_to_credits(rates, unit):
    #TODO Cover more units
    if unit == "Kbps":
        rates_in_bits = rates * 1000
        return floor((rates_in_bits * 8) / (UDP_PACKET**2))
