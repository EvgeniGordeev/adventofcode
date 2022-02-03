#!/usr/bin/env python3


import re
from collections import Counter, defaultdict


def parser(text) -> list:
    lines = [tuple(map(int, line)) for line in re.findall(r'(\d+),(\d+) -> (\d+),(\d+)', text.strip())]
    return lines


def read_input() -> str:
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


# MAIN FUNCTIONS
def points_hv(line) -> set:
    p1, p2 = sorted((line[:2], line[2:]))
    # only horizontal or vertical
    if p1[0] == p2[0] or p1[1] == p2[1]:
        return {(x, y) for x in range(p1[0], p2[0] + 1) for y in range(p1[1], p2[1] + 1)}


def part1(lines) -> int:
    ps = [h_or_v for lin in lines if bool(h_or_v := points_hv(lin))]
    intersections = set()
    for i, line1 in enumerate(ps):
        for line2 in ps[i + 1:]:
            intersections.update(line1 & line2)
    return len(intersections)


def points(line) -> set:
    h_or_v = points_hv(line)
    if h_or_v:
        return h_or_v
    p1, p2 = sorted((line[:2], line[2:]))
    x, y = p1
    line_points = {p1, p2}
    sign = lambda a: (a > 0) - (a < 0)
    x_sign, y_sign = sign(p2[0] - p1[0]), sign(p2[1] - p1[1])
    while (x, y) != p2:
        line_points.add((x, y))
        x += x_sign
        y += y_sign
    return line_points


def part2(lines) -> int:
    intersections = set()
    ps = [points(lin) for lin in lines]
    for i, line1 in enumerate(ps):
        for line2 in ps[i + 1:]:
            intersections.update(line1 & line2)
    return len(intersections)


# improved: 620 ms to 86 ms
def part1_improved(segments) -> int:
    grid = defaultdict(int)
    for line in segments:
        x1, y1, x2, y2 = line
        if y1 == y2:  # horizontal
            for i in range(min(x1, x2), max(x1, x2) + 1):
                grid[(i, y1)] += 1
        elif x1 == x2:  # vertical
            for i in range(min(y1, y2), max(y1, y2) + 1):
                grid[(x1, i)] += 1
    return sum(v > 1 for v in grid.values())


def part2_improved(segments) -> int:
    grid = defaultdict(int)
    for line in segments:
        x1, y1, x2, y2 = line
        if y1 == y2:  # horizontal
            for i in range(min(x1, x2), max(x1, x2) + 1):
                grid[(i, y1)] += 1
        elif x1 == x2:  # vertical
            for i in range(min(y1, y2), max(y1, y2) + 1):
                grid[(x1, i)] += 1
        else:  # diagonal
            sign = lambda a: (a > 0) - (a < 0)
            dx = sign(x2 - x1)
            dy = sign(y2 - y1)
            for i in range(abs(x2 - x1) + 1):
                grid[(x1 + i * dx, y1 + i * dy)] += 1
    return sum(v > 1 for v in grid.values())


#  external - v2
def part1_v2(lines):
    grid = {}

    for line in lines:
        x1, y1, x2, y2 = line
        if x1 == x2 or y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid[(x, y)] = grid.get((x, y), 0) + 1

    t = 0
    for v in grid.values():
        if v > 1:
            t += 1
    return t


def part2_v2(lines):
    grid = {}

    for line in lines:
        x1, y1, x2, y2 = line
        dx = x2 - x1
        dy = y2 - y1
        if dx: dx = dx // abs(dx)
        if dy: dy = dy // abs(dy)
        x = x1
        y = y1
        while True:
            grid[(x, y)] = grid.get((x, y), 0) + 1
            if x == x2 and y == y2:
                break
            x += dx
            y += dy

    t = 0
    for v in grid.values():
        if v > 1:
            t += 1
    return t


# external v3
def part1_v3(segments):
    straight = []
    for line in segments:
        x1, y1, x2, y2 = line
        (x1, y1), (x2, y2) = sorted([(x1, y1), (x2, y2)])
        if x1 == x2 or y1 == y2:
            straight += [(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)]
    position_counts = Counter(straight)
    return sum(v > 1 for v in position_counts.values())


