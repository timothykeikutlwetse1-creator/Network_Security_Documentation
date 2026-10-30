
from __future__ import annotations
import argparse
import sys
from datetime import date
from pathlib import Path

# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------

PROJECT_TITLE = "Basic Network Security Documentation"

OBJECTIVES = [
    "Identify common network security threats.",
    "Explain network security controls and their purposes.",
    "Promote secure network configuration and monitoring.",
    "Provide a checklist for reviewing basic network security practices.",
]

KEY_TOPICS = [
    "Firewalls", "Network segmentation", "Secure Wi-Fi", "Encryption",
    "Access control", "Software updates", "Intrusion detection",
    "Security monitoring", "VPNs", "Incident response notes",
]

# (name, description, example of how it appears)
THREATS = [
    ("Malware",
     "Malicious software such as viruses, worms, ransomware and spyware that "
     "damages systems, steals data or locks files for ransom.",
     "Spreads through email attachments, unsafe downloads or unpatched services."),
    ("Phishing and social engineering",
     "Deceiving people into revealing credentials or running malicious files.",
     "A fake 'password expired' email linking to a counterfeit login page."),
    ("Denial of Service (DoS / DDoS)",
     "Overwhelming a service or link so legitimate users cannot reach it.",
     "A flood of traffic that exhausts a web server's bandwidth or connections."),
    ("Man-in-the-Middle (MitM)",
     "An attacker secretly intercepts or alters traffic between two parties.",
     "Eavesdropping on unencrypted traffic over an open public Wi-Fi network."),
    ("Unauthorised access and weak credentials",
     "Gaining entry through default, reused or guessable passwords or "
     "excessive permissions.",
     "Logging in to a router with the factory-default administrator password."),
    ("Rogue access points",
     "Unapproved wireless devices connected to or imitating the network.",
     "An 'Office-WiFi' lookalike network that captures user logins."),
    ("Unpatched vulnerabilities",
     "Known software flaws left unfixed on servers, devices or firmware.",
     "An outdated VPN appliance with a publicly documented flaw."),
    ("Insider threats",
     "Misuse of access by employees or contractors, deliberate or accidental.",
     "A staff member copying sensitive files to a personal device."),
]

# (name, purpose, key practices)
CONTROLS = [
    ("Firewalls",
     "Filter traffic between networks according to defined rules, allowing "
     "only what is needed.",
     ["Use a default-deny policy: block everything, then allow what is required.",
      "Review and remove unused or overly broad rules on a regular schedule.",
      "Restrict administrative interfaces to trusted management addresses.",
      "Enable logging for denied traffic and rule changes.",
      "Use host-based firewalls on servers and workstations as well."]),
    ("Network segmentation",
     "Divide the network into zones so a compromise in one area cannot "
     "easily spread to others.",
     ["Separate guest, staff, server, and IoT/device networks (e.g. VLANs).",
      "Control traffic between segments with firewall rules.",
      "Keep management interfaces on a dedicated, restricted network.",
      "Place public-facing services in a DMZ."]),
    ("Virtual Private Networks (VPNs)",
     "Create an encrypted tunnel so remote users and sites can reach "
     "internal resources safely over untrusted networks.",
     ["Require multi-factor authentication for remote access.",
      "Use modern, supported protocols and strong cipher settings.",
      "Grant VPN users access only to what they need (least privilege).",
      "Keep VPN gateways patched and log all connections."]),
    ("Secure Wi-Fi",
     "Protect wireless access, which is easier to reach than a wired network.",
     ["Use WPA3 where supported, otherwise WPA2 with AES (never WEP/open).",
      "Use long, unique passphrases, or 802.1X for organisations.",
      "Disable WPS and change default administrator credentials.",
      "Provide a separate, isolated guest network.",
      "Periodically scan for unapproved access points."]),
    ("Encryption",
     "Keeps data unreadable to anyone who intercepts or steals it.",
     ["Use TLS (HTTPS) for web and application traffic.",
      "Replace insecure protocols (Telnet, FTP, HTTP) with SSH, SFTP, HTTPS.",
      "Encrypt sensitive data at rest, including laptops and backups.",
      "Manage certificates and keys carefully and renew before expiry."]),
    ("Access control",
     "Ensures only the right people and devices reach the right resources.",
     ["Apply least privilege and role-based access.",
      "Use unique accounts; avoid shared logins.",
      "Enable multi-factor authentication, especially for admin accounts.",
      "Remove accounts promptly when people leave or change roles.",
      "Review permissions on a regular schedule."]),
    ("Software updates and patching",
     "Fixes known vulnerabilities before attackers can use them.",
     ["Keep an inventory of devices and software versions.",
      "Apply security updates promptly, prioritising critical systems.",
      "Update router, switch and firewall firmware, not only computers.",
      "Retire unsupported systems or isolate them."]),
    ("Intrusion detection and prevention (IDS/IPS)",
     "IDS watches traffic or hosts for suspicious activity and alerts; IPS "
     "can also block it.",
     ["Place sensors at network boundaries and key internal segments.",
      "Keep detection signatures and rules up to date.",
      "Tune rules to reduce false positives so real alerts are not ignored.",
      "Send alerts to a monitored location with a clear owner."]),
    ("Security monitoring and logging",
     "Provides visibility so incidents are noticed early and can be "
     "investigated afterwards.",
     ["Collect logs from firewalls, servers, VPNs and authentication systems.",
      "Synchronise clocks (NTP) so events can be correlated.",
      "Store logs securely, with retention that meets policy needs.",
      "Define what 'normal' looks like and alert on meaningful deviations."]),
]

