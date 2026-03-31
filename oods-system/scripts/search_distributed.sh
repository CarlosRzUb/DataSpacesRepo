#!/bin/bash

ID=$1

MATCHES=$(cat providers/*/observations.csv | grep "$ID")

echo "$MATCHES"

TOTAL=$(echo "$MATCHES" | grep -c "$ID")

echo "Found $TOTAL matches."
