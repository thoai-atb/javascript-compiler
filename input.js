var side1 = 5
var side2 = 12

log("Side 1 is: " + side1)
log("Side 2 is: " + side2)

function findPythagorean(a, b) {
    log("Finding pythagorean of " + a + " and " + b + " ... ")
    return sqrt(a * a + b * b)
}

var side3 = findPythagorean(side1, side2)
log("The result is: " + side3)