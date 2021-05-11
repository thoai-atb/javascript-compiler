function factorial(n) {
   if (n < 2)
      return 1
   var p = factorial(n - 1)
   return p * n
}

var sample = 0

if (sample == 0) 
   factorial(3)
else
   factorial(5)