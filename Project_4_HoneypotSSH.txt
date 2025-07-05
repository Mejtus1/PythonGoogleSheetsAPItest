ssh honeypot 

nano fake_ssh_honeypot.sh

#!/bin/bash

LOG_FILE="$HOME/Desktop/fake_ssh_honeypot.log"
PORT=2222

echo "[+] Starting fake SSH honeypot on port $PORT..."
echo "[+] Logging connections to $LOG_FILE"
echo

# Infinite loop to keep listening
while true; do
    # Wait for a connection and log the IP and time
    nc -l -p $PORT -c '
        echo "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3"

        IP=$(echo $SOCAT_PEERADDR)
        TIMESTAMP=$(date)

        # Terminal notification
        echo "[!] Connection attempt detected from $IP at $TIMESTAMP"

        # Log to file
        echo "[!] Connection from $IP at $TIMESTAMP" >> "'"$LOG_FILE"'"

        sleep 1
    '
done

terminal: 
sudo ./fake_ssh_honeypot.sh

ssh fake@your_ip -p 2222

[!] Connection attempt detected from 192.168.1.42 at Mon May 20 14:13:22

