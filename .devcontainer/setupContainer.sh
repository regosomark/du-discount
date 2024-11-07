[ -f packages.txt ] &&
sudo apt update &&
sudo apt upgrade -y &&
sudo xargs apt install -y <packages.txt;

[ -f requirements.txt ] &&
pip3 install --user -r requirements.txt;
echo '✅ Packages installed and Requirements met'