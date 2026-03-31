#!/bin/bash

for file in providers/*/observations.csv
do
	directory=$(basename "$(dirname "$file")")
	lines=$(wc -l < "$file")
	echo "$directory: $lines"
done
