"""
BlackCell Security Toolkit - Payload Encoder
"""

import base64
import urllib.parse
import html
import codecs
from typing import Dict, Callable
from blackcell.core.logger import setup_logger

class PayloadEncoder:
    """Encode payloads for various contexts"""
    
    def __init__(self):
        self.logger = setup_logger("payload_encoder")
        
        # Encoding methods mapping
        self.encoders: Dict[str, Callable] = {
            "url": self.url_encode,
            "double_url": self.double_url_encode,
            "base64": self.base64_encode,
            "html": self.html_encode,
            "unicode": self.unicode_encode,
            "hex": self.hex_encode,
            "rot13": self.rot13_encode,
            "ascii": self.ascii_encode,
            "utf8": self.utf8_encode,
            "utf16": self.utf16_encode,
            "json": self.json_encode,
            "xml": self.xml_encode
        }
    
    def encode(self, payload: str, encoding_type: str) -> str:
        """Encode payload using specified encoding type"""
        
        if encoding_type not in self.encoders:
            self.logger.error(f"Unknown encoding type: {encoding_type}")
            return payload
        
        try:
            encoded = self.encoders[encoding_type](payload)
            self.logger.debug(f"Encoded payload using {encoding_type}")
            return encoded
        except Exception as e:
            self.logger.error(f"Encoding failed: {e}")
            return payload
    
    def url_encode(self, payload: str) -> str:
        """URL encode payload"""
        return urllib.parse.quote(payload, safe='')
    
    def double_url_encode(self, payload: str) -> str:
        """Double URL encode payload"""
        return urllib.parse.quote(urllib.parse.quote(payload, safe=''), safe='')
    
    def base64_encode(self, payload: str) -> str:
        """Base64 encode payload"""
        return base64.b64encode(payload.encode('utf-8')).decode('ascii')
    
    def html_encode(self, payload: str) -> str:
        """HTML entity encode payload"""
        return html.escape(payload)
    
    def unicode_encode(self, payload: str) -> str:
        """Unicode encode payload (\\uXXXX format)"""
        return ''.join(f'\\u{ord(char):04x}' for char in payload)
    
    def hex_encode(self, payload: str) -> str:
        """Hex encode payload"""
        return payload.encode('utf-8').hex()
    
    def rot13_encode(self, payload: str) -> str:
        """ROT13 encode payload"""
        return codecs.encode(payload, 'rot13')
    
    def ascii_encode(self, payload: str) -> str:
        """ASCII encode payload (decimal format)"""
        return ''.join(f'&#{ord(char)};' for char in payload)
    
    def utf8_encode(self, payload: str) -> str:
        """UTF-8 percent encoding"""
        return ''.join(f'%{byte:02X}' for byte in payload.encode('utf-8'))
    
    def utf16_encode(self, payload: str) -> str:
        """UTF-16 encoding"""
        return payload.encode('utf-16').hex()
    
    def json_encode(self, payload: str) -> str:
        """JSON encode payload (escape quotes and backslashes)"""
        return payload.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    
    def xml_encode(self, payload: str) -> str:
        """XML encode payload"""
        xml_chars = {
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            '"': '&quot;',
            "'": '&apos;'
        }
        
        result = payload
        for char, encoded in xml_chars.items():
            result = result.replace(char, encoded)
        return result
    
    def mixed_case_encode(self, payload: str) -> str:
        """Mixed case encoding for evasion"""
        result = ""
        for i, char in enumerate(payload):
            if char.isalpha():
                if i % 2 == 0:
                    result += char.upper()
                else:
                    result += char.lower()
            else:
                result += char
        return result
    
    def comment_encode(self, payload: str) -> str:
        """Insert comments for evasion"""
        # Insert /**/ comments in various places
        result = payload
        result = result.replace("script", "scr/**/ipt")
        result = result.replace("alert", "ale/**/rt")
        result = result.replace("SELECT", "SEL/**/ECT")
        result = result.replace("UNION", "UN/**/ION")
        return result
    
    def concatenation_encode(self, payload: str) -> str:
        """String concatenation for evasion"""
        if "alert" in payload.lower():
            return payload.replace("alert", "ale"+"rt")
        elif "script" in payload.lower():
            return payload.replace("script", "scri"+"pt")
        return payload
    
    def get_available_encodings(self) -> list:
        """Get list of available encoding types"""
        return list(self.encoders.keys())
    
    def multi_encode(self, payload: str, encodings: list) -> str:
        """Apply multiple encodings in sequence"""
        result = payload
        for encoding in encodings:
            result = self.encode(result, encoding)
        return result
    
    def bypass_waf_encode(self, payload: str, waf_type: str = "generic") -> str:
        """Encode payload to bypass WAF filters"""
        
        waf_bypasses = {
            "generic": [
                self.mixed_case_encode,
                self.comment_encode,
                self.concatenation_encode
            ],
            "cloudflare": [
                self.unicode_encode,
                self.double_url_encode
            ],
            "aws": [
                self.utf16_encode,
                self.comment_encode
            ],
            "akamai": [
                self.mixed_case_encode,
                self.utf8_encode
            ]
        }
        
        bypasses = waf_bypasses.get(waf_type, waf_bypasses["generic"])
        
        result = payload
        for bypass_func in bypasses:
            try:
                result = bypass_func(result)
            except:
                continue
        
        return result