# adventofcode

[![example workflow](https://github.com/EvgeniGordeev/adventofcode/actions/workflows/ci2024.yaml/badge.svg)](https://github.com/EvgeniGordeev/adventofcode/actions)
[![example workflow](https://github.com/EvgeniGordeev/adventofcode/actions/workflows/ci2023.yaml/badge.svg)](https://github.com/EvgeniGordeev/adventofcode/actions)
[![example workflow](https://github.com/EvgeniGordeev/adventofcode/actions/workflows/ci2022.yaml/badge.svg)](https://github.com/EvgeniGordeev/adventofcode/actions)
[![example workflow](https://github.com/EvgeniGordeev/adventofcode/actions/workflows/ci2021.yaml/badge.svg)](https://github.com/EvgeniGordeev/adventofcode/actions)
[![example workflow](https://github.com/EvgeniGordeev/adventofcode/actions/workflows/ci2020.yaml/badge.svg)](https://github.com/EvgeniGordeev/adventofcode/actions)
[![example workflow](https://github.com/EvgeniGordeev/adventofcode/actions/workflows/ci2015.yaml/badge.svg)](https://github.com/EvgeniGordeev/adventofcode/actions)

## repo

[EvgeniGordeev/adventofcode](https://github.com/EvgeniGordeev/adventofcode)

## ci

[GitHub Actions](https://github.com/EvgeniGordeev/adventofcode/actions) based
on [Docker image](https://hub.docker.com/r/egordeev/adventofcode) built with `make build-ci`.

## tools

[Benchmark](https://github.com/sharkdp/hyperfine)

### profiling

To profile with hyperfine - `brew install hyperfine`

* `hyperfine --warmup 3 -r 10 '2024/01.py'`
* `find 2024 -type f -regex ".*/[0-9]*\.py" -exec hyperfine --warmup 3 -r 10 'python {}' \;`
* `time python 2024/01.py`
* `python -m cProfile 2024/01.py`

### profiling visualization

To create a visualization of the profiling results (requires `brew install graphviz`):

```shell
export problem=2024/01 && python -m cProfile -o $problem.pstats $problem.py && gprof2dot -f pstats $problem.pstats | dot -Tpng -o $problem.png
```

## solutions

| Year                                                           | Stars                                                 | Solutions       | M1 2021 Benchmark                                                                                                                                                                                                                                   | CI Benchmark                                                                                                                                                                                                                                      |
|----------------------------------------------------------------|-------------------------------------------------------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [https://adventofcode.com/2024](https://adventofcode.com/2024) | ![](https://img.shields.io/badge/stars%20⭐-10-yellow) | [2024](2024.md) | [![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2024-all-m1.json)](https://github.com/EvgeniGordeev/adventofcode/blob/main/2024/benchmark-m1.txt) | [![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2024-all-ci.json)](https://github.com/EvgeniGordeev/adventofcode/actions/workflows/ci2024.yaml) |
| [https://adventofcode.com/2023](https://adventofcode.com/2023) | ![](https://img.shields.io/badge/stars%20⭐-8-yellow)  | [2023](2023.md) | [![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2023-all-m1.json)](https://github.com/EvgeniGordeev/adventofcode/blob/main/2023/benchmark-m1.txt) | [![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2023-all-ci.json)](https://github.com/EvgeniGordeev/adventofcode/actions/workflows/ci2023.yaml) |
| [https://adventofcode.com/2022](https://adventofcode.com/2022) | ![](https://img.shields.io/badge/stars%20⭐-18-yellow) | [2022](2022.md) | [![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2022-all-m1.json)](https://github.com/EvgeniGordeev/adventofcode/blob/main/2022/benchmark-m1.txt) | [![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2022-all-ci.json)](https://github.com/EvgeniGordeev/adventofcode/actions/workflows/ci2022.yaml) |
| [https://adventofcode.com/2021](https://adventofcode.com/2021) | ![](https://img.shields.io/badge/stars%20⭐-30-yellow) | [2021](2021.md) | [![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2021-all-m1.json)](https://github.com/EvgeniGordeev/adventofcode/blob/main/2021/benchmark-m1.txt) | [![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2021-all-ci.json)](https://github.com/EvgeniGordeev/adventofcode/actions/workflows/ci2021.yaml) |
| [https://adventofcode.com/2020](https://adventofcode.com/2020) | ![](https://img.shields.io/badge/stars%20⭐-45-yellow) | [2020](2020.md) | 28.560 s                                                                                                                                                                                                                                            | [![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2020-all.json)](https://github.com/EvgeniGordeev/adventofcode/actions/workflows/ci2020.yaml)    |
| [https://adventofcode.com/2015](https://adventofcode.com/2015) | ![](https://img.shields.io/badge/stars%20⭐-6-yellow)  | [2015](2015.md) | 33 ms                                                                                                                                                                                                                                               | [![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2015-all.json)](https://github.com/EvgeniGordeev/adventofcode/actions/workflows/ci2015.yaml)    |



