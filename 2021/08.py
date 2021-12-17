#!/usr/bin/env python3

# HELPER FUNCTIONS
import collections
from collections import defaultdict


# INPUT
def parser(text) -> list:
    return [line.split(' | ') for line in text.strip().split('\n')]


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


# just in case
"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""

digit_to_segment = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg'
}

# MAIN FUNCTIONS
len_segment_to_digits = defaultdict(list)
for k in digit_to_segment:
    len_segment_to_digits[len(digit_to_segment[k])].append(k)
# numbers 1, 4, 7, 8 have unique number of segments
unique_len_segments = {k: v[0] for k, v in len_segment_to_digits.items() if len(v) == 1}
assert unique_len_segments == {2: 1, 4: 4, 3: 7, 7: 8}


def part1(messages: list) -> int:
    return sum(1 for line in messages for digit in line[1].split(' ') if len(digit) in unique_len_segments)


# how many times each segment is used in all digits
segment_count = defaultdict(int)
for dig in digit_to_segment.values():
    for segment in dig:
        segment_count[segment] += 1
assert segment_count == {'a': 8, 'b': 6, 'c': 8, 'd': 7, 'e': 4, 'f': 9, 'g': 7}

digit_to_count = {k: sum(segment_count[seg] for seg in v) for k, v in digit_to_segment.items()}
assert digit_to_count == {0: 42, 1: 17, 2: 34, 3: 39, 4: 30, 5: 37, 6: 41, 7: 25, 8: 49, 9: 45}
segment_count_to_digit = {v: k for k, v in digit_to_count.items()}
# each number has a unique value of segment_count
assert segment_count_to_digit == {42: 0, 17: 1, 34: 2, 39: 3, 30: 4, 37: 5, 41: 6, 25: 7, 49: 8, 45: 9}


def part2(messages: list) -> int:
    res = 0
    for line in messages:
        signal_patterns = collections.Counter(line[0])
        num = [segment_count_to_digit[sum(signal_patterns[seg] for seg in dig)] for dig in line[1].split(' ')]
        res += int(''.join(str(n) for n in num))
    return res


