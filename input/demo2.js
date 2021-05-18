function factorial(n) {
    if (n < 2) return 1
    var n_1 = factorial(n-1)
    return n * n_1
}

function main() {
    var a = factorial(4)
    log(a)
}

main()