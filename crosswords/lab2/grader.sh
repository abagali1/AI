#!/bin/bash

grader() {
  timeout 30 ./crosswords.py 4x4 0 "dct20k.txt"
  echo -e '\n'
  timeout 30 ./crosswords.py 5x5 0 "dct20k.txt" "H3x0scare"
  echo -e '\n'
  timeout 30 ./crosswords.py 5x5 0 "dct20k.txt" "V0x3M"
  echo -e '\n'
  timeout 30 ./crosswords.py 4x4 2 "dct20k.txt"
  echo -e '\n'
  timeout 30 ./crosswords.py 5x5 2 "dct20k.txt" "h1x4N"
  echo -e '\n'
  timeout 30 ./crosswords.py 5x5 4 "dct20k.txt" "v0x3M"
  echo -e '\n'
  timeout 30 ./crosswords.py 4x5 0 "dct20k.txt"
  echo -e '\n'
  timeout 30 ./crosswords.py 5x4 0 "dct20k.txt"
  echo -e '\n'
  timeout 30 ./crosswords.py 7x7 11 "dctEckel.txt"
  echo -e '\n'
  timeout 30 ./crosswords.py 9x13 19 "dctEckel.txt" "v2x3#" "v1x8#" "h3x1#" "v4x5##"
  echo -e '\n'
  timeout 30 ./crosswords.py 15x15 37 "dctEckel.txt" "H0x4#" "v4x0#" "h2x3a"
  echo -e '\n'
}

time grader