#!/bin/bash

YEAR=$1

mkdir WTH_$YEAR
wget http://www.ffothello.org/wthor/base_zip/WTH_$YEAR.ZIP
unzip WTH_$YEAR.ZIP -d WTH_$YEAR
rm WTH_$YEAR.ZIP
./convert.rb WTH_$YEAR/WTH_$YEAR.wtb

echo "Converted WTHOR Database for year $YEAR to WTH_$YEAR/WTH_$YEAR.txt"
