#!/bin/bash

#rm *.xlsx *.csv
unzip ../data/data.zip
tail -n 100 ./weather.csv > ./weather100.csv

