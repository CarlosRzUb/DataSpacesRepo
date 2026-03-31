#!/bin/bash
IDS=$(cut -d, -f2 providers/*/observations.csv | grep -v "object_id" | sort | uniq -c)
echo "Objects in all providers:"
echo "$IDS" | awk '$1 == 3 {print $2}'
echo "Objects in only one provider:"
echo "$IDS" | awk '$1 == 1 {print $2}'
