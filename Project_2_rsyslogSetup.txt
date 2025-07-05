Linux rsyslog setup on personal OS 

damianhall@ip-10-10-99-1:~$ sudo systemctl status rsyslog
● rsyslog.service - System Logging Service
     Loaded: loaded (/lib/systemd/system/rsyslog.service; enabled; vendor prese>
     Active: active (running) since Mon 2025-05-19 17:44:52 UTC; 56min ago
TriggeredBy: ● syslog.socket
       Docs: man:rsyslogd(8)
             https://www.rsyslog.com/doc/
   Main PID: 727 (rsyslogd)
      Tasks: 4 (limit: 4595)
     Memory: 2.3M
     CGroup: /system.slice/rsyslog.service
             └─727 /usr/sbin/rsyslogd -n -iNONE

May 19 17:44:52 ip-10-10-99-1 systemd[1]: Stopped System Logging Service.
May 19 17:44:52 ip-10-10-99-1 systemd[1]: Starting System Logging Service...
May 19 17:44:52 ip-10-10-99-1 systemd[1]: Started System Logging Service.
May 19 17:44:52 ip-10-10-99-1 rsyslogd[727]: imuxsock: Acquired UNIX socket '/r>
May 19 17:44:52 ip-10-10-99-1 rsyslogd[727]: rsyslogd's groupid changed to 110
May 19 17:44:52 ip-10-10-99-1 rsyslogd[727]: rsyslogd's userid changed to 104
May 19 17:44:52 ip-10-10-99-1 rsyslogd[727]: [origin software="rsyslogd" swVers>
May 19 17:44:56 ip-10-10-99-1 rsyslogd[727]: [origin software="rsyslogd" swVers>

Using text editor create configuration file in /etc/logs for our webserver
damianhall@ip-10-10-99-1:~/Desktop$ gedit /etc/rsyslog.d/98-websrv-02-ssh.conf

Input into file: 
$FileCreateMode 0644
:programname, isequal, "sshd" /var/log/websrv-02/rsyslog_sshd.log (added into created file) 

restart rsyslog: 
sudo systemctl restart rsyslog

cd /var/log/websrv-02/
damianhall@ip-10-10-99-1:/var/log/websrv-02$ ls 
hashes_2023-08-15_rsyslog_cron.txt  rsyslog_cron.log.1.gz
hashes_2023-08-24_rsyslog_cron.txt  rsyslog_cron.log.2.gz
hashes_2025-04-27_rsyslog_cron.txt  rsyslog_cron.log.3.gz
hashes_2025-05-11_rsyslog_cron.txt  rsyslog_cron.log.4.gz
hashes_2025-05-19_rsyslog_cron.txt  rsyslog_cron.log.5.gz
rsyslog_cron.log                    rsyslog_sshd.log

damianhall@ip-10-10-99-1:/var/log/websrv-02$ ssh localhost
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:wKfZ3YhyMsNSPzUrgKO2CjD8WiFrTLKzoDVmEkXZjKQ.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
damianhall@localhost's password: 

LOGS: 
.........
May 19 18:44:15 ip-10-10-99-1 sshd[14830]: error: kex_exchange_identification: client sent invalid protocol identifier ""
May 19 18:44:15 ip-10-10-99-1 sshd[14830]: error: send_error: write: Broken pipe
May 19 18:44:32 ip-10-10-99-1 sshd[14854]: Connection closed by authenticating user damianhall 127.0.0.1 port 33138 [preauth]

