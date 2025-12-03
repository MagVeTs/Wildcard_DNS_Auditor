# Wildcard DNS Auditor

A lightweight Python utility designed to detect DNS Wildcard configurations on a target domain and its subdomains.

This tool is particularly useful for SecOps, Penetration Testers, and Bug Bounty hunters who need to identify wildcard records (e.g., `*.dev.example.com`) to filter out false positives during subdomain enumeration.

## Security Implications of Wildcard DNS

Using Wildcard DNS (*.example.com) is generally considered insecure by design in modern infrastructure. While it offers convenience for developers, it introduces significant risks that often outweigh the benefits.

1. **Phishing & Social Engineering**
Wildcard DNS allows any subdomain to resolve. Attackers can abuse this to create convincing phishing URLs that appear to be hosted on your legitimate domain.

Example: If you have a wildcard for `*.example.com`, an attacker can send a victim to `secure-password-reset.example.com`. Because the DNS resolves, the victim may see a valid domain (increasing the likelihood they will trust the page) - if the server at that IP serves a default page or can be manipulated.

2. **Cookie Scoping & "Cookie Tossing"**
If an application sets session cookies with a loose scope (e.g., `domain=.example.com`), those cookies are sent to all subdomains.

The Risk: If an attacker compromises any specific subdomain (or finds a way to host content on one, such as via a forgotten dev box), they can receive sensitive session cookies for your main application. Wildcard DNS expands the attack surface for this by ensuring every possible subdomain is a valid destination.

3. **Hidden "Shadow IT" & Asset Inventory**
You cannot protect what you cannot see. Wildcard DNS creates a "fog of war" for security teams.

The Risk: It becomes nearly impossible to distinguish between a legitimate, active service and a non-existent one during external scans. This allows forgotten, unpatched development servers to hide in plain sight because they look just like empty wildcard responses to a scanner.

4. **Subdomain Takeover Complexity**
While Wildcard A records themselves don't always cause Subdomain Takeovers, they often mask them.

The Risk: If you use a wildcard CNAME pointing to a third-party service (e.g., `*.herokuapp.com`), an attacker can claim any unused subdomain on that service and instantly have it served under your trusted domain. The wildcard makes detection of these dangling pointers significantly harder.

## Features

- **Parent Domain Check**: Automatically checks the root domain (e.g., `example.com`) for wildcards.

- **Nested Subdomain Support**: Accepts a list of subdomains to check for nested wildcards (e.g., `*.staging.example.com`).

- **False Positive Avoidance**: Uses random nonces (e.g., `wildcard-test-a1b2c3d4.example.com`) to ensure results are accurate and not cached.

## Reporting:

- **Live Console Output**: See results in real-time.

- **File Output**: Save results to a text file using the `-o` flag.

- **End-of-Run Summary**: Provides a statistical summary of all wildcards found.

## Prerequisites
- Python 3.x

- `dnspython` library

## Installation
Install the required dependency using `pip`:
```
Bash
pip install dnspython
```

## Usage

```
Bash
python wildcard_dns_auditor.py <DOMAIN> [SUBDOMAIN_LIST] [-o OUTPUT_FILE]
```

## Arguments

|Argument|Type|Description|
|:------|:------|:------|
|`Domain`|Required|The main target domain (e.g., `example.com`).|
|`SUBDOMAIN_LIST`|Optional|A `.txt` file containing a list of subdomains to check.|
|`-o`, `--output`|Optional|Path to a file to save the output results.|

## Examples

1. Basic check on a single domain: Checks if `*.example.com` exists.
```
Bash
python wildcard_dns_auditor.py example.com
```

2. Check a domain and a list of subdomains: Checks `*.example.com` and checks for wildcards on every subdomain listed in `example_subs.txt`.
```
Bash
python wildcard_dns_auditor.py example.com example_subs.txt
```

3. Check and save results to a file: Runs the check and saves the full log and summary to `example_results.txt`.
```
Bash
python wildcard_dns_auditor.py example.com example_subs.txt -o example_results.txt
```

## Example Output
```
Plaintext
--- Checking 5 domains/subdomains for Wildcards ---

[-] Probing target: wildcard-test-8x92m.example.com
    [OK] No wildcard.

[-] Probing target: wildcard-test-k291l.dev.example.com
    [!] WILDCARD DETECTED: *.dev.example.com
        --> Resolves to: 192.168.1.50

[-] Probing target: wildcard-test-m441a.api.example.com
    [OK] No wildcard.

----------------------------------------
SUMMARY REPORT
----------------------------------------
Total domains checked: 5
Wildcards detected:    1

List of domains with wildcards:
 - Wildcard: *.dev.example.com (192.168.1.50)
```

## How It Works

The script takes the base domain and any subdomains provided in the text file.

For each entry, it generates a unique, random hostname (e.g., `wildcard-test-[random_string].domain.com`).

It attempts to resolve this hostname.

If it resolves (A Record returned): A wildcard exists. The script flags it.

If it fails (NXDOMAIN): No wildcard exists.


## Disclaimer
This tool is for educational purposes and authorized security testing only. Always ensure you have permission to scan the domains you are targeting.

## Contributors
- [MagVeTs](https://github.com/MagVeTs)
- [KfirDu](https://github.com/KfirDu)




