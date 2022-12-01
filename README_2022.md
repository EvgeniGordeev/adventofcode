## 2022

![](https://img.shields.io/badge/stars%20⭐-2-yellow)
![](https://img.shields.io/badge/days%20completed-1-red)
![](https://img.shields.io/badge/day%20📅-1-blue)
[![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2022.json)](https://github.com/EvgeniGordeev/adventofcode/actions)

* [https://adventofcode.com/2022](https://adventofcode.com/2022)

To profile with hyperfine - ```brew install hyperfine```

* ```hyperfine --warmup 3 -r 10 '2022/01.py'```
* ```find 2022 -type f -regex ".*/[0-9]*\.py" -exec hyperfine --warmup 3 -r 10 'python {}' \;```
* ```hyperfine --warmup 3 -r 10 'python 2022/all.py'```
* ```python -m cProfile 2022/01.py```
* ```time python 2022/01.py```

| Day                                       | Name             | Solution                                  | M1 Stats                                                                                                                                                                                                                              |
|-------------------------------------------|------------------|-------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [01](https://adventofcode.com/2022/day/1) | Calorie Counting | [py](2022/01.py)                          | 35 ms                                                                                                                                                                                                                                 |
| ---                                       | ------           | ---------                                 | ---                                                                                                                                                                                                                                   |
| [all](https://adventofcode.com/2022)      | AoC 22           | [py](2022/all.py) [txt](2022/answers.txt) | M1 - 35 ms, CI - [![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2022.json)](https://github.com/EvgeniGordeev/adventofcode/actions) |

* or ** - external solution adopted