def triangulo_pascal_recursivo(filas, columna=0):
  if filas == 0 or columna == 0 or filas == columna:
      return 1
  else:
      return triangulo_pascal_recursivo(filas - 1, columna - 1) + triangulo_pascal_recursivo(filas - 1, columna)

def imprimir_triangulo_pascal(filas):
  espacios = filas + 1
  for i in range(filas):
    print(espacios*' ',end=' ')
    for j in range(i + 1):
      print('▲', end=' ')
    espacios -= 1
    print()
imprimir_triangulo_pascal(11)