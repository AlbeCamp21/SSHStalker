import paramiko
import argparse
import time
import sys

# ANSI Color Codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GRAY = "\033[90m"
RESET = "\033[0m"

# List of remote enumeration commands
commands = [
    "id",
    "uname -a",
    "sudo -l",
    "ls -laR /home",
    "cat /etc/passwd",
    "find / -perm -4000 2>/dev/null",
    "getcap -r / 2>/dev/null",
    "ps aux"
]

def print_header(text):
    print(f"\n{MAGENTA}{'=' * 55}\n{text}\n{'=' * 55}{RESET}")

def print_banner(cmd):
    print(f"\t{CYAN}[+] Running command: {cmd}{RESET}")

def run_remote_enum(ip, username, password):
    print_header(r"""
   _____ _____ _    _  _____ _        _ _             
  / ____/ ____| |  | |/ ____| |      | | |            
 | (___| (___ | |__| | (___ | |_ __ _| | | _____ _ __ 
  \___ \\___ \|  __  |\___ \| __/ _` | | |/ / _ \ '__|
  ____) |___) | |  | |____) | || (_| | |   <  __/ |   
 |_____/_____/|_|  |_|_____/ \__\__,_|_|_|\_\___|_|   
                Created by: @AlbeCamp
                 """)

    print(f"\n{YELLOW}[+] Connecting to {ip} as {username}:{password}...{RESET}")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, username=username, password=password)
        print(f"\n\t{GREEN}[+] SSH connection successful{RESET}\n")
    except Exception as e:
        print(f"\n\t{RED}[!] SSH connection failed: {e}{RESET}")
        return

    try:
        for cmd in commands:
            print_banner(cmd)

            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(0.2)

            out = stdout.read().decode()
            err = stderr.read().decode()

            # Filter passwd
            if cmd == "cat /etc/passwd":
                filtered = []
                for line in out.splitlines():
                    if any(shell in line for shell in ["/bin/bash", "/bin/sh", "/bin/zsh", "/bin/dash"]):
                        filtered.append(line)
                out = "\n".join(filtered)

            # Filter ls -la /home
            if cmd == "ls -laR /home":
                filtered = []
                for line in out.splitlines():
                    name = line.split()[-1] if line.split() else ""
                    if name not in [".", ".."]:
                        filtered.append(line)
                out = "\n".join(filtered)

            # Filter SUID binaries
            if cmd.startswith("find / -perm -4000"):
                filtered = [line for line in out.splitlines() if line.startswith("/usr/bin/")]
                out = "\n".join(filtered)

            # Filter sudo -l
            if cmd == "sudo -l":
                lines = out.splitlines()
                start = None
                for i, line in enumerate(lines):
                    if "may run the following commands" in line:
                        start = i
                        break
                if start is not None:
                    out = "\n".join(lines[start:])
                else:
                    out = ""

            if out.strip():
                for line in out.splitlines():
                    print(f"\t\t{GRAY}{line}{RESET}")

            if err.strip():
                for line in err.splitlines():
                    print(f"\t\t{RED}{line}{RESET}")

    except KeyboardInterrupt:
        print(f"\n{RED}[!] Canceling...{RESET}")
        ssh.close()
        sys.exit(1)

    ssh.close()
    print(f"\n\t{GREEN}[+] Enumeration completed for {username}{RESET}\n")


def main():
    parser = argparse.ArgumentParser(
        description="SSH enumeration tool for authorized lab environments."
    )

    parser.add_argument("-u", "--user", required=True, help="SSH username")
    parser.add_argument("-p", "--password", required=True, help="SSH password")
    parser.add_argument("-i", "--ip", required=True, help="Target IP address")

    args = parser.parse_args()

    try:
        run_remote_enum(args.ip, args.user, args.password)
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Canceling...{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()