def part2_v3(segments):
    straight, diagonal = [], []
    for line in segments:
        x1, y1, x2, y2 = line
        (x1, y1), (x2, y2) = sorted([(x1, y1), (x2, y2)])
        if x1 == x2 or y1 == y2:
            straight += [(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)]
        elif y1 < y2:
            diagonal += [(x, y1 + idx) for idx, x in enumerate(range(x1, x2 + 1))]
        else:
            diagonal += [(x, y1 - idx) for idx, x in enumerate(range(x1, x2 + 1))]
    position_counts = Counter(straight)

    position_counts += Counter(diagonal)
    return sum(v > 1 for v in position_counts.values())


# external v4
def part1_v4(segments):
    grid = defaultdict(int)
    for l in segments:
        # horizontal
        x1, y1, x2, y2 = l
        if y1 == y2:
            for i in range(min(x1, x2), max(x1, x2) + 1):
                grid[(i, y1)] += 1
        # vertical
        elif x1 == x2:
            for i in range(min(y1, y2), max(y1, y2) + 1):
                grid[(x1, i)] += 1

    return sum([1 if v > 1 else 0 for v in grid.values()])


def part2_v4(segments):
    grid = defaultdict(int)
    for l in segments:
        # horizontal
        x1, y1, x2, y2 = l
        if y1 == y2:
            for i in range(min(x1, x2), max(x1, x2) + 1):
                grid[(i, y1)] += 1
        # vertical
        elif x1 == x2:
            for i in range(min(y1, y2), max(y1, y2) + 1):
                grid[(x1, i)] += 1
        else:
            dx = 1 if x2 > x1 else -1
            dy = 1 if y2 > y1 else -1
            for i in range(abs(x2 - x1) + 1):
                grid[(x1 + i * dx, y1 + i * dy)] += 1

    return sum([1 if v > 1 else 0 for v in grid.values()])


# TEST
def test(part1, part2):
    # GIVEN
    given = parser("""
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""")
    assert part1(given) == 5
    # part 2
    assert points((1, 1, 3, 3)) == {(1, 1), (2, 2), (3, 3)}
    assert points((3, 0, 0, 3)) == {(0, 3), (1, 2), (2, 1), (3, 0)}
    assert part2(given) == 12

    return True


if __name__ == '__main__':
    # p1, p2 = part1, part2 # 620 ms
    # p1, p2 = part1_v2, part2_v2 # 101 ms
    # p1, p2 = part1_v3, part2_v3  # 103 ms
    # p1, p2 = part1_v4, part2_v4  # 87 ms
    p1, p2 = part1_improved, part2_improved  # 85 ms
    assert test(p1, p2)
    input_ = parser(read_input())
    # ONE #1
    part_1 = p1(input_)
    print(part_1)
    assert part_1 == 6666
    # TWO #2
    part_2 = p2(input_)
    print(part_2)
    assert part_2 == 19081

