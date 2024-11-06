import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import subprocess
import threading
import os
import time

# Fonction pour afficher la console dédiée pour chaque outil
def open_console_window(tool_name):
    console_window = Toplevel(window)
    console_window.title(f"{tool_name} Console")
    console_window.geometry("600x400")

    console_output = tk.Text(console_window, height=15, width=80, wrap=tk.WORD)
    console_output.pack(padx=10, pady=10)

    console_output.insert(tk.END, f"Launching {tool_name}...\n")
    console_output.yview(tk.END)

    return console_output


# Fonction pour exécuter les commandes en arrière-plan et afficher les résultats dans la console dédiée
def run_command(command, console_output):
    try:
        # Exécution de la commande
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Lire la sortie de la commande ligne par ligne
        for stdout_line in iter(process.stdout.readline, ""):
            console_output.insert(tk.END, stdout_line)
            console_output.yview(tk.END)
            console_output.update_idletasks()

        # Lire les erreurs de la commande ligne par ligne
        for stderr_line in iter(process.stderr.readline, ""):
            console_output.insert(tk.END, stderr_line)
            console_output.yview(tk.END)
            console_output.update_idletasks()

        process.stdout.close()
        process.stderr.close()
        process.wait()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Fonction pour gérer le choix de l'outil SSTI et vérifier le fichier
def run_ssti_scanner(target):
    # Demander à l'utilisateur de spécifier le chemin du fichier ssti-scanner.py
    file_path = filedialog.askopenfilename(title="Select SSTI Scanner Script", filetypes=[("Python files", "*.py")])

    if not file_path:
        messagebox.showerror("Error", "No file selected for SSTI Scanner.")
        return

    # Vérifier si le fichier existe
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", f"File {file_path} does not exist.")
        return

    # Construire la commande avec le chemin complet
    command = ["python3", file_path, target]

    # Ouvrir une fenêtre de console pour afficher les résultats de la commande
    console_output = open_console_window("SSTI Scanner")

    # Exécuter la commande dans un thread pour ne pas bloquer l'interface
    threading.Thread(target=run_command, args=(command, console_output), daemon=True).start()


# Fonction pour exécuter chaque outil selon le choix de l'utilisateur
def execute_choice(choice):
    target = entry_target.get()
    if not target:
        messagebox.showerror("Error", "Please enter a target (IP/URL/Domain).")
        return

    if choice == 1:
        tool_name = "Nmap"
        command = ["nmap", "-A", target]
    elif choice == 2:
        tool_name = "Nikto"
        command = ["nikto", "-h", target]
    elif choice == 3:
        tool_name = "Whois"
        command = ["whois", target]
    elif choice == 4:
        tool_name = "Dig"
        command = ["dig", target, "+short"]
    elif choice == 5:
        tool_name = "SMTP User Enum"
        command = ["smtp-user-enum", "-M", "VRFY", "-U", "/path/to/userlist.txt", "-t", target]
    elif choice == 6:
        tool_name = "Nmap Deep Scan"
        command = ["nmap", "-sS", "-sV", "-O", "--top-ports", "1000", target]
    elif choice == 7:
        tool_name = "OpenVAS"
        command = ["openvas", "-T", "html", "-i", target, "-o", "report.html"]
    elif choice == 8:
        tool_name = "Sublist3r"
        command = ["sublist3r", "-d", target]
    elif choice == 9:
        tool_name = "Curl Security Headers"
        command = ["curl", "-s", "-D-", target, "|", "grep", "-E", "Content-Security-Policy|X-Frame-Options|X-Content-Type-Options|Strict-Transport-Security|Referrer-Policy|Permissions-Policy|Expect-CT|Feature-Policy"]
    elif choice == 10:
        tool_name = "Nmap Service & Version Detection"
        command = ["nmap", "-sV", "--script=banner,http-title,http-headers,ssl-cert", target]
    elif choice == 11:
        tool_name = "SSLScan"
        command = ["sslscan", target]
    elif choice == 12:
        tool_name = "WhatWeb"
        command = ["whatweb", target]
    elif choice == 13:
        tool_name = "ZAP XSS Scan"
        command = ["zap-cli", "quick-scan", "-s", "xss", "--self-contained", target]
    elif choice == 14:
        tool_name = "SQLMap"
        command = ["sqlmap", "-u", target, "--batch", "--level=5", "--risk=3"]
    elif choice == 15:
        tool_name = "Nikto LFI/RFI Check"
        command = ["nikto", "-h", target, "-Plugins", "lfi,rfi"]
    elif choice == 16:
        tool_name = "Commix"
        command = ["commix", "-u", target]
    elif choice == 17:
        run_ssti_scanner(target)
        return
    elif choice == 18:
        tool_name = "ZAP CSRF Scan"
        command = ["zap-cli", "quick-scan", "-s", "csrf", "--self-contained", target]
    elif choice == 19:
        credits()
        return
    elif choice == 20:
        window.quit()
        return
    else:
        messagebox.showerror("Error", "Invalid option")
        return

    # Ouvrir une fenêtre de console pour afficher les résultats de la commande
    console_output = open_console_window(tool_name)

    # Exécuter la commande dans un thread pour ne pas bloquer l'interface
    threading.Thread(target=run_command, args=(command, console_output), daemon=True).start()


