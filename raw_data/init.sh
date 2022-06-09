#!/bin/bash

rm *.xlsx *.csv
unzip ../data/data.zip
head -n 100 ./weather.csv > ./weather100.csv