# INPUT
"""🎅
72,504 -> 422,154
877,851 -> 680,654
447,989 -> 517,989
173,125 -> 981,933
736,255 -> 374,617
835,681 -> 693,539
451,176 -> 451,885
793,629 -> 793,157
907,945 -> 47,85
868,104 -> 892,104
594,18 -> 384,18
454,880 -> 524,880
400,271 -> 915,271
843,989 -> 45,191
640,885 -> 845,885
115,370 -> 115,633
185,578 -> 185,648
159,929 -> 933,155
650,147 -> 650,523
719,72 -> 719,649
908,80 -> 18,970
417,246 -> 777,606
452,803 -> 170,803
311,324 -> 18,324
665,835 -> 108,278
654,122 -> 223,122
38,40 -> 38,713
658,471 -> 148,471
894,783 -> 894,693
461,950 -> 941,470
234,542 -> 941,542
441,793 -> 291,793
913,139 -> 302,139
978,24 -> 50,952
817,828 -> 374,385
919,68 -> 919,819
674,20 -> 722,20
950,698 -> 312,60
350,398 -> 213,398
93,627 -> 93,896
629,296 -> 118,296
324,372 -> 324,83
125,130 -> 543,130
29,40 -> 29,262
297,682 -> 768,211
578,173 -> 115,636
375,32 -> 375,667
755,937 -> 376,937
925,623 -> 735,623
538,57 -> 860,57
212,293 -> 212,797
725,844 -> 315,434
486,334 -> 486,564
392,924 -> 392,709
676,554 -> 676,411
807,520 -> 807,553
891,732 -> 973,650
617,445 -> 781,281
960,891 -> 353,284
264,543 -> 264,345
844,840 -> 844,753
567,963 -> 663,963
174,450 -> 477,450
259,943 -> 555,647
791,394 -> 791,34
962,532 -> 586,156
26,328 -> 519,821
904,132 -> 58,978
209,718 -> 209,591
364,73 -> 364,237
855,233 -> 268,820
923,577 -> 923,528
435,551 -> 393,593
506,168 -> 773,168
753,333 -> 753,178
124,375 -> 240,259
66,340 -> 66,248
596,533 -> 596,954
358,144 -> 358,368
106,866 -> 419,866
883,777 -> 185,79
325,981 -> 325,805
228,521 -> 228,602
808,938 -> 808,452
980,567 -> 980,293
696,129 -> 671,104
597,970 -> 731,970
691,920 -> 691,35
552,703 -> 616,639
74,124 -> 738,788
680,296 -> 680,467
858,76 -> 409,76
167,280 -> 167,346
172,576 -> 586,162
866,921 -> 866,975
760,192 -> 760,24
47,197 -> 47,781
657,136 -> 84,136
414,322 -> 76,322
14,923 -> 565,923
892,515 -> 426,49
560,325 -> 241,644
835,603 -> 471,603
421,54 -> 783,54
523,717 -> 523,188
272,473 -> 272,631
87,769 -> 87,459
983,110 -> 878,110
34,64 -> 34,362
40,717 -> 691,66
127,420 -> 127,697
289,337 -> 289,67
900,143 -> 956,143
118,450 -> 118,485
205,691 -> 205,179
674,363 -> 698,363
401,117 -> 776,117
619,15 -> 619,104
906,191 -> 167,930
505,228 -> 897,620
252,545 -> 51,344
235,917 -> 235,673
275,938 -> 275,892
909,518 -> 79,518
182,530 -> 182,324
708,314 -> 708,274
853,689 -> 542,378
221,802 -> 11,802
967,685 -> 967,469
402,360 -> 910,360
212,655 -> 212,602
126,860 -> 126,390
651,961 -> 406,961
482,491 -> 882,891
120,291 -> 120,570
305,437 -> 49,437
528,469 -> 112,885
146,689 -> 898,689
356,465 -> 356,722
967,576 -> 467,576
731,492 -> 731,684
845,330 -> 572,57
575,727 -> 544,727
257,703 -> 971,703
334,557 -> 456,557
701,241 -> 217,241
681,294 -> 438,537
797,874 -> 240,874
232,628 -> 41,628
586,529 -> 680,435
412,468 -> 130,468
83,200 -> 872,989
17,987 -> 979,25
304,103 -> 304,683
855,784 -> 236,165
770,866 -> 770,947
209,198 -> 720,709
915,779 -> 915,827
924,421 -> 172,421
191,265 -> 740,814
255,198 -> 903,198
600,147 -> 212,147
901,20 -> 25,896
662,96 -> 662,948
600,834 -> 600,549
556,142 -> 556,541
564,350 -> 803,111
921,927 -> 182,188
649,858 -> 649,953
751,435 -> 751,415
633,665 -> 633,160
487,343 -> 733,343
13,16 -> 976,979
91,692 -> 520,263
719,461 -> 843,461
236,645 -> 23,645
172,886 -> 172,936
429,310 -> 429,424
774,765 -> 31,22
72,495 -> 556,11
539,625 -> 539,124
270,735 -> 481,735
18,652 -> 18,662
710,405 -> 710,907
651,530 -> 651,365
526,41 -> 839,354
620,865 -> 965,865
889,383 -> 261,383
189,950 -> 483,950
591,402 -> 689,402
653,576 -> 653,430
13,600 -> 545,600
61,766 -> 491,766
432,533 -> 307,658
304,757 -> 304,274
988,52 -> 53,987
228,307 -> 813,307
651,414 -> 683,382
255,898 -> 71,898
901,263 -> 208,263
26,97 -> 300,371
546,133 -> 798,133
499,240 -> 412,153
415,877 -> 359,877
567,831 -> 685,831
102,510 -> 902,510
961,433 -> 386,433
399,252 -> 898,751
528,198 -> 528,241
71,28 -> 626,583
147,855 -> 158,855
218,879 -> 870,227
727,711 -> 226,210
402,797 -> 402,842
675,238 -> 675,311
98,917 -> 750,917
318,437 -> 343,412
197,311 -> 399,311
264,269 -> 696,269
100,475 -> 100,194
668,874 -> 668,822
564,52 -> 101,515
320,153 -> 320,894
656,574 -> 656,487
448,295 -> 448,112
543,108 -> 38,613
55,438 -> 742,438
547,140 -> 288,140
640,212 -> 320,212
406,760 -> 882,760
373,546 -> 373,693
79,328 -> 360,328
441,646 -> 441,614
25,197 -> 15,207
155,426 -> 457,728
874,36 -> 507,403
35,305 -> 420,305
635,629 -> 672,629
660,755 -> 660,862
535,124 -> 535,157
340,957 -> 72,689
601,734 -> 432,734
629,74 -> 768,74
526,454 -> 773,454
470,78 -> 489,78
301,820 -> 957,820
300,457 -> 697,854
100,90 -> 100,674
322,947 -> 322,209
964,973 -> 11,20
423,803 -> 937,289
19,980 -> 464,535
873,796 -> 873,240
125,29 -> 925,829
242,980 -> 750,980
419,576 -> 419,325
347,851 -> 769,429
599,704 -> 599,928
418,956 -> 693,956
83,76 -> 833,826
71,817 -> 926,817
210,312 -> 867,969
390,510 -> 664,784
969,520 -> 969,96
675,927 -> 684,918
157,541 -> 157,550
595,521 -> 595,576
378,629 -> 274,629
117,905 -> 942,80
891,336 -> 891,806
795,183 -> 795,517
285,396 -> 285,132
272,289 -> 347,289
204,495 -> 204,799
583,907 -> 176,907
961,574 -> 338,574
739,214 -> 739,858
78,102 -> 905,929
301,785 -> 301,810
687,560 -> 390,263
756,793 -> 60,97
913,918 -> 19,24
832,956 -> 219,343
916,54 -> 437,54
919,911 -> 120,112
681,200 -> 303,200
888,121 -> 888,769
266,274 -> 266,419
843,58 -> 54,847
542,438 -> 58,922
139,689 -> 259,809
773,22 -> 610,22
221,211 -> 221,915
636,474 -> 575,474
376,628 -> 376,95
105,210 -> 105,124
831,649 -> 989,649
52,207 -> 765,207
886,114 -> 564,436
817,41 -> 222,41
33,680 -> 24,689
975,698 -> 792,515
654,492 -> 654,116
555,976 -> 457,976
797,394 -> 797,521
21,980 -> 861,140
949,259 -> 316,892
485,311 -> 234,562
621,961 -> 621,656
864,232 -> 837,205
52,978 -> 987,43
441,63 -> 815,63
10,986 -> 983,13
213,207 -> 213,234
343,117 -> 343,889
732,92 -> 687,92
142,101 -> 142,736
419,248 -> 419,89
231,933 -> 672,492
603,49 -> 603,196
46,242 -> 46,55
31,257 -> 647,873
664,812 -> 53,201
642,772 -> 152,772
650,247 -> 650,16
578,197 -> 372,197
271,245 -> 271,350
281,820 -> 281,532
823,674 -> 255,106
735,657 -> 729,657
859,933 -> 859,395
183,939 -> 919,203
739,804 -> 739,128
581,494 -> 329,494
231,875 -> 231,166
193,911 -> 833,911
290,785 -> 290,866
57,152 -> 57,105
359,585 -> 905,39
96,669 -> 468,669
813,576 -> 959,576
711,157 -> 711,791
211,789 -> 211,716
561,881 -> 929,881
474,215 -> 22,667
32,981 -> 32,409
835,421 -> 640,226
267,184 -> 267,600
67,884 -> 67,317
119,182 -> 524,587
790,791 -> 298,299
841,810 -> 156,125
373,106 -> 12,106
130,214 -> 130,281
533,48 -> 675,48
522,724 -> 483,724
497,165 -> 497,814
72,329 -> 72,689
438,596 -> 438,470
422,133 -> 167,133
966,888 -> 80,888
894,151 -> 215,151
586,699 -> 233,699
95,247 -> 114,228
141,845 -> 141,365
252,861 -> 974,139
541,748 -> 541,454
31,114 -> 549,114
846,60 -> 318,60
502,475 -> 502,876
261,374 -> 261,107
155,863 -> 155,982
967,146 -> 902,81
208,955 -> 272,955
876,799 -> 876,30
684,973 -> 684,869
516,685 -> 304,685
473,737 -> 793,737
304,214 -> 656,214
361,755 -> 361,223
565,893 -> 565,124
29,44 -> 776,791
764,344 -> 764,66
294,307 -> 294,805
15,214 -> 15,116
481,76 -> 460,55
418,233 -> 418,808
24,892 -> 895,21
885,843 -> 92,843
109,226 -> 552,226
767,867 -> 767,485
112,900 -> 72,940
910,228 -> 910,35
564,59 -> 564,249
738,954 -> 738,228
551,308 -> 19,840
882,908 -> 267,908
73,790 -> 840,790
538,352 -> 827,63
352,707 -> 547,707
187,478 -> 409,700
840,735 -> 260,155
479,244 -> 479,639
135,370 -> 382,617
345,71 -> 752,478
155,621 -> 973,621
193,215 -> 782,215
493,385 -> 130,748
582,227 -> 627,227
88,789 -> 88,936
916,197 -> 916,360
13,989 -> 989,13
97,708 -> 668,137
601,407 -> 121,407
37,961 -> 985,13
176,260 -> 857,260
10,643 -> 690,643
71,258 -> 302,258
247,848 -> 250,845
933,913 -> 933,446
839,914 -> 674,749
657,683 -> 657,786
217,374 -> 418,575
192,862 -> 931,123
906,813 -> 785,813
312,387 -> 240,387
354,844 -> 132,844
600,104 -> 610,94
603,611 -> 616,624
611,919 -> 773,757
94,54 -> 460,54
494,317 -> 952,317
131,411 -> 587,411
221,776 -> 896,776
577,947 -> 686,838
139,666 -> 139,816
352,331 -> 261,422
63,986 -> 976,73
423,507 -> 898,507
149,914 -> 699,914
70,250 -> 965,250
796,732 -> 206,732
721,750 -> 136,165
987,370 -> 987,677
325,762 -> 325,337
750,767 -> 400,417
298,302 -> 298,135
714,324 -> 270,324
611,91 -> 633,113
43,270 -> 43,735
366,721 -> 158,513
877,976 -> 296,395
435,357 -> 590,357
376,900 -> 376,929
869,962 -> 331,962
42,868 -> 700,210
805,820 -> 805,635
247,709 -> 247,598
887,31 -> 611,31
111,306 -> 769,964
143,592 -> 143,296
264,829 -> 156,829
194,824 -> 933,85
110,942 -> 961,91
498,922 -> 498,226
271,790 -> 927,134
903,69 -> 903,541
879,346 -> 879,286
873,461 -> 873,203
115,678 -> 115,741
854,174 -> 248,780
180,409 -> 180,862
350,564 -> 350,28
380,400 -> 380,522
819,150 -> 31,938
133,615 -> 801,615
975,15 -> 21,969
103,973 -> 851,225
43,112 -> 43,626
689,926 -> 712,903
976,918 -> 284,918
47,405 -> 47,553
618,744 -> 208,744
475,221 -> 475,922
344,300 -> 811,300
27,510 -> 510,510
819,830 -> 871,830
723,326 -> 723,881
652,470 -> 652,497
103,880 -> 610,880
389,681 -> 389,218
717,785 -> 330,398
513,789 -> 381,789
43,130 -> 700,787
970,16 -> 24,962
565,568 -> 708,568
220,198 -> 825,198
24,984 -> 50,984
488,366 -> 292,366
220,137 -> 739,656
⛄"""
