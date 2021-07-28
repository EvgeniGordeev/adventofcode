# adventofcode

* https://adventofcode.com
* [Collection of external solutions](https://github.com/Bogdanp/awesome-advent-of-code)
* [300 stars and visualizations](https://github.com/surgi1/adventofcode)
* [rust under 1 second](https://timvisee.com/blog/solving-aoc-2020-in-under-a-second/)
* [rust under 1 second #2](https://www.forrestthewoods.com/blog/solving-advent-of-code-in-under-a-second/)
* https://github.com/narimiran/AdventOfCode2020

## 2020

* https://adventofcode.com/2020

* profiling with hyperfine - `brew install hyperfine`
|Day|Name|Solution|Stats (`hyperfine -r 10 'python 2020/01.py'` or `python -m cProfile 2020/01.py` or `time python 2020/11.py`)
|---|---|---|---|
|[01](https://adventofcode.com/2020/day/1)|Report Repair|[py](2020/01.py)|31.8 ms|
|[02](https://adventofcode.com/2020/day/2)|Password Philosophy|[py](2020/02.py)|37.5 ms|
|[03](https://adventofcode.com/2020/day/3)|Toboggan Trajectory|[py](2020/03.py)|34.1 ms|
|[04](https://adventofcode.com/2020/day/4)|Passport Processing|[py](2020/04.py)|36.1 ms|
|[05](https://adventofcode.com/2020/day/5)|Binary Boarding|[py](2020/05.py)|34.7 ms|
|[06](https://adventofcode.com/2020/day/6)|Custom Customs|[py](2020/06.py)|35.6 ms|
|[07](https://adventofcode.com/2020/day/7)|Handy Haversacks|[py](2020/07.py)|36.8 ms|
|[08](https://adventofcode.com/2020/day/8)|Handheld Halting|[py](2020/08.py)|42.4 ms|
|[09](https://adventofcode.com/2020/day/9)|Encoding Error|[py](2020/09.py)|43.1 ms|
|[10](https://adventofcode.com/2020/day/10)|Adapter Array|[py](2020/10.py)|33.5 ms|
|[11](https://adventofcode.com/2020/day/11)|Seating System|[py](2020/11.py)|5.134 s|
|[12](https://adventofcode.com/2020/day/12)|Rain Risk|[py](2020/12.py)|35.8 ms|
|[13](https://adventofcode.com/2020/day/13)|Shuttle Search|[py](2020/13.py)|39.4 ms|
|[14](https://adventofcode.com/2020/day/14)|Docking Data|[py](2020/14.py)|340.6 ms|
|[15](https://adventofcode.com/2020/day/15)|Rambunctious Recitation|[py](2020/15.py)|27.816 s|
|[16](https://adventofcode.com/2020/day/16)|Ticket Translation|[py](2020/16.py)|41.8 ms|
|[17](https://adventofcode.com/2020/day/17)|Conway Cubes|**||
|[18](https://adventofcode.com/2020/day/18)|Operation Order|[py](2020/18.py)|61.1 ms|
|[19](https://adventofcode.com/2020/day/19)|Monster Messages|**||
|[20](https://adventofcode.com/2020/day/20)|Jurassic Jigsaw|**||
|[21](https://adventofcode.com/2020/day/21)|Allergen Assessment|[py](2020/21.py)|35.4 ms|
|[22](https://adventofcode.com/2020/day/22)|Crab Combat|[py](2020/22.py)|120.5 ms|
|[23](https://adventofcode.com/2020/day/23)|Crab Cups|[py](2020/23.py)**||
|[24](https://adventofcode.com/2020/day/24)|Lobby Layout|[py](2020/24.py)|24577650 function calls in 54.416 seconds|
|[25](https://adventofcode.com/2020/day/25)|Combo Breaker|[py](2020/25.py)||

* or ** - external solution adopted

## tools

download input of last day:

* install:

```bash
go get -u github.com/GreenLightning/advent-of-code-downloader/aocdl
go build -v github.com/GreenLightning/advent-of-code-downloader/aocdl
mv aocdl /usr/local/bin/
echo '{"session-cookie": "xxx"}' > $HOME/.aocdlconfig
echo "
#!/usr/bin/env bash
aocdl --force
pbcopy <input.txt
" > get.sh
chmod +x get.sh
```

* download to input.txt and copy to clipboard:

```bash
./get.sh
```

## Py Tops from Leaderboard

* https://github.com/sophiebits/adventofcode
* https://github.com/arknave/advent-of-code-2020