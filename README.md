

# DDoS Test Tool (Educational Use Only) ⚠️

**⚠️ WARNING: This tool is for authorized security testing and educational purposes ONLY. Unauthorized use is illegal and unethical.**

---

## **About**
A Python-based DDoS simulation tool designed to help security professionals and students understand traffic patterns and mitigation techniques. Features include:

- ✅ **SSL/TLS Support** for HTTPS targets  
- ✅ **Asynchronous Concurrency** (high-performance via `asyncio`)  
- ✅ **Proxy Rotation** (HTTP/SOCKS5 support)  
- ✅ **Randomized Requests** (headers, methods, payloads)  
- ✅ **Safety Controls** (confirmation prompts, graceful shutdown)  

---

## **Features**
| Capability          | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| **HTTP/HTTPS Support** | Targets ports 80 (HTTP) and 443 (HTTPS) with SNI handling.                 |
| **Async I/O**        | Uses `asyncio` for thousands of concurrent requests.                       |
| **Proxy Rotation**   | Rotates through a list of proxies to distribute traffic origin.            |
| **Evasion Techniques** | Randomizes User-Agents, methods (GET/POST/HEAD/OPTIONS), and POST payloads. |
| **Safety Checks**    | Mandatory confirmation prompt before starting the attack.                  |

---

## **Installation**
1. **Python 3.8+** required  
2. Install dependencies:  
   ```bash
   pip install aiohttp pysocks
   ```

---

## **Usage**
```bash
python3 ddos_test.py <target> [--port PORT] [--threads THREADS] [--proxy-file PROXIES.TXT]
```

### **Example Commands**
```bash
# Test HTTP server on port 80 with 200 threads
python3 ddos_test.py example.com --port 80 --threads 200

# Test HTTPS server with proxies
python3 ddos_test.py example.com --port 443 --proxy-file proxies.txt
```

---

## **Proxy File Format**
Create a `proxies.txt` file with one proxy per line:  
```
HTTP:127.0.0.1:8080
SOCKS5:192.168.1.100:1080
```

---

## **Ethical Guidelines**
1. **Authorization Required**  
   - Only test systems you **own** or have **written permission** to attack.  
2. **Isolation**  
   - Use lab environments (e.g., VMs, cloud instances) to avoid unintended impact.  
3. **Transparency**  
   - Share results **only** with authorized parties.  

---

## **Development Notes**
- **Testing Environment:**  
  Use tools like `Wireshark` or `tcpdump` to monitor traffic.  
- **Mitigation Practice:**  
  Pair this tool with firewall rules (e.g., `iptables`) or rate-limiting configurations to learn defense strategies.  

---

## **License**
MIT License (for educational use only). **You are responsible for ensuring compliance with all laws and ethical standards.**  

---

**⚠️ Final Reminder: Misuse of this tool can cause harm and legal consequences. Always obtain explicit authorization before testing any system.**
