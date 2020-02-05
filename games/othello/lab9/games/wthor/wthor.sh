#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Missing required parameter: <year>"
    echo "Usage: ./wthor.sh <year>"
    echo "Required Parameter: <year> WTHOR Tournament Year to download database from"
    echo "<year> must be in the range of 1990-2019"
    exit 1
fi

YEAR=$1

mkdir WTH_$YEAR
wget http://www.ffothello.org/wthor/base_zip/WTH_$YEAR.ZIP
unzip WTH_$YEAR.ZIP -d WTH_$YEAR
rm WTH_$YEAR.ZIP
./convert.rb WTH_$YEAR/WTH_$YEAR.wtb

echo "Converted WTHOR Database for year $YEAR to WTH_$YEAR/WTH_$YEAR.txt"
