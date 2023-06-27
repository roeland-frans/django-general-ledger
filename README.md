## Setup Linux Environment

### Install System Requirements
```
sudo apt install zsh git direnv python3 python3-pip python3-venv
sudo usermod -s /usr/bin/zsh $(whoami)
sudo reboot
```

### Setup Dev Environment
```
sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
direnv hook zsh >> ~/.zshrc
direnv allow .
curl -LO https://github.com/BurntSushi/ripgrep/releases/download/11.0.1/ripgrep_11.0.1_amd64.deb
sudo dpkg -i ripgrep_11.0.1_amd64.deb
rm sudo dpkg -i ripgrep_11.0.1_amd64.deb
```


