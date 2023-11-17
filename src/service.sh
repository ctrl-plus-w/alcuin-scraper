[Unit]
Description=alcuin-scraper-service
After=multi-user.target[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /home/nx/Tools/alcuin-scrapper/src/worker.py

[Install]
WantedBy=multi-user.target