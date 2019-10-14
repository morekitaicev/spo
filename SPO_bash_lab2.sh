#!/bin/bash
echo "Please, stand by"
echo "Installing git"
sudo apt-get install git  #Устанавливаем git
echo "Installing golang in /usr/local"
wget -c https://dl.google.com/go/go1.13.1.linux-amd64.tar.gz #Скачиваем архив go
sudo tar -C /usr/local -xvzf go1.13.1.linux-amd64.tar.gz #Распаковываем архив в системную папку
mkdir -p ~/go
mkdir -p ~/go_projects/{bin,src,pkg} #Создаем дополнительные системные директории для go
echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile
echo 'export GOPATH="$HOME/go_projects"' >> ~/.profile
echo 'export GOBIN="$GOPATH/bin"' >> ~/.profile #Прописываем системные пути в файлы профиля
source ~/.profile
echo "Installing yggdrasil"
git clone https://github.com/yggdrasil-network/yggdrasil-go.git #Скачиваем утилиту с репозитория
cd yggdrasil-go
echo "Moved to yggdrasil dir"
./build #Устанавливаем утилиту
echo "Installation finished"
