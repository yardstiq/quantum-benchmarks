benchmark_pytest() {
    # set threads to one
    echo "benchmark pytest: $1 ($(date +"%Y-%m-%d-%H-%M-%S"))"
    export OMP_NUM_THREADS=1
    export MKL_NUM_THREADS=1
    export MKL_DOMAIN_NUM_THREADS=1
    
    mkdir -p "$BENCHMARK_LOG_PATH" "$BENCHMARK_DATA_PATH"
    ./env/bin/pytest "$1/benchmarks.py" --benchmark-storage="file://$BENCHMARK_DATA_PATH" \
        --benchmark-save=$1 --benchmark-sort=name --benchmark-min-rounds=5 \
        > "$BENCHMARK_LOG_PATH/$1.out" 2> "$BENCHMARK_LOG_PATH/$1.err"
}
