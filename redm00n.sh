#!/bin/bash

# Import Colorama colors for Python
python3 -c "from colorama import Fore, Style; print(Fore.GREEN + ' ' + Style.RESET_ALL)" &> /dev/null || {
    echo "Colorama is not installed. Install it using 'pip install colorama'."
    exit 1
}

# ASCII header using figlet
figlet -c "RedMoon"

# Function to show the main menu
show_menu() {
    echo -e "\033[32m=== RedMoon Tool Menu ===\033[0m"
    echo -e "\033[36m1) Host Scan (nmap)"
    echo -e "2) Web Vulnerability Scan (nikto)"
    echo -e "3) Domain Information (whois)"
    echo -e "4) DNS Resolution (dig)"
    echo -e "5) SMTP Users Enumeration (smtp-user-enum)"
    echo -e "6) Deep Port & Service Scan (nmap)"
    echo -e "7) Specific Vulnerability Scan (OpenVAS)"
    echo -e "8) Subdomain Analysis (sublist3r)"
    echo -e "9) Security Header Testing (curl)"
    echo -e "10) Service & Version Detection (nmap + scripts)"
    echo -e "11) Advanced SSL Certificate Check (sslscan)"
    echo -e "12) Website Technology Audit (whatweb)"
    echo -e "13) XSS Vulnerability Scan (OWASP ZAP)"
    echo -e "14) SQL Injection Detection (sqlmap)"
    echo -e "15) LFI/RFI Vulnerability Check"
    echo -e "16) Command Injection Security Test (commix)"
    echo -e "17) SSTI Vulnerability Detection"
    echo -e "18) CSRF Vulnerability Testing (OWASP ZAP)"
    echo -e "19) Credits\033[0m"
    echo -e "\033[31m20) Quit\033[0m"
    echo -e "\033[32m===========================\033[0m"
}

# Function to display credits with animated typing effect
credits() {
    python3 - << 'EOF'
import sys
import time
from colorama import Fore, Style

credits_text = """
RedMoon Security Tool
Developed by: Mlock
Description: A powerful tool designed to provide comprehensive
security scans, from host and vulnerability detection to
advanced injection testing, ensuring all angles of security
testing are covered. Please use responsibly.
"""

figlet_text = "\033[31m" + "\n".join([
    "      ___           ___          _____          ___           ___     ",
    "     /  /\         /  /\        /  /::\        /__/\         /__/\    ",
    "    /  /::\       /  /:/_      /  /:/\:\      |  |::\        \  \:\   ",
    "   /  /:/\:\     /  /:/ /\    /  /:/  \:\     |  |:|:\        \  \:\  ",
    "  /  /:/~/:/    /  /:/ /:/_  /__/:/ \__\:|  __|__|:|\:\   _____\__\:\ ",
    " /__/:/ /:/___ /__/:/ /:/ /\ \  \:\ /  /:/ /__/::::| \:\ /__/::::::::\\",
    " \  \:\/:::::/ \  \:\/:/ /:/  \  \:\  /:/  \  \:\~~\__\/ \  \:\~~\~~\/ ",
    "  \  \::/~~~~   \  \::/ /:/    \  \:\/:/    \  \:\        \  \:\  ~~~  ",
    "   \  \:\        \  \:\/:/      \  \::/      \  \:\        \  \:\      ",
    "    \  \:\        \  \::/        \__\/        \  \:\        \  \:\     ",
    "     \__\/         \__\/                       \__\/         \__\/    "
]) + "\033[0m\n"

print(figlet_text)
time.sleep(0.5)

for char in credits_text:
    sys.stdout.write(Fore.CYAN + char + Style.RESET_ALL)
    sys.stdout.flush()
    time.sleep(0.05)
print("\n" + Fore.GREEN + "Thank you for using RedMoon!" + Style.RESET_ALL)
EOF
}

# Function to execute the user's choice
execute_choice() {
    case $1 in
        1) 
            read -p "Enter IP or URL to scan with nmap: " target
            nmap -A "$target"
            ;;
        2) 
            read -p "Enter the URL to scan with nikto: " target
            nikto -h "$target"
            ;;
        3) 
            read -p "Enter domain for information (whois): " domain
            whois "$domain"
            ;;
        4) 
            read -p "Enter domain for DNS resolution (dig): " domain
            dig "$domain" +short
            ;;
        5) 
            read -p "Enter SMTP server for user enumeration: " smtp_server
            smtp-user-enum -M VRFY -U /path/to/userlist.txt -t "$smtp_server"
            ;;
        6)
            read -p "Enter IP or URL for deep port and service scan: " target
            nmap -sS -sV -O --top-ports 1000 "$target"
            ;;
        7)
            read -p "Enter IP or URL for specific vulnerability scan with OpenVAS: " target
            echo "Launching OpenVAS (requires configuration)..."
            openvas -T html -i "$target" -o report.html
            ;;
        8)
            read -p "Enter domain for subdomain analysis: " domain
            sublist3r -d "$domain"
            ;;
        9)
            read -p "Enter URL for security header testing: " url
            curl -s -D- "$url" | grep -E "Content-Security-Policy|X-Frame-Options|X-Content-Type-Options|Strict-Transport-Security|Referrer-Policy|Permissions-Policy|Expect-CT|Feature-Policy"
            ;;
        10)
            read -p "Enter IP or URL to check service versions and configurations: " target
            nmap -sV --script=banner,http-title,http-headers,ssl-cert "$target"
            ;;
        11)
            read -p "Enter URL or IP for SSL certificate verification: " target
            sslscan "$target"
            ;;
        12)
            read -p "Enter URL for website technology audit: " target
            whatweb "$target"
            ;;
        13)
            read -p "Enter URL for XSS vulnerability scan: " url
            zap-cli quick-scan -s xss --self-contained "$url"
            ;;
        14)
            read -p "Enter URL for SQL injection detection: " url
            sqlmap -u "$url" --batch --level=5 --risk=3
            ;;
        15)
            read -p "Enter URL for LFI/RFI vulnerability check: " url
            nikto -h "$url" -Plugins lfi,rfi
            ;;
        16)
            read -p "Enter URL for command injection testing: " url
            commix -u "$url"
            ;;
        17)
            read -p "Enter URL for SSTI vulnerability detection: " url
            python3 ssti-scanner.py "$url"
            ;;
        18)
            read -p "Enter URL for CSRF vulnerability testing: " url
            zap-cli quick-scan -s csrf --self-contained "$url"
            ;;
        19)
            credits
            ;;
        20)
            echo "Thank you for using RedMoon. Goodbye!"
            exit 0
            ;;
        *) 
            echo -e "\033[31mInvalid option, please try again.\033[0m"
            ;;
    esac
}

# Main loop
while true; do
    show_menu
    read -p "Choose an option: " choice
    execute_choice "$choice"
    echo ""
done
