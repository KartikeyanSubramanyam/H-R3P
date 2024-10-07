#! /bin/bash

set -o noclobber -e
for i in {0..9}; do echo "/data/scan/hospital/$(gdate -d "-$i day" +"%Y%m%d")/"; done > exclude.txt
{
    echo "rsync started"
    rsync -avz --progress --update --remove-source-files --exclude-from='exclude.txt' research-scan:/data/scan/hospital /chonk/scans
    if [ $? -eq 0 ]; then
        echo "[*] Success! Rsync completed."
    else
        echo "[!] Rsync failed."
        exit 1
    fi
} > "/chonk/svrao/logs/hospital-scan/$(date +"%Y_%m_%d_%I_%M_%p").log"

# 1. Pull files from the remote server to your local machine
# rsync -avz -e ssh username@remote-server:/path/to/remote/files /path/to/local/destination
# 2. Push files from your local machine to the remote server
# rsync -avz -e ssh /path/to/local/files username@remote-server:/path/to/remote/destination

rsync -e ssh /Users/kartik/Desktop/Hospital_Results kasubram@research-scan.sysnet.ucsd.edu:/home/kasubram/Hospital_Results
