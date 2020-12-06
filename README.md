# adventofcode

* https://adventofcode.com
* [Collection of external solutions](credit/Bogdanp/awesome-advent-of-code)

## 2020

https://adventofcode.com/2020

|Day|Name|Solution|
|---|---|---|
|[01](https://adventofcode.com/2020/day/1)|Report Repair|[py](2020/01.py)|
|[02](https://adventofcode.com/2020/day/2)|Password Philosophy|[py](2020/02.py)|
|[03](https://adventofcode.com/2020/day/3)|Toboggan Trajectory|[py](2020/03.py)|
|[04](https://adventofcode.com/2020/day4)|Passport Processing|[py](2020/04.py)|
|[05](https://adventofcode.com/2020/day5)|Binary Boarding|[py](2020/05.py)|
|[06](https://adventofcode.com/2020/day6)|SOME|[py](2020/06.py)|


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