# Fonction pour afficher les crédits
def credits():
    credits_text = """
    RedMoon Security Tool
    Developed by: Mlock
    Description: A powerful tool designed to provide comprehensive
    security scans, from host and vulnerability detection to
    advanced injection testing, ensuring all angles of security
    testing are covered. Please use responsibly.
    """

    github_link = "GitHub: https://github.com/Mlock-RedMoon"

    def type_writer_animation(text, delay=0.05):
        for char in text:
            credits_output.insert(tk.END, char)
            credits_output.yview(tk.END)
            window.update_idletasks()
            time.sleep(delay)

    type_writer_animation(credits_text)
    time.sleep(0.5)
    type_writer_animation(github_link)
    credits_output.insert(tk.END, "\nThank you for using RedMoon!")


# Fonction pour afficher l'interface graphique
def create_interface():
    global window, entry_target, credits_output

    window = tk.Tk()
    window.title("RedMoon Security Tool")

    # Titre stylisé
    title_label = tk.Label(window, text="RedMoon", font=("Helvetica", 24, "bold"), fg="green")
    title_label.pack(pady=20)

    # Champ de saisie pour l'IP ou URL
    target_label = tk.Label(window, text="Enter Target (IP/URL/Domain):")
    target_label.pack(pady=5)
    entry_target = tk.Entry(window, width=50)
    entry_target.pack(pady=10)

    # Liste des options du menu
    buttons_frame = tk.Frame(window)
    buttons_frame.pack(pady=20)

    options = [
        ("Host Scan (nmap)", 1),
        ("Web Vulnerability Scan (nikto)", 2),
        ("Domain Information (whois)", 3),
        ("DNS Resolution (dig)", 4),
        ("SMTP Users Enumeration", 5),
        ("Deep Port & Service Scan (nmap)", 6),
        ("Specific Vulnerability Scan (OpenVAS)", 7),
        ("Subdomain Analysis (sublist3r)", 8),
        ("Security Header Testing (curl)", 9),
        ("Service & Version Detection", 10),
        ("Advanced SSL Certificate Check", 11),
        ("Website Technology Audit", 12),
        ("XSS Scan (ZAP)", 13),
        ("SQL Injection Detection", 14),
        ("LFI/RFI Scan", 15),
        ("Command Injection Test (commix)", 16),
        ("SSTI Vulnerability Scan", 17),
        ("CSRF Scan (ZAP)", 18),
        ("Credits", 19),
        ("Quit", 20)
    ]

    for (text, val) in options:
        button = tk.Button(buttons_frame, text=text, width=25, command=lambda choice=val: execute_choice(choice))
        button.grid(row=(options.index((text, val))) // 2, column=(options.index((text, val))) % 2, padx=5, pady=5)

    window.mainloop()


if __name__ == "__main__":
    create_interface()
