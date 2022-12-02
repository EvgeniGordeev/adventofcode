## 2015

![](https://img.shields.io/badge/stars%20⭐-2-yellow)
![](https://img.shields.io/badge/days%20completed-1-red)
![](https://img.shields.io/badge/day%20📅-25-blue)
[![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2015.json)](https://github.com/EvgeniGordeev/adventofcode/actions)

* [https://adventofcode.com/2015](https://adventofcode.com/2015)

* ```hyperfine --warmup 3 -r 10 '2015/01.py'```
* ```find 2015 -type f -regex ".*/[0-9]*\.py" -exec hyperfine --warmup 3 -r 10 'python {}' \;```
* ```hyperfine --warmup 3 -r 10 'python 2015/all.py'```
* ```python -m cProfile 2015/01.py```
* ```time python 2015/01.py```

| Day                                       | Name                              | Solution                                  | M1 Stats                                                                                                                                                                                                                              |
|-------------------------------------------|-----------------------------------|-------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [01](https://adventofcode.com/2015/day/1) | Not Quite Lisp                    | [py](2015/01.py)                          | 31 ms                                                                                                                                                                                                                                 |
| [01](https://adventofcode.com/2015/day/2) | I Was Told There Would Be No Math | [py](2015/02.py)                          | 37 ms                                                                                                                                                                                                                                 |
| ---                                       | ------                            | ---------                                 | ---                                                                                                                                                                                                                                   |
| [all](https://adventofcode.com/2015)      | AoC 15                            | [py](2015/all.py) [txt](2015/answers.txt) | M1 - 66 ms, CI - [![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EvgeniGordeev/13c6cac3c39702cdcb9cc169b66c3210/raw/runtime-badge-2015.json)](https://github.com/EvgeniGordeev/adventofcode/actions) |

* or ** - external solution adopted
