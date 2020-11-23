#!/bin/bash
input="./custom_train/validdf.txt"

while IFS= read -r line
do
  A="$(cut -d'/' -f6 <<<$line)"
  I="./data/val/deepfake/$A"
  ln -s "../../../$line" $I

done < "$input"