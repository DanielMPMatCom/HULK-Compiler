def fib(n):
    if n <= 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

# Calcular el valor de Fibonacci para 10
resultado = fib(30)
print(resultado)