INCIDENT_RESPONSE = [
    ("Preparation", "Define roles, contacts, escalation paths and a basic "
                    "response plan before an incident happens."),
    ("Detection and analysis", "Confirm whether an event is a real incident, "
                               "record what was seen, and judge its scope and impact."),
    ("Containment", "Limit the spread, for example by isolating affected "
                    "devices or segments, while preserving evidence."),
    ("Eradication and recovery", "Remove the cause, restore systems from "
                                 "trusted sources, and monitor closely afterwards."),
    ("Lessons learned", "Document what happened, what worked, and which "
                        "controls or procedures need to improve."),
]

# Checklist: section -> items
CHECKLIST: dict[str, list[str]] = {
    "Firewalls": [
        "A firewall is deployed at the network perimeter.",
        "Default-deny rules are in place for inbound traffic.",
        "Firewall rules are reviewed at least periodically.",
        "Firewall administration is limited to trusted addresses and accounts.",
    ],
    "Network Segmentation": [
        "Guest devices are separated from internal systems.",
        "Servers, workstations and IoT devices are on separate segments.",
        "Traffic between segments is restricted by rules.",
    ],
    "VPN and Remote Access": [
        "Remote access uses a VPN or equivalent secure method.",
        "Multi-factor authentication is required for remote access.",
        "VPN access is limited to the resources users need.",
    ],
    "Secure Wi-Fi": [
        "WPA3 (or WPA2-AES) encryption is enabled.",
        "Default router and access point credentials have been changed.",
        "WPS is disabled.",
        "A separate guest Wi-Fi network is provided.",
    ],
    "Encryption": [
        "Sensitive web and application traffic uses TLS/HTTPS.",
        "Insecure protocols (Telnet, FTP) are disabled or replaced.",
        "Laptops and backups containing sensitive data are encrypted.",
    ],
    "Access Control": [
        "Each user has a unique account.",
        "Least privilege is applied to accounts and permissions.",
        "Multi-factor authentication is enabled for administrator accounts.",
        "Accounts of leavers are disabled promptly.",
        "Strong password rules or a password manager are encouraged.",
    ],
    "Updates and Patching": [
        "An inventory of network devices and software exists.",
        "Operating systems and applications receive regular updates.",
        "Network device firmware is kept up to date.",
        "Unsupported systems are replaced or isolated.",
    ],
    "Intrusion Detection and Monitoring": [
        "An IDS/IPS or equivalent monitoring is in place.",
        "Logs from key network and security devices are collected.",
        "Device clocks are synchronised.",
        "Alerts are reviewed by a named person or team.",
    ],
    "Backup and Incident Response": [
        "Regular backups are taken and at least one copy is kept offline or isolated.",
        "Backup restoration has been tested.",
        "An incident response plan with contacts exists.",
        "Users know how to report suspicious activity.",
    ],
}

