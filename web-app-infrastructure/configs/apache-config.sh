# Commands to install Apache on an Ubuntu EC2 instance
# Run these via SSH after launching your EC2 instance
sudo apt update
sudo apt install -y apache2
sudo systemctl start apache2
sudo systemctl enable apache2