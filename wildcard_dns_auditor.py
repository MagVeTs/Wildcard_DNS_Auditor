import sys
import random
import string
import argparse
import dns.resolver  # Requires: pip install dnspython

def log(message, file_handle=None):
    """
    Helper to print to console and optionally write to a file.
    """
    print(message)
    if file_handle:
        file_handle.write(message + "\n")

def check_wildcard(domain, file_handle=None):
    """
    Checks if a wildcard DNS record exists for the given domain.
    Returns: (bool, list_of_ips)
    """
    # Create a random nonce like 'wctest-8x92m'
    nonce = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    test_target = f"wildcard-test-{nonce}.{domain}"
    
    log(f"[-] Probing target: {test_target}", file_handle)
    
    try:
        resolver = dns.resolver.Resolver()
        resolver.lifetime = 3.0 
        
        answers = resolver.resolve(test_target, 'A')
        ips = [r.to_text() for r in answers]
        return True, ips
        
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return False, []
    except dns.resolver.LifetimeTimeout:
        log(f"    [!] Timeout resolving {test_target}", file_handle)
        return False, []
    except Exception as e:
        log(f"    [!] Error: {e}", file_handle)
        return False, []

def main():
    parser = argparse.ArgumentParser(description="Check for DNS wildcards on a domain and list of subdomains.")
    parser.add_argument("domain", help="The base domain (e.g., example.com)")
    parser.add_argument("subdomain_file", nargs='?', help="Text file containing list of subdomains")
    parser.add_argument("-o", "--output", help="File to write the output to", default=None)

    args = parser.parse_args()

    base_domain = args.domain
    subdomains = []
    
    # Always check the base domain first
    subdomains.append(base_domain)

    # If a file is provided, load those subdomains
    if args.subdomain_file:
        try:
            with open(args.subdomain_file, 'r') as f:
                for line in f:
                    clean_sub = line.strip()
                    if clean_sub:
                        subdomains.append(clean_sub)
        except FileNotFoundError:
            print(f"Error: Could not find file {args.subdomain_file}")
            sys.exit(1)

    # Open output file if specified
    out_file = None
    if args.output:
        try:
            out_file = open(args.output, 'w')
        except IOError as e:
            print(f"Error opening output file: {e}")
            sys.exit(1)

    log(f"--- Checking {len(subdomains)} domains/subdomains for Wildcards ---\n", out_file)

    wildcard_count = 0
    results_summary = []

    try:
        for domain in subdomains:
            has_wildcard, ips = check_wildcard(domain, out_file)
            
            if has_wildcard:
                wildcard_count += 1
                msg = f"    [!] WILDCARD DETECTED: *.{domain}\n        --> Resolves to: {', '.join(ips)}\n"
                log(msg, out_file)
                results_summary.append(f"Wildcard: *.{domain} ({', '.join(ips)})")
            else:
                log(f"    [OK] No wildcard.\n", out_file)
    
    finally:
        # Print Summary
        log("-" * 40, out_file)
        log("SUMMARY REPORT", out_file)
        log("-" * 40, out_file)
        log(f"Total domains checked: {len(subdomains)}", out_file)
        log(f"Wildcards detected:    {wildcard_count}", out_file)
        
        if wildcard_count > 0:
            log("\nList of domains with wildcards:", out_file)
            for res in results_summary:
                log(f" - {res}", out_file)
        else:
            log("\nNo wildcards detected.", out_file)

        if out_file:
            print(f"\n[+] Results saved to {args.output}")
            out_file.close()

if __name__ == "__main__":
    main()
