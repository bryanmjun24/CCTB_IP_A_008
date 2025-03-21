import sys
import json
import re
import random

# Predefined subnets
IPV4_SUBNET = "192.168.1."
IPV6_SUBNET = "2001:db8::"

# Lease database (temporary storage)
LEASES = {}

# Validate MAC address format
def validate_mac(mac):
    return re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', mac) is not None

# Generate IPv4 address dynamically
def assign_ipv4():
    for i in range(10, 255):
        ip = f"{IPV4_SUBNET}{i}"
        if ip not in LEASES.values():
            return ip
    return None  # No available IPs

# Generate IPv6 address using EUI-64 format
def generate_ipv6(mac):
    mac_parts = mac.split(":")
    mac_parts[0] = f"{int(mac_parts[0], 16) ^ 0x02:02x}"  # Modify U/L bit
    eui64 = f"{mac_parts[0]}{mac_parts[1]}:{mac_parts[2]}ff:fe{mac_parts[3]}:{mac_parts[4]}{mac_parts[5]}"
    return f"{IPV6_SUBNET}{eui64}"

# Main function to process DHCP request
def process_dhcp_request(mac, dhcp_version):
    if not validate_mac(mac):
        return json.dumps({"error": "Invalid MAC address format."})

    if mac in LEASES:
        assigned_ip = LEASES[mac]  # Reuse existing lease
    else:
        if dhcp_version == "DHCPv4":
            assigned_ip = assign_ipv4()
            lease_time = "3600 seconds"
        elif dhcp_version == "DHCPv6":
            assigned_ip = generate_ipv6(mac)
            lease_time = "No expiration (IPv6 SLAAC)"
        else:
            return json.dumps({"error": "Invalid DHCP version selected."})

        if assigned_ip is None:
            return json.dumps({"error": "No available IPs in the subnet."})

        LEASES[mac] = assigned_ip  # Store lease

    return json.dumps({
        "mac_address": mac,
        "assigned_ip": assigned_ip,
        "lease_time": lease_time
    })

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing input parameters."}))
    else:
        mac_address = sys.argv[1]
        dhcp_version = sys.argv[2]
        print(process_dhcp_request(mac_address, dhcp_version))
