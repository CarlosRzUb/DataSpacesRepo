#!/bin/bash
REPORT="reports/data_space_health.txt"
mkdir -p reports
echo "DATA SPACE HEALTH REPORT" > "$REPORT"
echo "Total datasets: $(ls providers/*/observations.csv | wc -l)" >> "$REPORT"
echo "Datasets missing metadata: $(./scripts/check_metadata_coverage.sh | wc -l)" >> "$REPORT"
echo "Empty datasets: $(find providers/ -name "*.csv" -empty | wc -l)" >> "$REPORT"
echo "Inconsistent datasets: $(./scripts/check_metadata_consistency.sh | wc -l)" >> "$REPORT"
echo "Federated queries complete: $(./scripts/check_query_completeness.sh | tail -n 1 | cut -d' ' -f2)" >> "$REPORT"
