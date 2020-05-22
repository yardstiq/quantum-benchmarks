#!/bin/sh
echo "benchmarking yao..."
sleep 5
# julia --color=yes benchmarks.jl
echo "finished $(basename $(dirname $0))"
