function factorial(n) {
    if (n < 2)
        return 1
    return factorial(n-1) * n
}

factorial(5)

