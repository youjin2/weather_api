# weather_api

# install requirements
```
# python 3.6.10
$ pip install -r requirements.txt
```

# example
```
$ cd weather_api
# request your service key on https://data.go.kr and save it as below
# e.g. echo "your_service_key" >> data/private_key
$ python -m src.download --kpath data/private_key --dpath /mnt/sdb1/data/asos/20190101_20191231 --sdate 2019-01-01 --edate 2019-12-31
```
