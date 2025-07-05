SSH monitor 

nano ssh_monitor.sh 

#!/bin/bash

LOG_FILE="/var/log/auth.log"
ALERT_LOG="$HOME/ssh_alerts.log"

echo "Monitoring SSH login attempts..."
echo "Logs will be saved to: $ALERT_LOG"
echo "Press Ctrl+C to stop."

# Monitor the log in real-time
tail -F "$LOG_FILE" | while read line; do
    # Look for failed SSH login attempts
    if echo "$line" | grep -q "Failed password for"; then
        echo "[FAILED LOGIN] $(date): $line" >> "$ALERT_LOG"
        echo "Failed SSH login attempt detected!"
    
    # Look for successful SSH logins
    elif echo "$line" | grep -q "Accepted password for"; then
        echo "[SUCCESSFUL LOGIN] $(date): $line" >> "$ALERT_LOG"
        echo "Successful SSH login detected!"
    fi
done

---------------------------------------