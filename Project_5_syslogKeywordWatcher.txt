syslog keyword watcher 

Monitor /var/log/syslog or /var/log/auth.log in real time

Alert/log if specific keywords appear, like:
- Failed password
- Invalid user
- sudo
- segfault

nano syslog_keyword_watcher.sh

#!/bin/bash

# === CONFIG ===
LOGFILE="/var/log/syslog"                      # or /var/log/auth.log
KEYWORDS=("Failed password" "Invalid user" "segfault" "sudo")
ALERT_LOG="$HOME/Desktop/syslog_alerts.log"

# === START ===
echo "[+] Starting Syslog Keyword Watcher..."
echo "[+] Monitoring $LOGFILE"
echo "[+] Alert log: $ALERT_LOG"
echo

# === MONITOR ===
tail -Fn0 "$LOGFILE" | while read line; do
    for keyword in "${KEYWORDS[@]}"; do
        if echo "$line" | grep -q "$keyword"; then
            TIMESTAMP=$(date)
            ALERT="[!] $TIMESTAMP - Match: '$keyword' -> $line"
            echo "$ALERT"
            echo "$ALERT" >> "$ALERT_LOG"
        fi
    done
done


terminal: 

chmod +x ~/Desktop/syslog_keyword_watcher.sh

sudo ~/Desktop/syslog_keyword_watcher.sh

Terminal output: 
[!] Mon May 20 14:30:55 - Match: 'Failed password' -> May 20 14:30:55 ip-10-0-0-1 sshd[12345]: Failed password for invalid user admin from 192.168.1.100 port 54321 ssh2

Logs will be also saved/outputted into: 
syslog_alerts.log file in ./Desktop directory
