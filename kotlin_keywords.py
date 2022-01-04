# File contains regexes responsible for coloring some keywords and operators from:
# https://kotlinlang.org/docs/keyword-reference.html#hard-keywords

# Changes msg to regex where msg is surrounded by at least one non-alphanumeric character
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
    r'\='
], "#E98400"


blue_colored = [
    r'\+', r'\-', r'\*', r'[^\/]\/[^\/]'
], "#4B93D2"

green_colored = [
    r'\d'
], "#10CE88"

purple_colored = [
    exact_keyword('object'),
    exact_keyword('interface'),
    exact_keyword('typeof'),
    exact_keyword('var'),
    exact_keyword('val'),
], "#EF00FF"

# Simple double slash comments, should pass high priority
grey_colored = [
    r'\/\/.*$', r'/'
], "#A4A4A4"

# Strings, high priority should be passed
yellow_colored = [
    r"([\"\'])(?:\\.|[^\\])*?\1"
], "#FAEE3C"
