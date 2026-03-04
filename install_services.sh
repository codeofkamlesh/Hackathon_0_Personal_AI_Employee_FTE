#!/bin/bash
# Install systemd services for watchers

echo "Installing systemd services..."

# Copy service files
sudo cp gmail-watcher.service /etc/systemd/system/
sudo cp linkedin-watcher.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable services to start on boot
sudo systemctl enable gmail-watcher.service
sudo systemctl enable linkedin-watcher.service

# Start services
sudo systemctl start gmail-watcher.service
sudo systemctl start linkedin-watcher.service

echo ""
echo "✓ Services installed and started!"
echo ""
echo "Useful commands:"
echo "  Status:  sudo systemctl status gmail-watcher"
echo "  Status:  sudo systemctl status linkedin-watcher"
echo "  Stop:    sudo systemctl stop gmail-watcher"
echo "  Start:   sudo systemctl start gmail-watcher"
echo "  Logs:    sudo journalctl -u gmail-watcher -f"
