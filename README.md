# BOT
test


## install binance-api
pip install python-binance

## install ta-lib
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xvf ta-lib-0.4.0-src.tar.gz 
cd ta-lib
./configure --prefix=/usr
make
sudo make install
sudo ldconfig

pip3 install ta-lib