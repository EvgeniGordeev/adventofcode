#!/usr/bin/env python3
from collections import deque


def parser(text) -> str:
    return text.strip()


def read_input() -> str:
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


# MAIN FUNCTIONS

def start_of_packet_marker(given: str, message_size: int) -> int:
    stack = deque()
    for i, ch in enumerate(given):
        stack.append(ch)
        if len(stack) == message_size:
            # message must contain unique characters
            if len(set(stack)) == message_size:
                return i + 1
            else:
                stack.popleft()
    return -1


def part1(given: str) -> int:
    return start_of_packet_marker(given, 4)


def part2(given: str) -> int:
    return start_of_packet_marker(given, 14)


# TEST
def test():
    # GIVEN
    assert part1("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert part1("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert part1("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert part1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11
    # part 2
    assert part2("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19
    assert part2("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
    assert part2("nppdvjthqldpwncqszvftbrmjlhg") == 23
    assert part2("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29
    assert part2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26

    return True


if __name__ == '__main__':
    assert test()
    given = parser(read_input())
    # ONE #1
    res1 = part1(given)
    print(res1)
    assert res1 == 1757
    # TWO #2
    res2 = part2(given)
    print(res2)
    assert res2 == 2950

# INPUT
"""🎅
bjbffsfnsnppzpphvhjvjtjmjwjrjdjffwrfrvvrqrrqwrrqpqhqnnddvccrbbwcwbcbclclhlzlznntrrzffctcggzqgqtgqtgtrgttlhttgstgtsgsfsnsddsvdsvddrzrvrnvnrvnrnmrrvfvbfbnbmmtbbgpgtptjptpctpccmccgbccqbcqczqccdssfqfzzjgzzvcvgggrjggncgctgtjjpttqtrrvmrvmmzzfcffpgfgfqggbwgghcctllfhlffbbcffspfpcplpjjlwldwldlpddwzzlqzqfzzcwcmwwcddhgddstsnsjsvjsvvndndsnnclcvcpvpwpqwpqwqllcjcsjjbppfdftfrrpwwqtqtvtllrsrhhczzgllsbsvsttbsszzgwgjwjqwjwvvcmcbczbbgppghghgshhvmhmvvvflllllsrsqsbbfsshhrhddcncbnnrfnnbtbftfltftdtndtdtcdcbdcbchhtddhhvbvsbstsjsjppmpjpttmjjvtjvvdcctcbbbbqzzssfdsdrdwdpplspllphpnhnshnncwnnhlnhhvvpttfftwfwjfjzjsjddjldjlddvzzfzczrzjrzrhzhshslhsllmcllhhthrttfssnqnjnbbzfbbmpmlplhlttmzzwrwjrjppzmpmrprcprplrprmrvrvqrrnlnccswwvggvgcgddlrlrccqhhgvgnvvmlmmcqqhrqrwqwsswgssfjjgvjvppfffhjhrhfhhlphpmpzmpmlppcspcpgpnpddcmcllwvvqfqbbpbcchjjpzpzbbhbzhhrrzrhzhphqphhqvqttmhhbvbcbcmbbfgbbmnmncmnmvnvffgdfggvhvthvhqqdwwvmvlmljjjvsjswjwzwjjqmqrmqmlljqqjvqvtvlldjjfbbpbvbttqhhgrrcssfdsdccrncrncnmnvvmccnrrrtctjtsjttrmrhhvdhdrdjdpdhphsppnttnhhvdvvztvtftsfsrfrppsggfbgbbvbmmjgjrjttfnngttscclzcztctcltcllsmllggbfbhffjljhhbjjjgddzdvdvrvzrrgqgllnvllnccqjqhhwrhhtfttfpfsfvfqvqgvgpppjjhzzcszczbcbtblltlffdfwddfsspgprgpgjgdgsgcccrllbzbqzbzwbwwtmwwvpvlpljlsjssfnfqfzqffthtjtptvptvvmlvlzzdnznwnddjtjpptnpnccbsccjmjqqcfcdddwtdtftntzzpbbbhcbblglttrmmclcdchhzttjwtwztwzwzczfccmrmcrmrsrnsrnrsnrrfmmmcpmmjtjrrwssvdssrvrqvrvcrchrhfhpprwprwpwtttvrtvrvffdcfcssfrfbbvsslvvhphrrwggssjtjbttqtllnmlnljlmmtllfjjtjtpjttbwbswsnwnnjdjbblfbfmmblmmwnmnncjcwwhzzdffvppvmmtzzrhrchhtjhttcssvnsnvnhvvdgvvvgtvtqtgqqzrzbzqzgqgmqmtqqztqqgllchlclwwbwrrwprwprrlgrgwggjhggtgmtggjddfhdddnzztrtjrjprpwrwttqzqnzzfnfcnfcftflfttvbvpbpllrtltslttlddbzdbzzfjfrjfjcjhjssbcsczcnznlzzggdccllhbhpbhbjbwjbwjwtwffptpqqqmssrlrddwqwqdqfqjqwqtqhtsrgvsdtrjmhtgrwvwrbfqtgvjbwphbrszdcgtcpqqrcqtzvzjstzpbmwrqlrcsmlnqpsprsfnpqqsdzbfglcshtjpphmchdzggrcjwttwlzdffgpswzfjdcgzntgzsqvjdnwwwwmtjvpqjgmltmstzztpzflfdhbhhljgdmthnrdzhmtwcmpsjnlgwcvnwdbdrbhcsscgwtptzrmqcwdcmsssmqjpnvclhhbgsjrmqgvvqhgmhzmnpqtczqwmnpvvpdhdtdpdsrmzwtsfchzmdlggrnvwcfbfmrgffssdjjlwbdvjqqwddgmgfwvbzldccwnwrnltcrmblwqswjslnsjtfqvssdrdtpwptdtvtdwhgtgqnmhqfljjjsdgwmptbctjtpdhzmtshgdwnnhfjthmhdrqqqprrdwhvsfwfbvwtfvhgglfphzwjqffwcclbpmtcqzmtjmswscngtbmbdsvfzfbgwvhwlhtgdsnscnrssdqzvhmhplqppzrgdncfvvpnzhgnjrvcmhrqmzvzmdhhpjmrrnwfrhdgqdhvvstbldrgdcwbgjvcwhfrpbgrnvgcszhpbbgvqnvvrrcgprtsftjqtnrbqrzspmzpnchbrbbbpnjdllhnnbcfdsjjhhjcrvvtsgnnfvczvqgvbgphzzjcczsgtlvfrddzlvwdfhprnsvrnzdcfqsbfhcmnrgmrfqwcblbzgrpnvbtrqqnnfslfllfsmrrfsthfzgrwswdprzcswgrjcpzwfhzbhpmsjjtsgcqpnhtwpvpcbpttdpcftrqsbtgtspdhlvmphvnglsdntqfzcrwvvzsmjftjpgjglnnjhnpbhpcmwshdrfbczwtmtslcpmnpngvhlccvtwrsglrrfcmngshtjlnvrtqpfngrrtvhhvmnbwpjtwplfnmfqrbzzqzwchthjbbrpgdppmsjlbljrzqvhmsbrtwglgwnhmmdwpmvmjqqrhtmjjmcnbgtpbbqbnphzhwfhzddqbhqhtmwvffjdcfjmwjjdrqwsfzfrrwlmhndhdvrsdqtmccdqgppwpfrtcgzzwczfblvtjhhdjmdlldbtwthfdpjhpsgbcjjznmwdgnczbnfdfslhsjcjnthgsjlslbcvvqgqbstdwlqllpmmtqlqrbtnvphvwhbshhpdzfbclsqgdmhrnjmbwjzwzdtqswzgmnmwcqcmtpnjzzcrqftvnrdqghszchhmnvlvmcmblpcqnspsjthgqrdpbrzvwtfmnfdcfgwtlvpvwjdwzdvqvgdrcqvzwlbmcwmbsqfhzmwfqmjvgjtsprwbbsrldnwmvhrtsmcdsbftpvcsmpnlmlggmlrgjfvljmpfldftqhjmqqhwfpjtzrrhtlrmmstjphtmldslnnmfhnccrpgjmrbffcvgvmghhnpqhpvdqmdzqcjtcjplhlffwgslpsfzpwqsfpngscdlszlpctpqgdmvwfdfgpwrpltvlwrzrgjjjnjtrwctjsnbtpbfbgqzftmjhfrzrtmtnztlhwwgqnvmfnrshfcdswbqnlrqvtgjdzmqqcdgpwjlgfwnnnjsmmtfbvpwqvnjdjphclnvjntqlfwdppjgcvlcjmfdsbtgngcglmdgsgzwdvsqlvgwcrjtttgdmrlthhwhnnrvvrjgqzqmbcbmhdwmndhjstlmbtwjbgmlrqqcmqzjzcbbfrqrqlmvvgfrdtrwrpgcfsrnjdbfddwgwqrlpvfjgnjjnrlzpbtnjphlqzmdwnqhvblmwzvtnsvbcgqdpmgvchqmgjmbvrfwmmzlchhbqrfmvdffczcsjlhjrmmlmdztmltszrjlrgjwrlfwvlgqtqznnscbqgdzbvdnnjbfmcztjvbgbfmdhvrjgjcngtpzndpnpwwldlfrtqhwpfwphrgdzjvslnbpmrvjpcjpbbsmpwvzmldrspmrlbsptzfdngcscsllswzccjzlmbglsrthvbzznzpjdswhqncmrpnqhzggzzfvhlgqbvlmfsqglpphhswhjbpqnqfpzltmhndmmzclwfmlqztvrqdzfqjpdhttgshjwffdcchmvrwmblpzffbgwrgnqhhvvsvlwnzmmhjwrszpfdsncjwllrnzrsfjsrdgnrbjqlrvpmzbstlqdznhjgbslzmplnqprwqgddjlwzbtrmfsfdlggddqrccztjffvbnsmfdzdhrgsflffmmjtjlbtnfcwhwzdsnbbphbjlrfrddbpncjrtglsnrppdbznrbjqqzdswnhvssffhjzrwnmlvmwmljnhtsnplpjdjpqzbbmzzfcmpm
⛄"""
