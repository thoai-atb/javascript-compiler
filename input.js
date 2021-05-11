function factorial(n) {
   if (n < 2)
      return 1
   var p = factorial(n - 1)
   return p * n
}

function add(a, b) {
   return a + b
}

var varone = 1
var vartwo = 2

factorial(add(varone, vartwo))