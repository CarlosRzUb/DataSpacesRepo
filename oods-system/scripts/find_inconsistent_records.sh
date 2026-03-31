#!/bin/bash
cat providers/*/observations.csv | grep -v "timestamp" | sort | uniq -u
