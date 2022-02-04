#!/usr/bin/env python3

# INPUT
from collections.abc import Iterable


def parser(text) -> str:
    return text.strip()


def read_input() -> str:
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


# MAIN
def to_bin(s: str) -> str:
    res = []
    for char in s:
        res.append(bin(int(char, 16))[2:].zfill(4))
    return ''.join(res)


def parse(bin_s: str, start=0) -> tuple:
    version = int(bin_s[:3], 2)
    type_id = int(bin_s[3:6], 2)
    if type_id == 4:
        size, cursor = len(bin_s), 11
        res = []
        while cursor <= len(bin_s):
            res.append(bin_s[cursor - 5:cursor])
            cursor += 5
        bin_res = ''.join(b[-4:] for b in res)
        return version, int(bin_res, 2)
    else:
        len_type_id = bin_s[6]
        if len_type_id == '0':
            limit = int(bin_s[7:22], 2)
            step = 11
            size = 11
            cursor = 33
            res = []
            while cursor <= len(bin_s) or size <= limit:
                res.append(parse(bin_s[cursor - step:cursor]))
                size += step
                step += 5
                cursor += step
            return version, res
        elif len_type_id == '1':
            num_of_subpacks = int(bin_s[7:18], 2)
            step, cursor = 0, 29
            res = []
            while cursor <= len(bin_s) or step < num_of_subpacks:
                res.append(parse(bin_s[cursor - 11:cursor]))
                cursor += 11
                step += 1
            return version, res


def part1(hex_s: str) -> tuple:
    bin_str = to_bin(hex_s)
    t = parse(bin_str)
    res = t[0]
    if isinstance(t[1], Iterable):
        res += sum(v for v, _ in t[1])
    return res


def part2(message: str) -> int:
    return -1


# TEST
def test():
    # GIVEN
    assert part1('D2FE28') == 6
    assert part1('38006F45291200') == 9
    assert part1('EE00D40C823060') == 14
    assert part1('8A004A801A8002F478') == 16
    assert part1('620080001611562C8802118E34') == 23
    assert part1('A0016C880162017C3686B18A3D4780') == 31
    # part 2
    return True


if __name__ == '__main__':
    assert test()
    input_ = parser(read_input())
    # ONE #1
    # part_1 = part1(*input_)
    # print(part_1)
    # assert part_1 == 3048
    # TWO #2
    # part_2 = part2(*input_)
    # print(part_2)
    # assert part_2 == 3_288_891_573_057

# INPUT
"""🎅
20546718027401204FE775D747A5AD3C3CCEEB24CC01CA4DFF2593378D645708A56D5BD704CC0110C469BEF2A4929689D1006AF600AC942B0BA0C942B0BA24F9DA8023377E5AC7535084BC6A4020D4C73DB78F005A52BBEEA441255B42995A300AA59C27086618A686E71240005A8C73D4CF0AC40169C739584BE2E40157D0025533770940695FE982486C802DD9DC56F9F07580291C64AAAC402435802E00087C1E8250440010A8C705A3ACA112001AF251B2C9009A92D8EBA6006A0200F4228F50E80010D8A7052280003AD31D658A9231AA34E50FC8010694089F41000C6A73F4EDFB6C9CC3E97AF5C61A10095FE00B80021B13E3D41600042E13C6E8912D4176002BE6B060001F74AE72C7314CEAD3AB14D184DE62EB03880208893C008042C91D8F9801726CEE00BCBDDEE3F18045348F34293E09329B24568014DCADB2DD33AEF66273DA45300567ED827A00B8657B2E42FD3795ECB90BF4C1C0289D0695A6B07F30B93ACB35FBFA6C2A007A01898005CD2801A60058013968048EB010D6803DE000E1C6006B00B9CC028D8008DC401DD9006146005980168009E1801B37E02200C9B0012A998BACB2EC8E3D0FC8262C1009D00008644F8510F0401B825182380803506A12421200CB677011E00AC8C6DA2E918DB454401976802F29AA324A6A8C12B3FD978004EB30076194278BE600C44289B05C8010B8FF1A6239802F3F0FFF7511D0056364B4B18B034BDFB7173004740111007230C5A8B6000874498E30A27BF92B3007A786A51027D7540209A04821279D41AA6B54C15CBB4CC3648E8325B490401CD4DAFE004D932792708F3D4F769E28500BE5AF4949766DC24BB5A2C4DC3FC3B9486A7A0D2008EA7B659A00B4B8ACA8D90056FA00ACBCAA272F2A8A4FB51802929D46A00D58401F8631863700021513219C11200996C01099FBBCE6285106
⛄"""
