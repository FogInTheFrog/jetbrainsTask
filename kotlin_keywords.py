# File contains regexes responsible for coloring some keywords and operators from:
# https://kotlinlang.org/docs/keyword-reference.html#hard-keywords

# Word to regex where there is word surrounded by non-alphanumeric
def exact_keyword(msg):
    return r'(?:^|\W)' + msg + r'(?:$|\W)'


orange_colored = [
    exact_keyword('true'),
    exact_keyword('false'),
    exact_keyword('def'),
    exact_keyword('break'),
    exact_keyword('if'),
    exact_keyword('for'),
    exact_keyword('else'),
    exact_keyword('in'),
    exact_keyword('is'),
    exact_keyword(','),
    exact_keyword('null'),
    exact_keyword('super'),
    exact_keyword('this'),
    exact_keyword('when'),
    exact_keyword('while'),
], "#E98400"


blue_colored = [
    '+', '-', '=', '/'
], "#4B93D2"

green_colored = [
    r"([\"\'])(?:(?=(\\?))\2.)*?\1"
], "#10CE88"

purple_colored = [
    exact_keyword('object'),
    exact_keyword('interface'),
    exact_keyword('typeof'),
    exact_keyword('var'),
    exact_keyword('val'),
], "#6D03C9"
