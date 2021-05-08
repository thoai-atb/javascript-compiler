function mult(a, b) {
   return a * b / 0
}

function compound(a, b, c) {
   return a + mult(b, c)
}

var c = compound(10, 3, 2)

