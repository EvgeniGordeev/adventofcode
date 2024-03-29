#!/usr/bin/env python3

# HELPER FUNCTIONS
from collections import defaultdict, namedtuple

Model = namedtuple("Model", "allergens potentials counter")


def parser(text) -> list:
    lines = [line.split(" (contains ") for line in text.strip().split('\n')]
    return [(ingredients.split(" "), allergens[:-1].split(", ")) for ingredients, allergens in lines]


def read_input() -> str:
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return data


# MAIN FUNCTIONS
def identify_allergens(lines) -> Model:
    potentials, allergens, counter = defaultdict(list), set(), defaultdict(int)
    # create a model of potential allergens and known ingredients
    for ings, allers in lines:
        allergens.update(allers)
        for a in allers:
            potentials[a].append(set(ings))
        for ingredient in ings:
            counter[ingredient] += 1
    # find ingredients for each allergen that are common in every line
    for key, sets in potentials.items():
        potentials[key] = sets[0].intersection(*sets[1:])
    return Model(allergens, potentials, counter)


def part1(lines) -> int:
    model = identify_allergens(lines)
    bad_ingredients = {ing for ings in model.potentials.values() for ing in ings}
    return sum(v for k, v in model.counter.items() if k not in bad_ingredients)


def part2(lines) -> str:
    _, potentials, _ = identify_allergens(lines)
    # sort by set length
    assumed_allergens = {k: v for k, v in sorted(potentials.items(), key=lambda item: len(item[1]))}
    allergens_by_ingredient, identified_ingrs = dict(), set()
    while len(assumed_allergens) > 0:
        keys = list(assumed_allergens.keys())
        for allergen in keys:
            bad_ingr = assumed_allergens[allergen] - identified_ingrs
            if len(bad_ingr) == 1:
                bad_ingr = next(iter(bad_ingr))
                allergens_by_ingredient[bad_ingr] = allergen
                identified_ingrs.add(bad_ingr)
                assumed_allergens.pop(allergen)
            else:
                assumed_allergens = {k: {v for v in _set if v not in identified_ingrs} for k, _set in assumed_allergens.items()}
                assumed_allergens = {k: v for k, v in sorted(assumed_allergens.items(), key=lambda item: len(item[1]))}
                break

    allergens_by_ingredient = {k: v for k, v in sorted(allergens_by_ingredient.items(), key=lambda item: item[1])}
    canonical_dangerous_ingredient_list = ",".join(allergens_by_ingredient.keys())
    return canonical_dangerous_ingredient_list


# TEST
def test() -> bool:
    given = parser("""
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""")
    assert part1(given) == 5
    assert part2(given) == 'mxmxvkd,sqjhc,fvjkl'
    return True


if __name__ == '__main__':
    assert test()

    input = parser(read_input())
    # ONE #1
    part_1 = part1(input)
    print(part_1)
    assert part_1 == 2072
    # # # TWO #2
    part_2 = part2(input)
    print(part_2)
    # assert part_2 == 85660197232452

