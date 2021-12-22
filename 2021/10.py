#!/usr/bin/env python3


# INPUT
def parser(text) -> list:
    return text.strip().splitlines()


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


# MAIN
close_to_open = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<"
}
open_to_close = {v: k for k, v in close_to_open.items()}


def part1(lines: list) -> tuple:
    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }

    ans = 0
    incomplete = []
    for mes in lines:
        stack = []
        valid = True
        for br in mes:
            if br in close_to_open:
                if stack and close_to_open[br] == stack[-1]:
                    stack.pop()
                else:
                    # invalid bracket
                    valid = False
                    ans += scores[br]
                    break
            else:
                stack.append(br)
        if valid and stack:
            incomplete.append(stack)
    return ans, incomplete


def part2(incomplete_lines: list) -> int:
    values = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }
    scores = []
    for stack in incomplete_lines:
        ans = 0
        while stack:
            last = stack.pop()
            ans = ans * 5 + values[open_to_close[last]]
        scores.append(ans)
    return sorted(scores)[len(scores) // 2]


# TEST
def test():
    # GIVEN
    sample_input = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
    given = parser(sample_input)
    score1, given2 = part1(given)
    assert score1 == 26397
    # part 2
    assert part2(given2) == 288957
    return True


if __name__ == '__main__':
    assert test()
    input_ = parser(read_input())
    # ONE #1
    part_1, incomplete = part1(input_)
    print(part_1)
    assert part_1 == 193275
    # TWO #2
    part_2 = part2(incomplete)
    print(part_2)
    assert part_2 == 2429644557

# INPUT
"""🎅
({{[<{[{[[<([[<><>][{}()]]<([]{})[<>()]>)><<<([]())>>{([()<>][{}{}])<[<>()]{()()}>}>]<(<[[[]<>]({}{})]{{{}<>}
[(<<<[[[{({(([{}{}]<()<>>)[<()<>>[[]<>]])}([{{<>()}}]))}<[{{[<[]()>][[<>()][[][]]]}{{(()()){{}{})}}
<(<(<<{<(({(<[()()]<<>[]>>((()[])(<><>)))}))[{<{<[(){}]>}><[<{{}[]}{[][]}>(<{}{}>)]([(<><>)(<>{})]{{(){}}[<>(
[{<[<{[[[<{<(<[]<>><<><>>)<{{}()}>>{[<()>{[]<>}]}}>[(<{[{}()]<<>()>}{(<>[])({}<>)}>)]]}{({<
[<[(<<<([[[<(<<>{}><()>)(<[]<>>([][]))>(<{{}<>}{{}[]}>)]](<(<({}){<>()}>{<{}<>>})[{[{}<>][<
[([(<([[[([([<[]()>[()()]]{{<>{}}([][])})<{<[][]>{()[])}[{<>{}}<<>()>]>][<[<{}<>>[[]{}]](<()
{({{<{[[(<[[{[()()][()[]]}<{<>[]}<{}()>>]({<<>>}(({}{})(<>)))]<([[()[]]<(){}>]{{{}<>}([]<>)})([{[][]}{<>
<(<{{([[<<({[<(){}>[()<>]]{[{}<>]<(){}>}}(<[[]{}]<[][]>>))<<[{{}()}][{<>[]}[{}<>]]>[([<>{}]{[]{}})
[<{<((([{<(<(<{}>[{}()])>)<{[{<>()}[{}[]]][{[]}<{}()}]}((<{}>{[]<>})({()()}<[]{}>))>>}])))
<{(<{((([((({({}<>)([]<>)}({()<>}[{}<>])){(<[][]><()[]>)<[{}[]]<[][]>>})[[{{<>{}}(<><>)}{[()()][()[]]}]])[[{
{<[<[[[(({(<<{[][]}(<>{})>{<[]()><()()>}>(({[]<>}{()<>}){[()()]}))})<({{<(<>{})>[(<>[]){()
([[[{{[<([<<({[]{}}{(){}})(<[]<>><[]<>>)>{{{[]}{[]{}}}}><[[[<><>]{{}[]}]]<<[{}{}][(){}]>{<()[]>[{}[]]}>>]
{[[[<<({([<<(((){})<{}()>)[({}[])<()[]>]><<[[]{}]<<>()>>{(<>())}>](<<{[]{}}[<>()]>>[{({}<>)[()[]]}
[<{{<({<<[(<<<{}<>>{[]{}}><((){})((){})>>(<[[]<>][(){}]>[<{}()>({}<>)]])]<[<{[[]()]({}[])}>(<
<{(({{(({({<[<{}<>><[][]>]<{(){}}>>}[(<[[]{}](()())>[[()()][{}[]]])])<[(<[<><>](()[])><{{}{}
[[(({(({([[<{<{}<>>{(){}}}{(<>[])<[]()>}>][[[<[]()>[()]][<<>{}><{}()>]]([([][])])]]<({[[<>[]][{}<>]]<{
<<[{{{<<[<{<<[<><>]{[]}>>{<([]<>)<<>[]>>[(<>{})(()())]}}{<[{{}<>}(<>[])]>[[{{}{}}<{}<>>](([
((({{[[<[([[<{()<>}({}{})><<<>[]><()<>>>]{{<[]{}>[{}()]}(<[]<>><()[]>)}][{{<[][]>}<[()[]]<[]()>>}])]>]]}([{{[
[([{({<<[{[[{{()()}}[[<>()]([]())]]{{(()<>)[{}()]}{[(){}][<>()]}}]}]>(([{[{[[]{}]{[]<>]}]{{<[]<
<(<(<({{<<([<{[]{}}[{}<>]>{<<><>>{{}{}}}])({(<<><>>((){}))({[]<>}<{}<>>)})>{{[<<()<>><[]()>><((){})<{}<>>>]<
([{<{{[{([{[<[(){}]{(){}}><{[]()}[{}{}]>]({<<>{}>({}[])})}[{[{[]()}<(){}>]({[]{}}{()()})}(
(<[([[(<([([<[[]()]>][<[()<>]([][]}>[(()[])<[]()>]])<{[<[][]>(()[])](([]()))}{[<{}<>>[[]()]]((()<>)
[([((([<<{[({{{}()}(<>())}([()<>]<{}()>))<<(()[])[()<>]>{<()>}>]}{{((({}{})[{}<>])[{[]()}([]{})])<<{<>[]}(
<([{(<<[(<({<<{}{}>{{}[]})<<<>[]><[]<>>>}(<([]<>)<(){}>>[[{}{}]<[]{}>]))>{([<<{}{}>>({[]()})])})](
[(<[((<{[(((([[]]<<>[]>){<{}<>><()()>}))<[[{{}()}<<>()>]]>)]<<(<{(<>{})}{({}<>){{}()}}>([{()<>}{{}()
<{(<<[{<<[({<<{}{}><()[]>>}){[([{}{}]([]{}])(((){})[[]<>])]<<<()<>><<><>>>([{}()]<[][]>)>}]>>(<(<({({}
(([{{<{{(<{[{{<>[]}}({{}[]}<(){}>)]{(([]())[()<>])<[[]][[]()]>}}{<({(){}})<[{}{}]>>[((()()))]}
[(({[<{([{[[{[[]()]<[]{}>}]{{<{}[]>{<>{}}}{(()<>)<()<>>}}][<<<{}()>(()())>>]}(([{{<>[]}[(){}]}[([]<>)<
[<(<{{(<[(<<({()<>}<()()>)([<><>]<(){}>)>>)]>{<<[([[(){})<<>[]>])({<()>(()[])})][[({{}}(<>())){
(((<<[<(([<[<[()()][{}()]>[([]())[[]()]]][<<<><>>{<><>}>{<<>[]>[<>()]}]>}{<{[[()[]]<()()>]{[[][]][[]
{{(<<{(<[<({{<<>()>{{}[]}}([[]{}]<[][]>)}<(({}()){()()})>)>({<[[<><>]{[]}]{(<>())([]{})}>[[<<>[]>({}
<<<[[[<[<{[[<({}())[[]()]><{(){}}{{}}>]][[[[{}[]]<(){}>]]<[{()()}<[]{}]]<(<>())[<><>]>>]}<[[({<>}<{}{}>)<
(<(<[<<{<[({([[]{}]{[]}){[(){}](<>{})}}{[[[]][[]()]]})<[<[<>()]{{}()}>][((()[]){(){}})[[()
<[{{{({(([{[{<{}<>>}<[{}<>]>]}]<([{{(){}}{[][]}}[<<>()><{}<>>]][{<{}[]>{()()}}])[({[{}<>][[][]]}{[{
<[<{[([<<[[<[<()[]>[<>{}]]{([][]){[]<>}}>({{()<>}[()<>]}[{<>()}{<>{}}])]<<{({}())(<>)}[[()()][[]{}]]>>]>><(
{[{<([(<<[[<[[<>{}}{{}{}}][{{}{}}[{}{}]]>][{([[][]](()[]))(([][])(()<>))}{[<<>{}>{[]}]{((){})(<>)}}]]{[<<<
(({<<[<[<(<[<[<>{}]([]{})>(<[]<>><()>)][<[<>()]{()[]}>]>)[[[({{}{}){<><>})[(<>()){{}<>}]]]<<[<()[]>([][])]<<[
<[({<<<<[{<<([{}[]][[]<>])[({}())<()<>>]>{<{{}<>}{[]}>[([]())({}()))}>}]{[<<<(<>())(()<>)>>{[<<><>>({}{})][
<<((<{<{[{<<{<()<>>{<>{}}}>>}{<{{<<>>(()())}<{[]()}[()<>]>}{[<()>{<><>}]}>([<{[]<>}[{}<>]>{[[]<>]<<
([<[<[<<{{{{{(()<>)[<>()]}[({}{})[{}{}]]}(((()()))<{<><>}>)}<[<[<>()]{<><>}>[{<><>}{()}]](
[([[((<({{([[([]{}){{}<>}]([[]()]<<>[]>)][[<()()>{{}}]<((){})[<>()]>])<<{<[][]>}[[[]<>]<{}<>>]>{{({}[])(
<(<<[<{{[([([(<>()}{()()}][{{}{}}[<>]]){<{<><>}<[]<>>>{{<><>}[[]()]}}]<<[([]<>)<()[]>]><[<[][]>]<[{}{}]{{}[]}
[({(({(({{([{[{}()]<()<>>}(([][])({}))])({(<{}()>)}{{([]<>)(<>{})}})}({<[<{}<>>{[][]}]({<>[]}<{
[([[<[[{{<(<{<()<>><<>()]}<<[]{}>([]())>><<[[]<>]{{}<>}>>)><([<({}())>((<>{})[(){}])][<<[]()>(
[[(((<{({<<(<({}[])({}[])>[{[]{}}{<>{}}])[<<[][]>{<><>}>([[]()](<>[]))]>({<<<><>><[]()>>[([][])[[]{}]]})>}<
{[<(<<[{{{{<<{{}{}}{()<>}>(<[]()>({}<>))>}({<{{}()}{()()}>(<[]{}>({}<>))}([[<>()]({}())}((
{[{([{<([({{{[{}<>){{}}}(<<>{}>{<><>})}[<<()()><<>[]>>]})(<<{([]<>)<{}()>}>>)])(<{<((<()[]>{{}{}})){({[]<>}(
<[[<(<{{{{{((<()<>>(<>{}))([{}{}]<<>[]>))<{<[]>(<>{})}>}}[(((([]<>){<>[]}))(({<>()}({}[]))))]}([{[<{[]
{<({[{[{<{{{[[<><>]{{}<>})<<[]()>([])>}[{{<>[]}{()<>}}]}<<{<{}<>>({}<>)}[<{}()>[[]<>]]>[<<<>{}>[(){}
<({({{([<[[[<{<>{}}([])>](<{[]}<[]<>>>)]]>)<[[<([<{}[]>[()()]]<(<>{})<{}[]>>){{({}<>)[[]<>]}<{{}{}}{()<
<{<{({<<{{{(<{[]{}}(()())>({<>[]}(<>[])))<{([][]){{}()}}(<{}[]>)>}{[<<()<>><{}[]>>{{[]{}}[[]()
{[<({<<{[(<{([{}[]]<[]<>>)<<{}[]>[()()]>}<<{()[]}{<>{}}>[[{}()]([]<>)]>>({[([]{})]<<[]{}><[][]>>}))][{[[<{[]
[<<{<({<(<{{[{()()}<[][]>]{{<><>}({}{})}}}<<(<()[]>{[][]})[[{}()]]><[<<>[]>(()<>)][(<>{})([]())]>>>[[<({
{{((([[<[<[[[{()<>}(<><>)](<{}()>({}()))][{<{}()>[{}[]]}{<{}[]>[{}<>]}]]({{[<>[]]<<><>>}([<>]{[]})}([({
<<([[{[{[<(({[{}{}]<()<>}}[(<>{})[(){}]])([[{}{}]]{[()<>]<()<>>})){{[([][])<()[]>]}}>]((<(<({
(<({[{[{(<<<<([]<>)<[]()>><{()[]}{{}()}>>{{[[]()](<><>)}({<><>}{<>{}})}>{([((){})(<>())]{<<><>>({}()}})([[{}
<<<{(([(((({{<()())}<((){})[<>{}]>})(<[{<>{}}<{}()>]([{}[]][{}()])>[{{[]{}}{[]<>}}{{<><>}({}<>)}])
(<{{[{{<([[[[([]()){(){}}][<[]()>{<><>}]]{[([])(<><>)]}]])((<[[({}{})[[]{}]]<({}){()}>][[(
{(((({([<[<<<[()()](<>{})>[{{}[]}<<>{}>]>>([{<{}()>[[]()]}{({}())<{}()>}])]{({<{[]{}}<[][]>><[[]
(<{[[<{{[((((<(){}><{}[]>)<{()()}<{}()>>)<<[(){}]>>}){(({{[]()}}<<<>[]>([]<>)>){{[<>{}]{[]()
<<{{{<<[{<[<[{[]{}}[{}<>]]<([]{})[<>{}]>>({[()()]}(([][])[<>()]>)][{<<<><>>(()<>)>[{<>()}<[]{
[[<[[[<([((({{{}<>}[()[]]}{([]<>)<{}()>})[(<<>()>{<><>})]))<[({(()()){{}<>}}(({}())<[]{}>))({<<>{}>[[]{}]}(
{[[({[(<<{<((<{}()>({}<>))<<{}()><{}[]>>)>(<[<()()>(<>)]{([][])[(){}]}){([{}()]({}()))[[()
(<({[{<{<({{{({}<>)}{[()<>]<{}{}>}}{<<{}{}>([]<>)>(<{}<>>{<>{}})}}{[{<(){}>><[[]()](<>())>
[<{(({[{[<(<({[]{}}[<>])[{()()}(()<>)]>{{[[]{}]}<({}[])[{}{}]>})[{[[()]{<>{}}][<()[]>[[]()]]
(<[{{<(<({{{({[][]}{()()}){([]())<[]{}>}}}{(<<{}()>{{}{}}>[(<>[])])}]{[<[<(){}><{}<>>]<(<>[])(()[])>>[[{()
<<[<{[(<{({(((<><>))[[{}{}}(()())])<{<()[]>}>})<[{<<{}<>>(()())>[<<>[]>[{}()]]}{{<{}()>[<>{}
<({((<([{{<[(<{}[]><<>()>)(({}()){[]{}})]{{<()[]>[()<>]}<{()[]}{[]<>}>}><<{((){})[{}<>]}{(()[]
<{{[[<{<{<{{{[[]<>]}{{{}{}}<[]()>}}[<{()<>}(()())><<{}<>><()[]>>]}<([[<>()]([]{})]{{()}{<>[]}}){<<[]<>>>((
<<({<{{[<{(((<(){}>{[]<>}){[(){}]})<({[]})[<()<>>{{}<>}]>)}><[({{<[][]>}}<{{[][]}<[]{}>}>>([(<{}<>>(()(
{<([{((({<((<<[]{}><{}<>>>[{{}()}[[][]]]))[<{[{}[]][<>[]]}>[<<{}()>{{}<>}>((<><>))]]>}(((<([[][]){[](
[[<{(<(([<[{(<{}[]>[{}<>])<<{}<>><<>()>>]<{[()<>]{{}{}}}{<<><>>[[]{}]}>]<(<{()()}<<>[]>><({
([{<(<<<([[{[[[]()]({}[])]({[]{}}(<>[]))}<{[[]{}]({}())}>]{([([][])[{}<>]]([<>()]<()[]>))}](<({({}[])((){})}
[<[{{[[[[[<({({}<>){{}{}}}{{[]<>}{<>}}){((<>())<[]<>>)[<()>[{}[]]]}>[{[[{}<>]]{{()<>}<()()>}>[[{[]<
(<{{{<([([([[([]())<[]{}>]<<()><[]()>>])])(<{[<(<>())<{}>>]<{[{}<>]<{}[]>}(([]<>)(<>()))>}(({<<>{}>[[]
{[(<[<{<<[{<<(()<>)<(){}>>[[<>[]](<>())]>{{[[]()][<>[]]}({{}[]}<<><>>)}}<<(([]<>)[()()])[[()<>][
(<<[(([<([<<[[()[]]([]<>)]{(<>())([][])}>>{((<{}[]>{<>{}})[<<>()>])}]{([{{()()}<<>()]}{[[][]][(){}]}]
{{<[<(((<(<{{([]())<{}()>}<<<>[]>{{}<>}>}<<<[]{}>>(<[]{}>({}<>))>><<{[(){}][[]()]}{{<>[]}([]
[{{<[[([{[({[({}<>){{}()}]([{}<>]({}()))}(({()<>}<[][]>)({{}{}}{<>[]})))([([()[]][[]{}])]<<([
([<(({<<(<([<([]()){(){}}>[([]{}){()[]})]{{(<>())(<>[])}<[<>[]][{}[]]>})><[[{(()<>){{}()}}{
<((<<[{[[[[{[[<>{}][[]()]]{{[][]}<[][]>}>]]{({{[()[]]<{}[]>}<[<><>]<[]<>>>}<<<()<>>>[{()()}]>)(<<{<>()}>([{}
([(([{([((<{<([]<>)<{}<>>>(<{}{}>)}{{[{}]{<><>}}[[{}<>]([][]}]}>){<<<[{}()][{}{}]>>>[[{<{}{}>[{}[]]}]<[
{[[(<([([{([<[()[]]<(){}>>[(<><>)[()()]]])}<{[[(<>[])([]{}>]{[[]<>]<{}[]>}]}[(((()<>)<()[]>
{{<(({([<<<<{([]()){()[]}}({()()})><(<()[]>[<>[]]}({<>{}}{[][]})>>{({<()[]>[{}<>]}((()[])(()<>)))}>>[(
{([[(({{{[[{<[{}()]<<>()>>[[()<>]{[]()}]}<[<{}()>{{}()}]{[[]<>](<>())}>]{({<(){}>(<>{})}{<[]>[[]()]}){<(
(<{<[(<[[<[{[[(){}][()()]]<[()<>]((){})>}[(<(){}>{<>{}>)]]{({{()}}{[{}<>]<<><>>})(({<>()}<{}()>)[{()}<<
[([([<{<((([[<[][]>{[]()}][<()<>><{}()>]]({[{}()]}[<()()>{[]<>}]))<[(<()()><()[]>){{[]<>}[()()]}]
{([<({[<((({(<{}<>>[{}()])<[<>{}]>})){{<<<[]()><[]<>>>{{<>()}[<>()]}>{[<()[]>[(){}]]})})<({
<<<[[[((<{[{[([])[()<>]]((<>{}}(()()))}<{<[][]><[]()>}{<(){}>{{}<>}}>]<([<<>>]<([][])({}{})>
<[[({[<([{<<<(()[])>{{(){}}<[]<>>)>>[{{{()<>}[{}()]}<{()[]}[()<>]>}<<{()()}([]())>[(<>()){<>{}}]>]}])[((((<{
⛄"""
