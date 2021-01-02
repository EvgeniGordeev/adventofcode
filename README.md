# adventofcode

* https://adventofcode.com
* [Collection of external solutions](https://github.com/Bogdanp/awesome-advent-of-code)

## 2020

* https://adventofcode.com/2020

|Day|Name|Solution|Stats (`python -O -m profile 2020/01.py`)
|---|---|---|---|
|[01](https://adventofcode.com/2020/day/1)|Report Repair|[py](2020/01.py)|457 function calls in 0.065 seconds|
|[02](https://adventofcode.com/2020/day/2)|Password Philosophy|[py](2020/02.py)|17117 function calls in 0.038 seconds|
|[03](https://adventofcode.com/2020/day/3)|Toboggan Trajectory|[py](2020/03.py)|5351 function calls in 0.016 seconds|
|[04](https://adventofcode.com/2020/day/4)|Passport Processing|[py](2020/04.py)|8697 function calls in 0.020 seconds|
|[05](https://adventofcode.com/2020/day/5)|Binary Boarding|[py](2020/05.py)|4323 function calls in 0.012 seconds|
|[06](https://adventofcode.com/2020/day/6)|Custom Customs|[py](2020/06.py)|4529 function calls in 0.015 seconds|
|[07](https://adventofcode.com/2020/day/7)|Handy Haversacks|[py](2020/07.py)|18025 function calls in 0.047 seconds|
|[08](https://adventofcode.com/2020/day/8)|Handheld Halting|[py](2020/08.py)|62482 function calls in 0.136 seconds|
|[09](https://adventofcode.com/2020/day/9)|Encoding Error|[py](2020/09.py)|1470 function calls in 0.014 seconds|
|[10](https://adventofcode.com/2020/day/10)|Adapter Array|[py](2020/10.py)|216 function calls in 0.002 seconds|
|[11](https://adventofcode.com/2020/day/11)|Seating System|[py](2020/11.py)|9225289 function calls in 23.786 seconds|
|[12](https://adventofcode.com/2020/day/12)|Rain Risk|[py](2020/12.py)|13547 function calls in 0.046 seconds|
|[13](https://adventofcode.com/2020/day/13)|Shuttle Search|[py](2020/13.py)|5107 function calls in 0.016 seconds|
|[14](https://adventofcode.com/2020/day/14)|Docking Data|[py](2020/14.py)|1838789 function calls in 3.656 seconds|
|[15](https://adventofcode.com/2020/day/15)|Rambunctious Recitation|[py](2020/15.py)|37 function calls in 27.338 seconds|
|[16](https://adventofcode.com/2020/day/16)|Ticket Translation|[py](2020/16.py)|1556 function calls in 0.015 seconds|
|[17](https://adventofcode.com/2020/day/17)|Conway Cubes|||
|[18](https://adventofcode.com/2020/day/18)|Operation Order|[py](2020/18.py)|43291 function calls in 0.131 seconds|
|[19](https://adventofcode.com/2020/day/19)|Monster Messages|[py](2020/19.py)||
|[20](https://adventofcode.com/2020/day/20)|Jurassic Jigsaw|||
|[21](https://adventofcode.com/2020/day/21)|Allergen Assessment|[py](2020/21.py)|786 function calls in 0.005 seconds|
|[22](https://adventofcode.com/2020/day/22)|Crab Combat|[py](2020/22.py)|1107572 function calls in 2.289 seconds|
|[23](https://adventofcode.com/2020/day/23)|Crab Cups|[py](2020/23.py)|11000209 function calls in 43.072 seconds|

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