# INPUT
"""🎅
xnjhn pgmj lclnj qgnpkp vpfstj ffdsnc mnpfcx tkccrc lkv cgdx rmfmm grjrrm frq lvzjpn vntgs cbzcgvc mnnzf rfdm vxrdlb dvmzkk vpsmz sfp kltxt sxbr dlrpp pqrvc lpqxmc kfgln zzvhml prgnr svpfz scfhknrs nvzjxr tpv jmvxx nxkpfqtg lgtpk vcrs pqqks dxxmnr jlxqpjd qp mjhdfg vbbk qtsjztd tnfgxsn zhxh rrmvn tnn gdfddn jx tbv vnddzb (contains soy, peanuts, sesame)
lclnj gsbdgk pcgr lsntrr fbcnsr pgckbv tpfjxp cbzcgvc vpmzl vxrdlb qmq fjlhvt bljlvc jfpttz vhxjc tsdz lsx llpvqk vbbk tbrdjm vlbdl mmvgjk pxtg jts nvqgxc lkv qp psrnxh fdsfpg djrbkjr lkgjp ffqpqck vhsh jdfcj lfqpqc zqr qthz prcft nhnnc xmnscmnv qqdxk zvqg mjhdfg flfn fvd qqsr gdgdd dxxmnr vnddzb fnvjz mzsb pqrvc ghkptm krg pqqks dcxcc kltxt hqtdss jx bbsnzc prcbf dcrtvq grjrrm kfgln xgqfzp gmmtk jzfz xtdrm (contains wheat)
jlxqpjd fdsfpg jgdxt mjhdfg pqrvc qtsjztd vntgs ktfzfj prgnr cbzcgvc lfq pxtg psrnxh nhlrh pzxlmn lkv zpn xtpvjscp kfgln tsdz jmvxx jvx kltxt qntgqv vpfstj prcbf gmmtk ndfq pqqks tsgvdsj qlcd sfp xbj dcfzd tktff fnvjz cgdx mfl zttgff tkccrc tpjf xnjhn nbgl tpfjxp rzjcr jjjn tnfgxsn qdxnn rrmvn vbbk djrbkjr vxrdlb hvhsn qrdq qltxnk (contains dairy, peanuts, shellfish)
nxkpfqtg vppmgd lclnj kfgln mrj flfn bvn glbpt jx qqdxk ghkptm tpfjxp qlcd tbrdjm jlxqpjd stvl bbsnzc prcft pxtg cpjmc jmvxx zrxbmt zttnb svpfz gppn vvgcfr gdgdd hqtdss lgtpk pqqks vhsh nbgl vxn rfqxzg cbpt tsgvdsj zzvhml dcrtvq zqr lpqxmc vxrdlb mfl msqtqc fdsfpg rdpzthm ktfzfj jts qnsl vpmzl sgfvv xmnscmnv jzfz lsntrr cbzcgvc pgmj lfqpqc xtpvjscp rjj tffgpr vnddzb kmzrf qnjbl cpnxdkk sfp dcvrc ffqpqck prcbf krg psrnxh gffjlg frq qgnpkp qhpds rrmvn hdqdqbm qltxnk lxrtk fvd zhxh vhxjc xzkgmj lkv xtdrm pvpbdk (contains eggs, sesame)
zvqg zttnb stvl mfl lxrtk dcxcc rmfmm prcbf jmvxx fbcnsr jztckz qrdq mrj qmmzr gdgdd hqtdss vhxjc lgtpk xgqfzp lclnj prgnr ndfq xbf fdsfpg cbzcgvc hdqdqbm djrbkjr tsdz kpsp cpjmc qtsjztd vqmqqr mpklvq mnpfcx xf xnjhn jlxqpjd jvx rjj kfgln jx qmq nvp tkccrc cbpt vnddzb jzfz lkv lvzjpn gppn pqqks ffdsnc lfq mmvgjk nxkpfqtg (contains fish, dairy, eggs)
nvzjxr jrmnf ndfq jxdcgp cdkx fdsfpg frq cbzcgvc zttnb mzsb rmfmm ghkptm vbbk zvqg hlkqpp jzfz tnrkjkr rdpzthm jztckz vnddzb hvhsn stvl xf kpsp flfn lclnj tpfjxp qrdq cpjmc lxrtk gjcnhb nhnnc lvzjpn djrbkjr gppn cpnxdkk prgnr kxsftq vshth kltxt jhvbj jmvxx pqrvc kfgln pxtg fnvjz vppmgd krg vhxjc qnsl qntgqv fzccd vpsmz gmmtk sclxx dxxmnr vpmzl qp tpjf dzvsv dcvrc sxbr rjj xmcs dvmzkk nhlrh vxn pgckbv jgdxt xjvc dgnvz jvx xmnscmnv lkv xbj kc zpn bvn (contains eggs, sesame)
xmcs sxbr lclnj xnjhn cpnxdkk fbcnsr lvzjpn vntgs vvgcfr vlbdl pqqks mzsb tbrdjm lnfvdxb tnn jgdxt hvhsn tffgpr tfdfqp qhpds chtd lfq frq sclxx qthz pqrvc pxtg jvx pcgr ffdsnc bfrtj qntgqv jmvxx lkv lsntrr cbzcgvc ghkptm prcft fdsfpg kmzrf gjcnhb vpmzl vppmgd (contains soy, fish)
zvqg xmcs vhsh cdkx kpsp cbzcgvc jbt prgnr sclxx nhnnc kfgln zzvhml lfqpqc cpnxdkk tpfjxp fbcnsr kxsftq zvdqv fdsfpg zqr nhlrh flfn lkv tffgpr vxn vvgcfr lpqxmc cpjmc pqrvc zttnb dcxcc lkgjp jjjn mtkgvt pqqks jmvxx xf jztckz ffqpqck tsdz dxxmnr mmvgjk vnddzb sxbr qtsjztd nnlmz zpn sgfvv vhxjc qgnpkp djrbkjr (contains fish, eggs, peanuts)
fvd tsgvdsj dcrtvq gmmtk tpfjxp xmnscmnv vpfstj lfqpqc qntgqv vshth rrmvn jmvxx rzjcr qmq tffgpr qtsjztd qnjbl pgckbv tktff kpsp mzsb glbpt jrmnf jfpttz sfp jdfcj cbzcgvc ljnk fbcnsr lkv jts qp rjj ktfzfj msqtqc dgnvz fjlhvt vntgs trvjv vlbdl srckbnq xjvc mjhdfg zrxbmt qrdq flfn xbf vxrdlb xf stvl vbbk pqqks dxxmnr zpn pxtg svpfz fdsfpg tfdfqp lkgjp lclnj nxkpfqtg nkktc dcvrc lsntrr cgdx pqrvc prgnr bvn kltxt mnnzf mpklvq qtbtcv pvpbdk (contains wheat, soy, dairy)
jvx vsskb bbsnzc xtpvjscp xgqfzp mrj psrnxh xbj fdsfpg qqsr lxrtk qqdxk lnfvdxb sxbr msqtqc mnnzf lpqxmc qlcd sgfvv vpfstj lfqpqc llpvqk jmvxx ljnk zqr lkv hqtdss fvd prgnr cpjmc lsx xjvc jfpttz vppmgd grjrrm lkgjp ndfq vhsh kfgln pqqks qgnpkp jdfcj mfl pqrvc lgtpk kc jjjn gmmtk tnfgxsn tnrkjkr gjcnhb rjj vcrs nkktc cbzcgvc nbgl vhxjc (contains soy, fish, dairy)
gdgdd nbgl lkgjp cpnxdkk stvl cgdx nxkpfqtg tpv lxrtk tktff kltxt jbt xgqfzp jmvxx tffgpr tnn dcxcc cbzcgvc sgfvv vnddzb gppn sfp zvqg vpmzl mfl hdqdqbm qqsr pcgr mjhdfg qtsjztd gffjlg tpfjxp pqqks pxtg dvmzkk zrxbmt xtpvjscp kfgln lkv lclnj psrnxh pgmj fnvjz qmmzr bfrtj rfqxzg pqrvc nnlmz sclxx dcrtvq qltxnk lfq (contains peanuts, eggs, fish)
nhlrh jts cbzcgvc jztckz nvzjxr xbj zvdqv cbpt nnlmz qqdxk nhnnc jxdcgp mtkgvt pgmj tffgpr jbt qtsjztd xbf pqrvc lkv vvgcfr lfq jvx cpjmc vqmqqr chtd ffdsnc nzhsjkt qthz qhpds pqqks tkccrc tsgvdsj zhxh vppmgd fjlhvt qmmzr lclnj mfl qrdq kfgln qdxnn tpfjxp rrmvn trvjv dgnvz rdpzthm dvmzkk xgqfzp kpsp lpqxmc sxbr lfqpqc bfrtj gsbdgk bvn xtpvjscp flfn xnjhn rjj rfdm jlxqpjd lkgjp glbpt jmvxx qtbtcv fzccd qp tsdz tpjf qnjbl frq tfdfqp lxrtk ktfzfj mjhdfg (contains soy, eggs, fish)
jdfcj lxrtk nvp dcfzd tbv lsntrr pqrvc vlbdl dlrpp nkktc vpsmz jjjn cpnxdkk xmnscmnv fbcnsr cbzcgvc frq kfgln ffdsnc hvhsn mpklvq lfq fzccd kxsftq fdsfpg bbsnzc cpjmc vqmqqr jbt vhsh cbpt jmvxx gdgdd zvqg lsx vbbk lkgjp nvzjxr fnvjz dzvsv qhpds lvzjpn nvqgxc jfpttz qtbtcv gsbdgk nhnnc lclnj djrbkjr xnjhn qrdq hqtdss xtpvjscp jts pqqks mmvgjk dcvrc tsgvdsj zpn vshth (contains eggs)
bbsnzc vvgcfr ljnk bfrtj zttgff xbf fjlhvt kpsp glbpt xmcs lkv pgmj qgnpkp gsbdgk lclnj jlxqpjd tnrkjkr dzvsv dxxmnr xjvc xtpvjscp nvqgxc qdxnn srckbnq mpklvq kfgln pcgr rrmvn gffjlg tktff fdsfpg mfl mrj hvhsn pqrvc mnnzf xgqfzp vhxjc vlbdl jmvxx tnfgxsn psrnxh tffgpr qthz hdqdqbm nvp nnlmz qltxnk dcfzd qmq jgdxt gppn ndfq chtd cgdx tpfjxp xnjhn rfqxzg vppmgd rzjcr zqr jbt lsntrr xzkgmj cbzcgvc (contains soy)
nhnnc xtdrm cgdx vpmzl kpsp qtbtcv kfgln mpklvq lclnj mtkgvt trvjv xmnscmnv nzhsjkt fzccd lpqxmc llpvqk lvzjpn bfrtj hvhsn ndfq sgfvv jgdxt gppn rfqxzg qmq pgckbv rfdm fvd nkktc hlkqpp vpfstj xf rjj tnfgxsn glbpt jfpttz bvn lkv qntgqv gmmtk tpjf ffdsnc jts mnpfcx krg lgtpk dgnvz qthz vntgs rdpzthm vsskb lsx cbzcgvc tffgpr tbrdjm vnddzb fdsfpg ghkptm zvqg zvdqv msqtqc lkgjp jmvxx jjjn pcgr dcxcc jztckz pqrvc cpnxdkk (contains soy)
lsx vxrdlb sxbr pqqks qmmzr kxsftq cdkx rfdm vbbk tsdz xf vpmzl fnvjz zttgff xzkgmj vshth nzhsjkt kltxt gsbdgk chtd lkv fvd qnjbl hvhsn vlbdl jmvxx zvdqv pgmj kfgln svpfz nkktc xmnscmnv rdpzthm rmfmm ghkptm tnfgxsn vhxjc pqrvc vcrs jts xjvc cbzcgvc mzsb fdsfpg pvpbdk bljlvc lfq xgqfzp dlrpp prcbf jxdcgp (contains shellfish, eggs, dairy)
psrnxh pqqks xbf xjvc nhlrh vxn pcgr srckbnq zttnb tktff sgfvv fbcnsr qntgqv lsx dcrtvq cbzcgvc qmq jmvxx qlcd nvqgxc rmfmm pzxlmn jgdxt vhxjc xtpvjscp chtd jrmnf zqr pqrvc rfqxzg jhvbj tnrkjkr cgdx prcbf ndfq gdgdd tffgpr pvpbdk lkv vpsmz rrmvn zzvhml krg gmmtk ktfzfj mpklvq dvmzkk kltxt mrj fdsfpg vntgs rfdm lclnj (contains fish)
qdxnn nhlrh qrdq kxsftq dlrpp xzkgmj mmvgjk cpnxdkk pzxlmn pvpbdk lclnj xbj bvn gsbdgk tsgvdsj vcrs lkgjp tpfjxp fdsfpg lkv psrnxh zqr vhsh vqmqqr qmmzr jrmnf ljnk prgnr dcfzd srckbnq lgtpk sgfvv bljlvc pqrvc jxdcgp mpklvq ffdsnc dcrtvq nvp chtd kmzrf hqtdss qqsr ffqpqck tnrkjkr bfrtj vhxjc tbrdjm qntgqv nbgl jlxqpjd dgnvz lxrtk vpfstj kfgln dcvrc vntgs smk tkccrc xtpvjscp ghkptm bbsnzc vnddzb jdfcj lfq ndfq mjhdfg vshth llpvqk xtdrm nxkpfqtg jmvxx qthz pqqks tfdfqp prcbf jx lsx hlkqpp (contains fish, eggs, wheat)
qp kfgln kpsp vxn vntgs dcfzd vnddzb lfq pqrvc cbzcgvc nhlrh jmvxx dcrtvq lvzjpn zttgff zhxh pqqks bljlvc pcgr jlxqpjd lkv chtd zttnb kc lfqpqc nvp dcxcc pzxlmn jjjn prcbf pxtg tpv gjcnhb zzvhml mrj zvqg llpvqk trvjv pvpbdk vxrdlb lclnj xgqfzp smk (contains eggs, wheat)
vxn qltxnk vsskb zttnb rdpzthm qmq fdsfpg jlxqpjd mrj prcbf qqsr jgdxt dcfzd qmmzr vhxjc vbbk pqrvc pgckbv xnjhn jzfz srckbnq nhlrh kfgln fjlhvt gffjlg vxrdlb pcgr lkgjp jmvxx scfhknrs ffdsnc tpjf tffgpr xmcs mmvgjk krg qrdq tfdfqp ndfq vhsh mjhdfg qqdxk tnn qtbtcv grjrrm trvjv fzccd zvdqv kmzrf sfp nvzjxr vqmqqr frq nvqgxc cbzcgvc zqr cpjmc jbt lkv bbsnzc rfdm psrnxh mpklvq vpfstj gjcnhb lclnj xbf lfqpqc dlrpp jx rrmvn (contains eggs, soy, wheat)
pqqks zhxh sxbr ghkptm vvgcfr gsbdgk cdkx qnjbl fzccd fdsfpg rrmvn fbcnsr lfqpqc flfn fnvjz cbzcgvc rfqxzg vqmqqr xnjhn rzjcr jmvxx nvqgxc prcbf lfq qntgqv xgqfzp scfhknrs rmfmm sfp jhvbj zttgff dxxmnr tkccrc lkv dcxcc ktfzfj xtdrm qnsl kfgln qtsjztd kxsftq qqdxk lclnj lxrtk mfl bbsnzc tpfjxp xmnscmnv (contains eggs, shellfish)
fdsfpg kfgln cbpt ktfzfj rmfmm fnvjz ndfq xmnscmnv vhsh glbpt vppmgd nvp tpv vhxjc tsdz fvd qnjbl bbsnzc zzvhml jjjn sclxx nkktc bfrtj gffjlg lkv srckbnq pqqks jzfz mtkgvt pqrvc tkccrc xnjhn qnsl gdfddn nbgl vpfstj kltxt hdqdqbm jbt lclnj qhpds vshth qthz nhlrh mnnzf tnn tffgpr cpjmc nhnnc jmvxx qdxnn grjrrm prcft qqdxk vntgs fzccd rdpzthm pvpbdk pgmj zvdqv rfqxzg jlxqpjd zrxbmt ffdsnc ffqpqck qtsjztd lgtpk lxrtk (contains fish, sesame)
fbcnsr vpsmz fdsfpg jbt trvjv rmfmm qthz grjrrm jmvxx ffqpqck jjjn qlcd mzsb dcxcc cpjmc lsntrr qqdxk sgfvv dvmzkk nzhsjkt dcvrc qtbtcv djrbkjr xtdrm dxxmnr bfrtj mjhdfg cbpt vpmzl cpnxdkk ljnk pqqks vhxjc fzccd gffjlg fnvjz kxsftq vpfstj tnrkjkr vntgs lgtpk jlxqpjd vlbdl vshth pxtg lfq vbbk mpklvq dgnvz vcrs pqrvc xnjhn lclnj qqsr xbf lkv kmzrf vhsh lxrtk lvzjpn rfdm svpfz gmmtk zzvhml qrdq hlkqpp fvd kpsp kfgln cdkx tbv tnfgxsn (contains fish)
rzjcr lgtpk tbv jmvxx kfgln qtsjztd cbzcgvc frq lfq qrdq lkv tktff nvzjxr lpqxmc qqsr chtd mmvgjk glbpt tpjf nnlmz mrj ghkptm rmfmm pvpbdk tfdfqp pqqks qntgqv jgdxt vsskb nhnnc sclxx xmnscmnv vqmqqr xf nzhsjkt xbf fzccd psrnxh qp pzxlmn qthz krg lclnj bvn jts grjrrm kmzrf ffdsnc nxkpfqtg qlcd jrmnf tpv zttgff vlbdl qdxnn tnrkjkr fdsfpg (contains shellfish)
zzvhml jfpttz vcrs zvqg glbpt tsdz pqrvc vlbdl jmvxx tffgpr cbzcgvc tnfgxsn vpmzl qnjbl xmnscmnv ghkptm qqdxk scfhknrs xbj jztckz nbgl kxsftq gppn rfqxzg fdsfpg qltxnk nzhsjkt pvpbdk mfl zrxbmt lkv chtd vhxjc jzfz prgnr xmcs kc mrj nnlmz kfgln jbt sxbr gdfddn mzsb bvn bljlvc xtdrm dcxcc dcfzd tpv ktfzfj zpn rjj pqqks hqtdss vpfstj djrbkjr vppmgd fjlhvt dcrtvq tpfjxp ffqpqck (contains dairy, shellfish)
jmvxx jfpttz cbzcgvc mpklvq scfhknrs pxtg mrj vpsmz sgfvv xjvc ghkptm lkgjp nvp lclnj kfgln jjjn hqtdss vpfstj jts xtpvjscp kxsftq qqsr qp fvd dcxcc lsx gdgdd kpsp gmmtk smk gppn lfqpqc sxbr pvpbdk rjj hvhsn nhnnc tpjf tsgvdsj pqrvc lsntrr tsdz flfn msqtqc dxxmnr xf cgdx pqqks sclxx ffqpqck qqdxk jvx xgqfzp jx dcrtvq qnsl qdxnn lvzjpn tktff nbgl llpvqk vppmgd vbbk zvqg vxn bljlvc lxrtk dzvsv zzvhml hdqdqbm bvn qmq nhlrh mtkgvt xtdrm lkv (contains shellfish, sesame, wheat)
cpnxdkk tnn lsx lclnj lvzjpn nzhsjkt qmq pqrvc qqdxk zqr qp jmvxx dvmzkk rmfmm fnvjz fdsfpg qgnpkp vppmgd nxkpfqtg dcrtvq cgdx vxn sgfvv jlxqpjd lkv lfq lkgjp mrj hqtdss cbzcgvc vxrdlb jztckz vpsmz nvqgxc cdkx xbj dcvrc gjcnhb jx gffjlg rjj zvdqv jzfz qrdq qqsr rdpzthm bfrtj vvgcfr tktff hvhsn lnfvdxb gmmtk scfhknrs kfgln zrxbmt lpqxmc rzjcr jrmnf qlcd qnsl nkktc qhpds mzsb psrnxh xf xtdrm vhsh sfp (contains soy)
pvpbdk grjrrm jx gdfddn dvmzkk qltxnk glbpt tnrkjkr qmmzr vpsmz zvqg vcrs pgmj rjj qp nvzjxr qtbtcv dcvrc pqqks kfgln bvn qqdxk nkktc pqrvc sclxx mnpfcx sfp cbpt bbsnzc prcbf xbf gsbdgk xf rfqxzg xmcs vntgs lkv gjcnhb dcrtvq nhlrh zqr fdsfpg trvjv fbcnsr rfdm jts cpjmc cbzcgvc nvqgxc tktff qrdq smk lclnj xmnscmnv tsdz jzfz jjjn vlbdl tffgpr rrmvn pgckbv mrj zzvhml jvx cgdx tkccrc prcft ffdsnc cdkx rzjcr vqmqqr fvd qnsl zpn gffjlg fnvjz nnlmz jztckz jrmnf qthz (contains peanuts, sesame, soy)
xf vbbk jzfz vxn zttgff pxtg chtd nvzjxr pcgr qmmzr tfdfqp krg sgfvv mzsb rfqxzg nnlmz jx lsx vpsmz rjj qgnpkp fdsfpg xbf prgnr jmvxx kfgln cbzcgvc kxsftq zhxh dlrpp tnn tkccrc jxdcgp pgckbv grjrrm tpfjxp mfl bfrtj mmvgjk trvjv qthz bvn pqqks lclnj xjvc lkv prcft (contains sesame, peanuts)
sfp zzvhml lvzjpn jhvbj tfdfqp smk dlrpp gdgdd rrmvn qnsl qltxnk jxdcgp rfdm jmvxx vshth kltxt tbrdjm qmmzr jztckz lkv nvzjxr jjjn vnddzb zttnb chtd kxsftq lnfvdxb sgfvv mnpfcx nnlmz pqrvc jfpttz vvgcfr tffgpr mzsb jvx lclnj hvhsn qqsr pqqks pgmj mnnzf fdsfpg ffqpqck llpvqk vppmgd xjvc kfgln vpsmz pxtg (contains shellfish, soy, dairy)
bfrtj nvqgxc xtdrm zttnb sxbr sfp kltxt qntgqv vqmqqr qthz prcbf qp zrxbmt jmvxx tpv kfgln mtkgvt tfdfqp sgfvv ljnk mrj gdfddn stvl cbzcgvc lsx trvjv mnpfcx xtpvjscp dvmzkk fdsfpg xbj tbrdjm vshth sclxx qtsjztd mpklvq ffdsnc qqdxk vcrs qhpds qltxnk lfq smk qrdq lpqxmc qqsr qmmzr vhsh tnn pqqks djrbkjr scfhknrs qlcd bbsnzc lclnj xgqfzp fbcnsr pqrvc (contains wheat)
lfqpqc krg nnlmz ffdsnc jxdcgp cbzcgvc lkv gjcnhb cgdx qmq kfgln pcgr vvgcfr sxbr kxsftq lxrtk rjj cpnxdkk dgnvz fdsfpg jhvbj jzfz zpn stvl tffgpr prcft tpv jztckz pqqks zvdqv lsntrr xnjhn lgtpk cdkx tnfgxsn kpsp tpfjxp qhpds sclxx ndfq qgnpkp jmvxx pqrvc mpklvq mrj hdqdqbm tnn srckbnq fbcnsr vhxjc lkgjp xf hvhsn bvn hqtdss jlxqpjd sgfvv nkktc xbj kmzrf vnddzb gmmtk fnvjz cpjmc dzvsv xmnscmnv dlrpp fvd fjlhvt nbgl (contains eggs, sesame, fish)
vqmqqr nxkpfqtg qntgqv tffgpr lgtpk hdqdqbm nvzjxr rfdm vntgs jvx pqrvc djrbkjr lvzjpn qnsl rfqxzg vpsmz rdpzthm jzfz ghkptm lfq jmvxx lxrtk xbf dcfzd tbrdjm vxn gppn qthz qrdq lclnj tpv cbzcgvc gjcnhb srckbnq nbgl pgmj pxtg gsbdgk mnpfcx zrxbmt pqqks grjrrm kfgln pvpbdk sclxx dcrtvq fvd nhnnc tkccrc qltxnk mjhdfg fdsfpg jxdcgp mzsb (contains shellfish, sesame)
jts zhxh xbf qqdxk nbgl kxsftq cbzcgvc lnfvdxb vsskb zqr xtpvjscp jvx jxdcgp vxn nnlmz qp mmvgjk fdsfpg rzjcr jbt pzxlmn pqqks qnsl mnpfcx dcxcc cgdx jfpttz bvn zvqg pqrvc tnfgxsn lsntrr vnddzb qlcd gffjlg zvdqv rjj tpjf dlrpp pcgr dvmzkk hqtdss prgnr jztckz kfgln lxrtk cpnxdkk jmvxx prcft scfhknrs vvgcfr dcvrc smk tkccrc vshth jhvbj vcrs gdgdd krg trvjv tpfjxp tktff fbcnsr dzvsv lkv tpv msqtqc vqmqqr (contains shellfish)
tktff zvqg vhxjc hqtdss lclnj jbt xtdrm nnlmz vpfstj tsgvdsj jx tpv qmmzr jvx xzkgmj prcbf fbcnsr vbbk qnsl trvjv rjj zpn lfq dxxmnr nkktc jdfcj jts krg kfgln tbrdjm xbf stvl jzfz tkccrc mzsb zrxbmt jztckz mnnzf jgdxt tbv kltxt qhpds qdxnn gjcnhb pqrvc jmvxx fnvjz jjjn cbzcgvc pqqks zvdqv mfl zzvhml ljnk scfhknrs lkv djrbkjr nxkpfqtg jrmnf pgmj ndfq mnpfcx sgfvv pgckbv vsskb bfrtj qqdxk xgqfzp chtd hdqdqbm qthz mmvgjk lnfvdxb (contains peanuts, soy, wheat)
lnfvdxb qnjbl smk tbrdjm prcft zvdqv nhnnc lclnj prcbf cbzcgvc zvqg tsdz ghkptm zhxh qntgqv lxrtk fdsfpg flfn hvhsn jgdxt bbsnzc ffqpqck kfgln lkv chtd qp mnpfcx sxbr xmcs xmnscmnv jvx jrmnf xjvc zrxbmt gjcnhb lgtpk dcxcc vvgcfr gdgdd sfp svpfz pqrvc pqqks frq grjrrm (contains wheat)
flfn kfgln jx vppmgd lnfvdxb lfqpqc zqr tfdfqp vntgs vshth kxsftq jdfcj jbt prgnr qgnpkp qhpds jzfz ndfq qlcd lkv vhxjc tpjf pqrvc hdqdqbm xmcs fdsfpg rfqxzg jvx rzjcr vxn cbzcgvc jmvxx xzkgmj hvhsn vqmqqr qmq nzhsjkt nkktc pqqks (contains shellfish)
zvdqv hlkqpp zttnb cbzcgvc dlrpp fvd vntgs fbcnsr kfgln jvx pcgr jgdxt nvzjxr dcfzd lsx dgnvz mtkgvt jzfz hvhsn qntgqv xf kmzrf rdpzthm tktff vsskb lkv gdgdd pqrvc cbpt xbf tkccrc gjcnhb sfp vpsmz msqtqc vxrdlb jmvxx gffjlg rmfmm fdsfpg pgmj tpfjxp dcrtvq fnvjz rfqxzg gmmtk svpfz prgnr xbj qtbtcv vhsh tbv mjhdfg pqqks tsdz flfn vbbk lnfvdxb nbgl grjrrm rfdm rjj bfrtj qrdq pgckbv qqdxk vhxjc (contains shellfish)
⛄"""
