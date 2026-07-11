#!/usr/bin/env bash
set -euo pipefail

echo "OutcomeIQ AWS Lightsail server setup"
echo "This script installs Docker tooling only. It does not clone repos or create secrets."

sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg git

sudo install -m 0755 -d /etc/apt/keyrings
if [ ! -f /etc/apt/keyrings/docker.gpg ]; then
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg
fi

. /etc/os-release
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu ${VERSION_CODENAME} stable" |
  sudo tee /etc/apt/sources.list.d/docker.list >/dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo usermod -aG docker "$USER"
sudo mkdir -p /opt/outcomeiq
sudo chown "$USER":"$USER" /opt/outcomeiq

echo
echo "Server setup complete."
echo "Next manual steps:"
echo "1. Log out and SSH back in so docker group membership applies."
echo "2. Clone the OutcomeIQ repository into /opt/outcomeiq."
echo "3. Create /opt/outcomeiq/backend/.env manually from backend/.env.aws.example."
echo "4. Run: docker compose -f docker-compose.aws.yml up -d --build"