SECURITY_NOTICE = (
    "This project is for educational purposes. Any network assessment or "
    "security testing must be authorised by the network owner. Do not "
    "publish passwords, private keys, confidential network diagrams or "
    "sensitive configuration details."
)

# --------------------------------------------------------------------------
# Markdown builders
# --------------------------------------------------------------------------


def build_readme() -> str:
    objectives = "\n".join(f"- {o}" for o in OBJECTIVES)
    topics = ", ".join(t.lower() for t in KEY_TOPICS[:-1]) + f" and {KEY_TOPICS[-1].lower()}"
    return f"""# {PROJECT_TITLE}

## Project Overview

This project provides basic network security documentation explaining common
network threats and the measures used to protect computer networks. It is
designed to help students and beginners understand how organisations maintain
secure and reliable networks.

## Project Objectives

{objectives}

## Project Contents

| File | Description |
|------|-------------|
| `network-security-guide.md` | Describes network threats and protective security controls. |
| `network-security-checklist.md` | Lists recommended practices for improving network security. |

## Intended Audience

Cybersecurity students, IT support personnel, network administrators and
beginners learning about network security.

## Key Topics

The project covers {topics}.

## How to Use This Project

1. Read the network security guide to understand the main concepts.
2. Use the checklist to review basic network security practices in an
   authorised learning environment.

## Security Notice

{SECURITY_NOTICE}

## Conclusion

Good network security combines technical controls, regular monitoring, secure
configuration and responsible user behaviour. This documentation provides a
starting point for understanding and applying these practices.
"""


def build_guide() -> str:
    lines: list[str] = [
        "# Network Security Guide",
        "",
        "## 1. Introduction",
        "",
        "Network security is the practice of protecting the confidentiality, "
        "integrity and availability of data and services as they move across "
        "a network. No single control is enough, so organisations use layered "
        "defences (\"defence in depth\") and monitor them continuously.",
        "",
        "## 2. Common Network Threats",
        "",
    ]
    for name, desc, example in THREATS:
        lines += [f"### {name}", "", desc, "", f"*Example:* {example}", ""]

    lines += ["## 3. Protective Security Controls", ""]
    for name, purpose, practices in CONTROLS:
        lines += [f"### {name}", "", f"**Purpose:** {purpose}", "", "**Best practices:**", ""]
        lines += [f"- {p}" for p in practices]
        lines.append("")

    lines += [
        "## 4. Illustrative Firewall Policy (conceptual)",
        "",
        "The table below shows the *idea* of a default-deny policy. It is a "
        "generic teaching example using placeholder zones, not a "
        "configuration to copy. Real rules depend on your own environment "
        "and must never be published with real addresses.",
        "",
        "| # | From | To | Service | Action |",
        "|---|------|----|---------|--------|",
        "| 1 | Staff network | Internet | Web (HTTPS), DNS | Allow |",
        "| 2 | Guest network | Internet | Web (HTTPS), DNS | Allow |",
        "| 3 | Guest network | Internal networks | Any | **Deny** |",
        "| 4 | Internet | Public web server (DMZ) | HTTPS | Allow |",
        "| 5 | Any | Any | Any | **Deny and log** |",
        "",
        "## 5. Incident Response Notes",
        "",
        "A simple response lifecycle helps teams act calmly and consistently.",
        "",
    ]
    for i, (phase, desc) in enumerate(INCIDENT_RESPONSE, start=1):
        lines.append(f"{i}. **{phase}:** {desc}")
    lines += [
        "",
        "## 6. Security Notice",
        "",
        SECURITY_NOTICE,
        "",
    ]
    return "\n".join(lines)


def build_checklist() -> str:
    lines = [
        "# Network Security Checklist",
        "",
        "Use this checklist to review basic network security practices in an "
        "authorised learning environment. Tick each item that is in place; "
        "unticked items are candidates for improvement.",
        "",
    ]
    for section, items in CHECKLIST.items():
        lines += [f"## {section}", ""]
        lines += [f"- [ ] {item}" for item in items]
        lines.append("")
    lines += ["---", "", f"*Notice:* {SECURITY_NOTICE}", ""]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# File generation
