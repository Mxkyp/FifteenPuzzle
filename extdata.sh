#!/usr/bin/env bash
#
# Extract data regarding performance of various strategies used to search the
# state space in order to solve the 15-puzzle. Data are extracted from
# statistics files generated by a solver program and stored in the current
# directory, aggregated in a tabular form, and the result is written to the
# standard output.
#
# The names of the statistics files should obey the following format:
#  size_depth_id_strategy_param_stats.txt
# for example:
#  4x4_01_00001_bfs_rdul_stats.txt

stats_filename_regex='^[a-zA-Z0-9]+_([0-9]+)_([0-9]+)_([a-zA-Z]+)_([a-zA-Z]+)_stats.txt$'

echo "Depth ID Strategy Param SolutionLength Visited Processed Depth Time"
for filename in *; do
    if [[ -f "$filename" && "$filename" =~ $stats_filename_regex ]]; then
        line=$(printf "%d %d %s %s " $((10#${BASH_REMATCH[1]})) \
               $((10#${BASH_REMATCH[2]})) ${BASH_REMATCH[3]} ${BASH_REMATCH[4]})
        line+=$(cat "$filename" | tr '\n' ' ')
        echo "$line"
    fi
done
