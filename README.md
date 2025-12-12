```
   _____ _____ _    _  _____ _        _ _             
  / ____/ ____| |  | |/ ____| |      | | |            
 | (___| (___ | |__| | (___ | |_ __ _| | | _____ _ __ 
  \___ \\___ \|  __  |\___ \| __/ _` | | |/ / _ \ '__|
  ____) |___) | |  | |____) | || (_| | |   <  __/ |   
 |_____/_____/|_|  |_|_____/ \__\__,_|_|_|\_\___|_|   
```

SSHStalker is a lightweight SSH-based enumeration tool designed for **authorized cybersecurity labs**, **CTFs**, and **safe practice environments** where the attacker already has valid credentials and wants to analyze privilege-escalation opportunities.

> **Legal Warning:**  
> SSHStalker must only be used in environments where you have explicit authorization.  
> Unauthorized system access is illegal.

## Features

- **Automated Post-Login Enumeration**
  - Runs a curated set of commands for privilege escalation discovery.
  - Filters unnecessary noise such as:
    - `.` and `..` directories  
    - Non-login users from `/etc/passwd`
    - Non-useful SUID findings (focus on `/usr/bin`)

## Installation

### Requirements
- Python 3.8+
- Paramiko (`pip install paramiko`)

### Clone the Repository

```bash
git clone https://github.com/<your-username>/SSHStalker.git
cd SSHStalker
```

## Usage

```
python3 sshstalker.py -u <username> -p <password> -i <target_ip>
```

### Arguments

| Flag | Description |
| --- | --- |
| `-u`, `--user` | SSH username |
| `-p`, `--password` | SSH password |
| `-i`, `--ip` | Target IP address |

## Enumeration Commands Executed

SSHStalker currently runs:

- `id` – user/group identity

- `uname -a` – system information
- `sudo -l` – sudo privileges
- `ls -laR /home` – recursive home directory listing
- `cat /etc/passwd` – only users with login shells
- `find / -perm -4000 2>/dev/null` – filtered SUID binaries
- `getcap -r / 2>/dev/null` – Linux capabilities
- `ps aux` – running processes