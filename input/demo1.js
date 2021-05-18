// This is a comment and the lexer will drop this


function findPythagorean(a, b) {
    log("Finding pythagorean of " + a + " and " + b + " ... ")
    return sqrt(a * a + b * b)
}



function main() {
    var side3 = findPythagorean(5, 12)
    log("The result is: " + side3)
}


main()

/* 
    This is also a comment
    but expands multiple lines
    and the lexer will drop this too
*/
