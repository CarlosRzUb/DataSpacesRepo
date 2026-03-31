#!/bin/bash

for file in providers/*/metadata.json
do
	grep data_path $file
done
