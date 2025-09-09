"""
BlackCell Security Toolkit - Utility Functions
"""

import re
import ipaddress
from pathlib import Path
from typing import List, Union

def is_valid_ip(ip: str) -> bool:
    """Check if string is a valid IP address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_domain(domain: str) -> bool:
    """Check if string is a valid domain name"""
    pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
    )
    return bool(pattern.match(domain))

def is_valid_url(url: str) -> bool:
    """Check if string is a valid URL"""
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))

def expand_ip_range(ip_range: str) -> List[str]:
    """Expand IP range or CIDR notation to list of IPs"""
    try:
        if '/' in ip_range:
            # CIDR notation
            network = ipaddress.ip_network(ip_range, strict=False)
            return [str(ip) for ip in network.hosts()]
        elif '-' in ip_range and ip_range.count('.') == 3:
            # Range notation (e.g., 192.168.1.1-10)
            start_ip, end_part = ip_range.split('-')
            start_parts = start_ip.split('.')
            end_num = int(end_part)
            start_num = int(start_parts[-1])
            
            base = '.'.join(start_parts[:-1])
            return [f"{base}.{i}" for i in range(start_num, end_num + 1)]
        else:
            # Single IP
            return [ip_range]
    except Exception:
        return [ip_range]

def validate_target(target: str) -> dict:
    """Validate and categorize target"""
    result = {
        'valid': False,
        'type': 'unknown',
        'target': target
    }
    
    if is_valid_ip(target):
        result['valid'] = True
        result['type'] = 'ip'
    elif is_valid_domain(target):
        result['valid'] = True
        result['type'] = 'domain'
    elif is_valid_url(target):
        result['valid'] = True
        result['type'] = 'url'
    elif '/' in target or '-' in target:
        # Might be IP range
        try:
            expand_ip_range(target)
            result['valid'] = True
            result['type'] = 'ip_range'
        except:
            pass
    
    return result