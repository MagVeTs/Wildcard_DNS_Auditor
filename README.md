# Wildcard DNS Auditor

A lightweight Python utility designed to detect DNS Wildcard configurations on a target domain and its subdomains.

This tool is particularly useful for SecOps, Penetration Testers, and Bug Bounty hunters who need to identify wildcard records (e.g., *.dev.example.com) to filter out false positives during subdomain enumeration.

Using Wildcard DNS is not best practice from a security perpsective


## Features

- **Parent Domain Check**: Automatically checks the root domain (e.g., example.com) for wildcards.

- **Nested Subdomain Support**: Accepts a list of subdomains to check for nested wildcards (e.g., *.staging.example.com).

- **False Positive Avoidance**: Uses random nonces (e.g., wildcard-test-a1b2c3d4.target.com) to ensure results are accurate and not cached.

## Reporting:

- **Live Console Output**: See results in real-time.

- **File Output**: Save results to a text file using the -o flag.

- **End-of-Run Summary**: Provides a statistical summary of all wildcards found.

## Prerequisites
- Python 3.x

- `dnspython` library

## Installation
Install the required dependency using pip:
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

2. Check a domain and a list of subdomains: Checks `*.example.com` and checks for wildcards on every subdomain listed in `subs.txt`.
```
Bash
python wildcard_dns_auditor.py example.com subs.txt
```

3. Check and save results to a file: Runs the check and saves the full log and summary to `example_results.txt`.
```
Bash
python wildcard_dns_auditor.py example.com subs.txt -o example_results.txt
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




