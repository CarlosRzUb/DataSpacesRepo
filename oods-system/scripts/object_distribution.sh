#!/bin/bash
cut -d, -f2 providers/*/observations.csv | grep -v "object_id" | sort | uniq -c
