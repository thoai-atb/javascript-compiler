THIS PROGRAM IS BASED ON THIS YOUTUBE PLAYLIST: https://www.youtube.com/playlist?list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD

HERE IS THE LIST OF THINGS THAT ARE DONE DIFFERENT FROM THE TUTORIAL:

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