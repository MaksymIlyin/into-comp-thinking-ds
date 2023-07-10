def fib(n):
    if n in {0, 1}:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def fast_fib(n, memo={}):
    if n in {0, 1}:
        return 1
    try:
        return memo[n]
    except KeyError:
        result = fast_fib(n-1, memo) + fast_fib(n-2, memo)
        memo[n] = result
        return result


if __name__ == '__main__':
    for i in range(121):
        print(f'Fib({i})={fast_fib(i)}')