# TEST
def test():
    # GIVEN
    given1 = parser("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
    given2 = parser("""
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""")
    assert part1(given1) == 0
    assert part1(given2) == 26
    # part 2
    # 7       5     5     5     3   6      6      4    6      2
    # acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
    # 8       5     2     3     7   9      6      4    0      1    5     3     5     3
    # segment_map = {'acedgfb': 8, 'dab': 7, 'eafb': 4, 'ab': 1}
    """
     dddd
    e    a
    e    a
     ffff
    g    b
    g    b
     cccc
    """
    assert part2(given1) == 5353
    assert part2(given2) == 61229
    return True


if __name__ == '__main__':
    assert test()
    input_ = parser(read_input())
    # ONE #1
    part_1 = part1(input_)
    print(part_1)
    assert part_1 == 397
    # TWO #2
    part_2 = part2(input_)
    print(part_2)
    assert part_2 == 1027422

# INPUT
"""🎅
dacefg fegab de dceb bedag dae bcgaefd bdacg fbgcad bgedca | acfebgd de dbagc deagcb
cfgda fdebgc bfcdeag dbg afgedb efbad bg cdfeab gabdf abeg | dbg fbedgca gbea gbae
dgcbe egdafcb bgcfe dgbf cgbafe db ecbfad deb agcde gdbfec | edb bcefgd gdfb edb
fbgad bgedafc dcageb gcfbed bgdfca ebfag df fdg fcad bcagd | gdecfb dbfgac cgabd fd
bacgd dbceg acedgf dgefb dcfbag cgbead edc ce abce bgecfad | abec gdcfea cbdga agbcde
gcbfde gbdfeca ec afcbge egafb cdagb dbegfa ecaf bcaeg egc | egfcdb cgbdfe ebafgc cdfgeb
fgcab efb afgbed deafbgc efgda dbgfce gbaef be fecdga deab | gfbdec bef agdef dabegf
bcaegfd cbgd gb gfb bgdacf egfbad afdcb baecdf cfagb cagfe | gdcb defacb bg baefdg
fgaecb fbad fgdae bedgacf defgc fa fga adcbeg gdeabf egdba | af agfdbce egcfd cgfed
edfa dfbgac egabcf fbadce bcdaf cea gbfceda ae edacb bgced | ae eac dfae aefd
decafb ae dbecg bdgae edfbgc bafgd egbcad fgcadeb cega eba | aedcbf ea eab gcae
bfcge afdc bgaedc egdfc efcagbd fd dgfbae gfd dcgea defgac | ecdfabg efbgc edcfg gcfbe
cgdfa cdaebg acedf egfc cae cfgdba ce bgfedac efbda dfcgea | afegdc fdeca debgac ace
bcef abgec fabeg afbecg bfagd edbcgfa fe egadfc cagdeb efa | bgcdae gcdabe fgbae fe
dgbaf faecbd cafebdg ade cdbfag ae abgdfe agdbe gecdb gfae | ae aed ebdcg dae
bcgdfa bgaf bcf gabcd cfegadb cdfeg degbca bfcead dcbfg bf | acgbdf gabf bcf fcb
cgdfae gfaebd dgfbca cdg dbgca cg cabde fdbga fcbg cdbfega | eagdfc gc egdcfa cbadfeg
gdea acedfgb de deafc fbdca dfe ecdbgf cfage fceagb daegcf | dfeca edf fde gabfce
abecg efc dgbace edcgabf bafec begf edgfac fe cfdab fcbage | defagc dbcaf begf fe
gdecfa ebafc egbfacd fec fdeb geacb ef cabdgf fbdeac cbdfa | cdafb fegcda fagcbde caefb
efgcd abfgedc cgeb eacdfb cdegbf cgf egadf dbgacf dcbfe cg | gcf fgc bcdefg cbaegdf
baefdg egdfc gebcda dae aegcbfd gbadc dgafbc cabe ae geacd | eadgc ea cdgba ae
ba feadcb bedcfga gacef bac egadcf ebgacf cbfgd ebga afbgc | acbegf gcaebfd cagfb fbgac
afdeg fb defb geabc gacbdf ebgadf bfa dacgfeb bfgea fadecg | gbcae fb faecbgd fgdcae
bgedfca agfcbd cbfeg afde dfbage gacebd aedbg debgf dfb fd | cbgdae efbgd gaefbdc cegbdaf
cbeda fgcead dfe ef ecfg cedaf bfdegac fabgde cagdf fdgcba | fecda dgebfac def gfadbe
fde dgecf begcd gfcbae geacf fd efgbcad cadefg cdfa fdegab | df def dcfaeg gfaebd
agecbd fbdag caebdf gefdabc fagbc cbfea fceg agfbce cg gbc | eagfbc dcaebg cbdeaf gc
dbega gbefa aedcgb cebdg dcea ad gda cebdfga gfbced bcafgd | gad cdeabg gda aedc
ebfgac cdbegaf facged dge caegbd gbeda agcbe de dbfga ecbd | dbce dge dcefag defbgac
dfabce dacbeg gfbed bcgeaf afebd fdac debca egdabcf fa afb | abcde cbdaef gabecd dfgbe
cgb fcdab fgeabc bedcgf dceg gcbfd cg defbg bfgdae gcfdeab | gced gdabcfe bdcgf bfagcde
dgcb cdafb bgafd cgfdab adgcfbe cfdae agcfbe cb cab adebgf | dacef baedcgf cdefa cbdaf
ebagcf bgaf gabec daefcgb gcefb fabdce begdca cfb fb defcg | edagbc bfgce bdeacf eabfdgc
eadbcgf bcd befcd fcegd bd agcbfd cbefa fcbeda cafgbe ebda | bdacef efcabdg db dbae
gdecf acfedb fgac degcb gfdea abdfeg fc cfdage fec bdafgce | gcfed fgca cf agfc
bafecg gefac cegfb cea efba dcgbfe dbecga gadfc cbadefg ea | gfcae ea gefcbd afegc
bafe ba dbcae fgcabde bda ebcfdg gcdae gabfdc bcfed fedacb | adegcbf abd eacfgdb cfadgb
afcd geadb bcaedgf acfgb fgdabc cdbefg fbd gdfba fd egfcab | gdeba cdaf gcfba fcdgba
edbgfac bceg fagedb ebfca eb cdeaf gdcfab gcbfea fcbga bea | bedcafg eb abe adecf
cbdfge gabfce edabc bdfcag bcfdg gdef fce fe gbedacf bedcf | ef defg ecf cdbgaf
bafge de ebcdgf dbega bde cadebfg cagfbe acdgb efad gdfabe | decbgfa bfgae gdeacbf ceafgb
cgfdeb adfegc dce ce fgcdb cgdafb cdefgba cdebf gbec dafbe | ce egdfca ec fabde
eabcgf fcgbed bfaedc cabfedg fd gcdfe cdeag fcgbe gdfb def | fde df gfbd efd
aed ebfa gdefab bgfda dacgfb cdgfae ea bgaed debcg gefadbc | bdgfcae dfbga gdebc bfedag
eafdb ceadf fac ebacfg ecdabf fdcabge badc egfadb ca ecgfd | eacdf gfdce bcda cfa
adgecb cf cagf cfdgab abfdc cbf dfagbec cadgb fcgdbe adefb | dbcfa fabdc cfga bcdaeg
bgdcfa fdc bfcaeg gfdea dc gacdfbe fadgc fgbca fbceda bgdc | cd cabgf bcagfd acgfd
defbc gcfbae efg aedg eg cgfbdae cgefd daefgc bafdcg fadgc | gfe gcdfa gfdcba befcgad
bfgeca gcade bec begac afcgbd beaf cgabf be fecdbg deabgfc | eb cbe efgbcd afbe
ebfcd dce fadceb cd gdbafe fedab aedgfc dfbgcae acbd efbcg | edcfb bdaefgc cbegf cefbd
fgbc egcfda bga abcedg cabfgd dbefa abgfd bg dacfg cfdgeba | fcgb aefdb eafcgd agdecbf
dcega dacgbef gbadc dcafeg gdebaf ead ae gbfced faec efdgc | cegfadb acdeg ae dgecf
afgcb adebcg bgdec bcgea dacbefg aeb febcgd egda ae defcba | edcafb gfdceab ea gabfedc
adcge bge agbfcde eafdcb facgeb aecgb gabf fdcegb acebf bg | dcbefg gabcef cbfdge gfcbed
cebdag ace gfdbec gcebd agcde gfacd ae aebg defcab gbdafec | ea fbedcg dbgce eadgfcb
bdaegc eabgcf bgfae bfcag edcbgfa ebg eb geafd gcabfd cbfe | aefgb bge be ebafgdc
cbedgf eabfc gacf gfe bedag gefbcda cedbfa fcbeag fegab fg | fabeg bcefgd fg egfabdc
bdce dfcebg cbf fbgcea bc edcafg dcegf bfgeacd cdbfg adgfb | bfc acbgfe edgfc gfcbd
cedafg ae gfbed eaf dace gdfac dgcbaf caebfgd faegd eabcfg | aedfcg dfgbe ae edbgf
fgcde cdebg cfage dbcf gafdeb baegdc df gcbdfe fed dacgbfe | fd dfe debgc geacf
ed deb dabgf gade aegdfcb cefba abefd dfcgeb bfdagc afdegb | dbe gbadfe gdea de
gbadc gde agced ecagdb ge ecgbdaf cebdgf aebg fadec bacgdf | gde adbgcf aefcbdg cbagd
eadgc gae geadfc cafe ae gdcfa cgebd bcfadg bcdegaf befgda | ecadfg fadgc gedbc gaecfdb
geca ac abgfedc edfcg fdgbce eadcf fagbdc feadb fdeagc afc | dbfea efacd egca cgbadf
fbdca ebcdaf feca fcgbde fba dfeabg gcdab fcebd gefadbc af | dbacf dfecb af bcdag
bfdegc afdgec defgab fcade fdc ebcad cf fbgecad gadef acfg | dcf gfac fcd cgaf
dgfbc badefc cbe aebf dgeabc eb cadef fabedcg ebdfc gdecfa | be dcfbg afced ebgfadc
dfcg degfab dg gcdea cgbefda deacf bceag afdcbe agd edacfg | faedbg gebafd afecd dcaef
fdbe cfeabdg acfbde df dagecf dfabc cagbd fad egfcab efcba | cbfda efbdac bfdca fd
aefdcg bgcda cgedbf eb gdcbaef bdeag geabfd aedfg bge fabe | fgcebd geb ebfa fadegb
aedb dbfca caebf adf ad gbcafed bcdeaf ebcgfa acgedf cfdgb | acefb daf aedb fbcad
ecgdabf fdcge begfca bg dabfec bgfdca abgd bcfda cdfbg cbg | agdb cagefbd cfgdb afdebc
cga ecadfgb gfcd gc fagcbe aedgcf dgfabe bedac fadeg cadeg | gdfc cdgf gcbfae fdgc
ga acdg egfbcd fegcad aeg dbafe fdage eabfcg degfc dafbegc | cdgfbe fegda fbade fcbdage
agdfe dgcaef eb fcdbgae gcdbf deafgb bgfeca bfe egdbf bdea | ebf ebf abde bdgfe
agbef egdf baegdf cdfbag df ebcad bafecgd fedab afd acfbeg | fd decab bedfa feabd
dabcfge ab abge acfeb fdecb bac aebfgc cgdbaf aefgc cadgef | bca fbecga ebcfd ba
feagcb cgdbfe cefdbag dg gdabec dcg ecbga ecdga dgab ecfda | dgc cabegd bdga gebcad
dbfaec gac cgdeab efgcd dfagbce cfabe ag acbgef afegc afbg | ga acebdg bcdefa ag
aegcbd cgfba gbdafce agcdb bfg afgbdc fg fgabed bcefa cdfg | bfg bafgdc dgcf bgf
edcbf gceafd dfbaeg cgefba dafeg daecf aec agdc bfadcge ac | cfbedag eac febdc dagbef
fgadcbe daecg abfd af afg bgfcae fabged gedfa dbefg bgedfc | afg gaf dgfbe gacebf
fgbca cdbfa fgedac cfegb ag agbfdc bgfaedc gac acebfd gabd | dfeacb acg cfdagb eadcbf
fcgeabd beac cfgdba cgfeda bfcdea bfa gefbd ab bfdae dceaf | ab bfdge fdecag dcefab
dafeg bdefac gcebaf gcfbed fdcea cd aecfb dcf ecgbadf acdb | eafgd dfeca acbd egbfdc
cdgfe egc abdefg agfc adecbgf aefdg gc gecdab ebfcd efcdag | gdecf cbefd gecfd gbdafe
edbf fdgbac bcd ecbda bfcead dafcbeg cfeba egbcfa db eagdc | ecdfabg faecb bcdea abfcde
ecfag fcdba cbg adegcf bgef badcge ecafbdg gb fgacb cfbeag | cbg bacfd gacefb cfbga
gafed gbefca bfe badcfge fb dcebga abegc gfabe abcf edbcfg | afbc feb cebga afbc
fedga ecbdgf acef degba dfabgce cdfaeg cgdfe acbfdg af daf | fda gdefac eadfgbc bfeacgd
cd cfd afcged eacfg dfegb cfdeba dagc ecgbaf efdgc cegfadb | cgda fgdbe dcf cfaeg
bdfceg aefgcd bgade gbf acfb bgcadf gfacd bf fdgbace gfbad | bf efgcda ecgdfb dfgace
abecg fdaegcb acdgb cbde edacgf gbdace ec aec cgfdab fbgae | gacedfb eagdfc gaedfc bdcgea
gf cbfeag ebcag bdacge cafed ebgafdc gcabfd begf afg gfcae | fbeg facbdg bgecdaf dcgefba
gfcda gcaefb ad cfedga adc daeg fecbagd dabefc cfbdg gfeac | ad ecafg cdfeag cdbfg
cdbfg deb ebgfd bgfdce cfbgda dcef egfab edbcga gacfbed ed | efdgb fgbcd gcadfeb fdce
fbcaed bgcf fbgdcea gbaec fdebga geb gb caegd cbafe gaebfc | cfgb egb gb dcbfaeg
bged fgdbc ebfcad efacg fed dcgafb dbgcef cgdef cebadgf de | fcdeg gdeb ecfgd gcbedf
adebgf agefd abdgcf dg acfde gaecfbd egbd agd efgab cfebag | fcebagd dagbcf gefda adg
ae fbdea defgb bfecgd bgedcfa eadgfb ebdacg fadbc eab egaf | gfedbc acebgdf bcgade bdgfec
adbfc eacbf abgcef dgfcea eaf faecgbd efgbc dfecgb ae gbae | gafdce gbea ea cdbgfe
cdefg ecbafg fgda cfgea cafbegd acdebg dfceag gd ecdbf cgd | efdcg agfd ecfdg dg
cbdeafg ed bafgde efcd dabfc dfcabe ecdba ead cbeag bagcfd | de cabfed ade eda
dbefagc dfgacb cfegbd fbgdc gbe edbc degfa efbacg eb gebdf | fagbcd bcfdg gbfcad dbce
bfdce de dgaebcf begcf acfdb ecgbfa cedg fbedcg afedgb bed | cbefd fdgbae de bde
ca ace cbdega ecgfd eagbfd acbg bcafde dcgfbea aedgb agecd | ca eca acgb adgce
bc cgb acfb dbcgfea bdecgf gfadbe abgfd eacdg fbcdag bdgac | fcegbd bcg cbedfg badgcfe
ag gbefac cdebg bdceaf cdbfaeg gcadfb gaceb gab agef cabfe | fcgadbe cagfedb ebfacd ga
fg gaced gdcafb egacf cbafge fgdabce fbge bfaced cabfe gcf | beafcd eafgc bfcea bgcedaf
eafdc cedbfa dcaegf fcg fcbega ecfgd bgcdfea afgd fg ecdbg | facged fg ecfda dgfa
fb badcg eadgfb bdgeac fdbcg bfg fcdagb bgcdefa efgdc abcf | bgf bf gaedfb bcaf
dbcag da bgdce afcd gacdbfe cagfb gabcfe adg cbdagf begdaf | da cgdba bagfec da
dgcbf cfbe egf ecdgfa bcedgf adbcfge degab fe bedgf cfdbga | fcdgbe agdcfb fe fe
dacegbf afgec fgbdec degfa eacfgd gdbfae gec gc efcba gcda | dbagef cdbgef dfaceg degcfba
ecbdf gfced bcaf fabgecd egbcda gfbade bc bce cbeadf debaf | bdface afdgbec cb aefgbd
gefab cafdge db edfgc bcgd fegbd cabedf cabefgd cbedfg bed | bgcd fcdeg gafbedc fcbgeda
cdbgfe gadcb afbdeg gfdbc gedfb dcfgea fbagdec befc cf dfc | bfdge acgebdf cdf decbfg
egdc fgcbae cbg adbgc gbcdeaf cg aedfgb bdafc ebdag abecdg | daebgc gbdeca gc gdabce
fdb fbacgde befda fb bfec cdgaeb aedcb afbcde agcdbf fegda | bfd fdb bcfaed eafgd
eagfc dgba faged gdf gadfcbe dg dafeb cedfgb ebadgf edabcf | egadfb agbd bagd badgfe
cgdbfe cfdabeg fcdbga edabg af bdecaf aecf daf fdbea cebfd | af af af ecaf
cdgabe dafegbc gbedc cbaed gbe ecdfg bg gdab baegcf deafbc | bg bge cebgafd dabg
ef afe facbged adcfg cfebad dgef gfcdba acdgef fgeac aebgc | badecf dfge gdacf gedf
fedcbg gcdb gbecf dbagef fdb cabgedf aecgfb dfceb adecf bd | cgeabf egfcb db fbecga
ceadgb fadbe fdbgea ac cdfa afdegcb abcef ecfbad eac cbefg | fabde ac bafcde abdfe
dcg dgfab beadc fgac dcgefb dafbgec agdcb cg facdbg afgbde | gdc cfga dgfebac adebc
ecgab eacbf acf dafbe edbgca gedfcba caefbg cf fcgb fcdgea | fbdaecg gdeabc cfa gbfc
acgbf cedbg cfebg fecagb fcgeda ef gfe befa fagecdb gfcadb | egbfc gedcfa egdcb egcbd
abecd bf acfegd dafcb cfb gcafdb fbgd cgfad befcdag fgeabc | bfc dfagce cfdba acebfdg
gdf egabfc ebgfa gaedfb acbfd agde fbeadgc gbdcfe gabdf gd | agbcef fbgdace gfd gd
bdge ge fcdgeba gaceb cdabef bcfga aegfcd egc bdcage adecb | eg dbfgcea ge ceg
gefbd gce cedf becgfa acbdg bgcfde bcedg egbadf ce gacbefd | gbfde ecagbfd cge cdef
fed dfbegca gdaec abdgce fgedac ef afcdb faeg ecbgfd dface | dfagec gefa cebagd faeg
acbfd facbdg badgcef ecb fdegb cdea bdfce cbfade ec afbgce | bagecf ebc dcbfe efcabdg
be cdgeaf bfcgd gcfabed gcabed abgedf bdgce aecgd caeb edb | gdfcb eadcg gabdce ebd
bfegcad abdgc cebdag cg caeg cfdebg gcb degbaf adegb dcafb | bgc aceg cabdge debfgac
eg fcbae fgabe fgcade gbfad dgbe edacbgf fgdbac fge dfeagb | gadbf abdgf gadbef fabeg
aegfcd eba fbacd be ecgb aegcd cdgeba aedcb agcebdf fgedab | ebgadc dfagbec cdgae bdfeagc
fcdgeab aef bedfag fbadc gaebdc dgaecf feacd fe egcf dcgae | gaced fe ecdgab bfdca
egdba baecfgd debcaf gb gcfbed gecda fdgbea bgaf bdfae egb | gfdeab gb gbe ecgda
ecgab adbceg cegfbd ceg gacd ecgbdaf fgeba acbde cdfabe cg | dabecf cgbdea fdabecg bfaecgd
fcbg egdaf dbecfa abgec feb begadc eagcfb gbefa cgfdeba fb | fedga dfbceag cegafb efb
fe agdbcfe eafgdb fae dceabg eafgcb fcadb agedb dafeb fgde | fdeg adcgeb fe deabcgf
ebfgd ad abdgf ebcgfa fdaebc dba cadegfb gcda bafdcg cabgf | gdfab cbdgaf abgfc fagdb
eadgfc gdbfca fgcbaed bcdg cg cgf gdbfa egfbda fcabe cbfga | gc gabfd fcg afecb
acbefgd fgcdab bcga fgdbc fdabe fdbceg acd fcbad eafdcg ac | ca aebcfgd cfbdg cbga
beacfg ecafgd fdcbg fd gcbfe dcf efdb fcgdaeb adgcb ebdgcf | fecagbd dabcg fd fd
ecfga fcdbae afgebc egdfa cae fcgedba bgac ca bfceg cdfbeg | agdfe gcebf afegc bacgfe
cafebd gfebca dceaf eabfc efbagd faedgbc abdc adf ad fcgde | cbad badc gcefd cbegfa
fgdbc beca adc cbgead bdgae cfagde dfgecab gcdab afbedg ca | agbefd ac dac abce
ecbdaf geadbc cfdbe fcdgabe adfcg ge ceg gcdef fegb fbcegd | cfdabe gdfce ecbfd ge
baegfd cadgb gdcfb agec dcgaefb bcagde edgab acb ac ebfdac | agdbef bdaecf ac egca
dbaec eadcg ga gadceb gcedf cga ecbfagd acbdgf bgea eafbcd | daegc ag cga afcgbd
daefbc bdeacg bacdg gdcfe egab becdg bce acdebfg fbadgc be | cagbed ebcadg aecbgd dbgafce
bfedagc gbafcd fead eafgc ef cfadg edfcga fce dgcbfe caebg | ef fcadg ef edaf
fadgce egc fegda dafgbe dcabg gceda ce gcfbdea agbfce defc | egacd gecadf febcgda abcgd
egcdf cagedf bacef bdcgefa bd cbfdga ebdcf fbd bdefgc gdbe | becaf efbdagc cdaebgf cfbed
faebd ebdfga fagced fe gbfad dcbfga eaf egfb cgedafb ebacd | eaf efgb baecd efa
bdega edaf fabdge fe dfebg cgefab gfbdc dcabge gcedbfa fge | cegbda defa feg agbed
gdecaf defbg acgdeb badc gcaed fbaceg afdebgc ebc cb gdbce | cb bdceag bc dcbge
bgfc agdefc dgabcef fegca eadcb bg gbfdae gbe cagbe cefagb | gb ceafg bcega gb
cgb cg efabc dbaecfg cbedfg bcefg ebagdf gfdc debgf deabcg | fgbed ebgcad fedgcab cgbfe
fecad egdfbc gadcfe eagfc aebcg fdag feg fecdab aedbgfc gf | gfe dfag cgbdfe gfcdeb
gadfce bcadegf fcged cafbg bd dcgbfe dgb dbec dgbfc beagdf | bgd cgfbde bcfga gfdbc
gdecbf efg fbcgae cfeadbg geab cagef gadfc eg bafedc cafeb | egf fgaec becfa gcefa
bcf eadcbf dcfeb cegbd bfea gdcafb efcad cadefg gfbeacd fb | fb cfgaed eabf afebcd
ebcdag bgaefdc aegf eg fgebc dbecaf abcef beg cbafeg fbgcd | afecbg feag efag bdfcea
cadfbe cgba cb cgadfe acgdf fbdcg bcf fcabegd fedbg gbafdc | eadgbfc faegcd bfc cabg
bcgefd fcabg dafgcb cadfe fadcb dbf bd gcdebfa cfgabe dagb | cadfb eabcfg gbafce gcabdf
dcegfb efadbc fceabgd dcab db beafc abefgc agdfe fbaed bdf | dcegafb dfb bfd fbd
abe be faced fegb cabedg dfabe adfbge cfaebdg gbdaf fcgbda | eagdfcb egadfbc adfebg agfbd
cgaefdb cedgfb dcfbe gef gabfde fbagc fgbec gcde ge bdafce | dafecb ge gfe efg
edgaf defbagc edcbfa cd cbgd cegad cde afegbc gcebda abegc | badcfeg cde fadge fbdcae
abgfec abfe acf ceagf baecdg dfecabg fa afgdbc agbec dfgec | acf fa af afceg
ebgfda deafbc bcedg adcgbf fagdb afcg gdbfc fdc cf fdgaceb | feacdb fcag fcd dbefac
gdfba de dbgefc ecdf dceagb dgefb cbgfe dbe gabfced ecgfba | efdgb feacgb egabfcd gfbde
fgad gac bgcfae dgcfbae ga dfgcb begdcf abgcd cdeba bafgdc | agdf ag cdgfb ag
efbcd efda fdbacg fe bdcaf feb gdcbe bgaecf dcfbgea fcbeda | fe ef becgd cebgd
dgefbac de decb abfdg dacegf gde cbegf efbgd gfbdec cafebg | fecgab dbec de dafgb
gec bdcfea gbdfe gc fdabgec bgedac adbec agbc ebgdc afgcde | cagb gecabd bfedac abcg
cf cgdea cdgfe egdfb dcf dafcbg fbce eagfdb dcfegb bdcgeaf | fceb fdc fcbe efcb
bcdga cgb bacf gcafdb cfgbade baegd bdcfeg cdafg gaecfd bc | dbgae gbcfda acgdb fbac
fgcdae geacfb gd cdefb dbfgea bdga defgbac fgd febga gfbed | gfd ebcfag dfgbe dbag
bdeag fedab cafgeb gb decbag gbe bgcd dcgea fgdcae ceagfbd | cfgebda ebg cfaegdb gdbc
fdebac cb bface agbcfde befcgd ecb dacb efcad bagef caefgd | eadbgfc dbac ecb egfab
bdcea cbgfead dfc ecfb efgdac fc bfdac edbcaf dfbag cgdaeb | fc edbgacf cf dagecf
bdgfca abegfdc fdg abfceg dafbge gacde agcdf fdcb df bagcf | fbcga ecgabf bcfd df
befcadg ce bdfgce cbed fce fecgb gefacd bafeg gfdcb gbafcd | ebdc bgfce gfedca ecbd
fbgce abgefd ecdfga abfc efcgba bdecagf abfeg dbgce cf cfe | fec bgdaef bcfge ebdfcga
cgfdba dbcegf gac fadeg ca fcab gdaceb dafgc bdgfeca gdbfc | adcfbge gdfca ecgabd ebadcg
dcaebf gfdceab bd ecbgd egacb cedgf bed dfgb fgadce ecfgdb | bgdcfe cdebg gebdc dbe
dcbae aecgbd daebcf cbefag adgc ag dabeg aedgbcf gea egbfd | badcefg gefdb dacbe dgac
fgcdbae cagfd de eagcbf cbaedf gebd edf dgecf cgbdfe ecfbg | afcdeb fed dbeg efd
adbec bdecfg adbcegf fd ebfcd gdbaef efd cbfgea cdgf cfbeg | befgc ebdfc gcbfe bgefc
fadbg aebgfcd edgafc ebdfac dbe efcad be agcdbe fceb dfbae | agcdeb bfec fceb cbef
fcged gfbdec adebf adc cage adbefcg caefd ac cbfagd efagcd | ecgafbd dac ca gfcbed
gcdba fecgd gfdceb dgeabf af facgd feca aegfdc ecabfdg dfa | fcdga adbgef cadbfge daf
afdec faebc bdea fgbcad efdgca ba egdbfac fcegb cba acfebd | cebfda bdae adeb abde
defgca efgbadc ecgba gecbfd db dabegf aebdg gdfae deb adfb | dcgaef edb bed becgdfa
⛄"""
