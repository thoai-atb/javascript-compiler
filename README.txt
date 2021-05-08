THIS PROGRAM IS BASED ON THIS YOUTUBE PLAYLIST: https://www.youtube.com/playlist?list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD

HERE IS THE LIST OF THINGS THAT ARE DONE DIFFERENT FROM THE TUTORIAL:

HELLO WORLD 

ep 2:
    don't need to wrap res.register for self.advance()

ep bonus (power):
    grammar = {
        expr : term ((PLUS | MINUS) term) *
        term : factor ((MUL | DIV) factor) *
        factor: atom (^ atom) *
        atom: (PLUS | MINUS) atom 
            :   INT | FLOAT
            : LPAREN expr RPAREN
    }

ep 4:
    don't add advancement count and other jazz for parse_result class

ep 5:
    comp_expr in parser: just return the res, don't need to make new error
    in bin_op: more checks
    in symbol table: added check if name in symbols list

changed:
    and -> &&
    or -> ||
    not -> !

function:
    don't create new interpreter, only 1 interpreter exists

/////////////////////// IN PPTREE:

Fix order by changing to this:
    a = children(current_node)
    b = []
    while a and sum(size_branch[node] for node in b) < sum(size_branch[node] for node in a):
        b.insert(0, a.pop())