# --------------------------------------------------------------------------


def generate_docs(out_dir: Path, force: bool = False) -> list[Path]:
    """Write the three documentation files. Returns the paths written."""
    out_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "README.md": build_readme(),
        "network-security-guide.md": build_guide(),
        "network-security-checklist.md": build_checklist(),
    }
    written: list[Path] = []
    for name, content in files.items():
        path = out_dir / name
        if path.exists() and not force:
            print(f"  skipped (exists): {path}  [use --force to overwrite]")
            continue
        path.write_text(content, encoding="utf-8")
        print(f"  wrote: {path}")
        written.append(path)
    return written


# --------------------------------------------------------------------------
# Interactive checklist review
# --------------------------------------------------------------------------


def ask(question: str) -> str:
    """Prompt for y / n / na. Returns 'y', 'n' or 'na'."""
    while True:
        answer = input(f"  {question}\n    [y]es / [n]o / [na] not applicable: ").strip().lower()
        if answer in ("y", "yes"):
            return "y"
        if answer in ("n", "no"):
            return "n"
        if answer in ("na", "n/a"):
            return "na"
        print("    Please answer y, n or na.")


def run_review(out_dir: Path) -> None:
    print("\n" + "=" * 60)
    print(" Network Security Checklist Review")
    print("=" * 60)
    print(SECURITY_NOTICE)
    consent = input("\nIs this review of a network you own or are authorised "
                    "to assess? [y/N]: ").strip().lower()
    if consent not in ("y", "yes"):
        print("Review cancelled. Only review networks you are authorised to assess.")
        return

    results: dict[str, list[tuple[str, str]]] = {}
    for section, items in CHECKLIST.items():
        print(f"\n--- {section} ---")
        results[section] = [(item, ask(item)) for item in items]

    # Scoring (N/A items are excluded)
    total = sum(1 for items in results.values() for _, a in items if a != "na")
    passed = sum(1 for items in results.values() for _, a in items if a == "y")
    pct = round(100 * passed / total) if total else 0

    report = [
        "# Network Security Review Report",
        "",
        f"*Date:* {date.today().isoformat()}",
        "",
        f"**Score:** {passed} of {total} applicable items in place ({pct}%)",
        "",
    ]
    gaps: list[str] = []
    for section, items in results.items():
        report += [f"## {section}", ""]
        for item, answer in items:
            mark = {"y": "[x]", "n": "[ ]", "na": "[-]"}[answer]
            report.append(f"- {mark} {item}")
            if answer == "n":
                gaps.append(f"{section}: {item}")
        report.append("")
    report += ["## Suggested Improvements", ""]
    report += [f"- {g}" for g in gaps] if gaps else ["- No gaps identified in this review."]
    report += ["", "*Legend: [x] in place, [ ] needs attention, [-] not applicable*", ""]

    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"review-report-{date.today().isoformat()}.md"
    report_path.write_text("\n".join(report), encoding="utf-8")

    print("\n" + "=" * 60)
    print(f" Score: {passed}/{total} ({pct}%)")
    print(f" Items needing attention: {len(gaps)}")
    print(f" Report saved to: {report_path}")
    print("=" * 60)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate basic network security documentation and run "
                    "an optional interactive checklist review.",
    )
    parser.add_argument("-o", "--output-dir", type=Path,
                        default=Path("network-security-docs"),
                        help="Folder for generated files (default: network-security-docs)")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Overwrite existing files")
    parser.add_argument("--review", action="store_true",
                        help="Run the interactive checklist review instead of "
                             "generating documents")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.review:
            run_review(args.output_dir)
        else:
            print(f"Generating '{PROJECT_TITLE}' in {args.output_dir}/")
            generate_docs(args.output_dir, force=args.force)
            print("\nDone. Remember: " + SECURITY_NOTICE)
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130
    except OSError as exc:
        print(f"File error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())