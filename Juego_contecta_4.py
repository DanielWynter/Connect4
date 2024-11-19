#from IPython.display import display #esto sirve para la presentacion y que se vea bonito
import numpy as np
import time
#estaremos usando estas librarias para el progama
from sympy import init_printing, Matrix #esto sirve para que la matriz de presnete limpiamente
import os
init_printing()#esta linea nos ayudara con la estetica del programa, para que se vea una presentacion limpia

class cuatro_en_linea: #las clase sera ecencial para el programa
#nota:investigar que es una clase
  def __init__(self): #esta funcion es la que inicia el programa y nos da el menu de seleccion
    print("1. Jugador VS Computadora")
    print("2. Jugador VS Jugador")
    seleccion = input("seleccione el modo de juego: ") #aqui el usuario definira
    seleccion = self.comprobar_seleccion(seleccion)#comprobara su el ususario pone una opcion valida
    self.modo = int(seleccion)+1 #guardara el modo de juego seleccionado por el jugador
    self.tablero = np.zeros((6,7)).astype(int) #crea el tablero segun las espesificaciones que le demos, la crea usando una matriz
    self.opciones = [0,1,2,3,4,5,6] #una lista de las opciones de las columnas del tablero
    self.columnas_llenas = set()#nos hace un congunto de las colunas que ya estan llenas, asi le damos un seguimiento al tablero

  def comprobar_seleccion(self, seleccion, columnas_llenas=set()):#esta funcion nos ayuda a comprobar que los usuarios den valores correctos con respecto a los opciones, tomando como parametros laa veriables escritas dentro
    while True: #esto nos ayudara a seguir pidiendo un valor hasta que la respuesta sea valida
      if not seleccion.isdigit(): #verificara que el valor dado sea un numero entero
        seleccion = input("No valido, debes ingresar un numero: ")
      elif int(seleccion) - 1 < 0 or int(seleccion) - 1 > 6 or int(seleccion) - 1 in columnas_llenas:#verificara que la columna seleccionada todavia sea valida
        seleccion = input(f"Seleccion no valida, escoja otra columnna: ")
      else:
        break
    return int(seleccion) -1 #ponemos el -1 porque la primera columna en pyton es cero

  def comprobar_ganar(self,booleano,cadena): #esta fuincion verificara que un jugador haya ganado
    #comprobar la filas
    for fila in booleano:
      #solo si hay por lo menos 4
      if sum(fila) >= 4:
        # if 4 in a fila
        if sum(fila[:4]) >= 4 or sum(fila[1:5]) >= 4 or sum(fila[2:6]) >= 4 or sum(fila[3:]) >=4:
          return True, f'¡{cadena} ganó! 4 en una fila'

    #comprobar las columnas
    for fila in booleano.T:
      # solo si hay por lo menos 4
      if sum(fila) >= 4:
        #if 4 in a fila
        if sum(fila[:4]) >= 4 or sum(fila[1:5]) >= 4 or sum(fila[2:6]) >= 4 or sum(fila[3:]) >=4:
          return True, f'¡{cadena} ganó! 4 en una columna'

    # comprobar las diagonales
    for k in range (-2,4): #comprobar la diagonales es una tera mas complicada por lo que usaremos funciones de la libreria numpy
      #usaremos la funcion diag, esta nos da los numero en diganal de una matriz
      if sum(np.diag(booleano,k)) >= 4: #establece si hay 4 en la diganola
        if sum(np.diag(booleano,k)[:4]) >=4 or sum(np.diag(booleano,k)[::-1][:4]) >=4:#nos ayudara a saber si estan consecutivas con la indexcion de matriz
          return True, f'{cadena} gano! 4 en diagonal!'
      if sum(np.diag(np.rot90(booleano),k-1)) >=4: #con esto checaremos la direccion de la diagonal
        if sum(np.diag(np.rot90(booleano),k-1)[:4]) >=4 or sum(np.diag(np.rot90(booleano),k-1)[::-1][:4]) >=4:
          return True, f'¡{cadena} ganó! 4 en una columna'

    return False, '' #esto singnifica que el jugador no ha ganado

  def turno(self, jugador, computadora, seleccion=''): #funcion para el turno
    os.system('clear') #despeja el espacio
    display(Matrix(self.tablero)) #muestra el tablero como una matriz
    if not computadora:
      seleccion = input(f"jugador {jugador}, seleccione una columna: ") #el usuario debe seleccionar una columna
      seleccion = self.comprobar_seleccion(seleccion) #combrobar seleccion

    seleccion = int(seleccion)  # Convertir a número entero

    if np.prod(self.tablero[:, seleccion]) != 0: #combrobar si la columna esta llena
        self.columnas_llenas.add(seleccion) # si la computadora escogio una columna llena
        if computadora:
            self.opciones.remove(seleccion) #la computadora no volvera a seleccionar esa columna
            seleccion = np.random.choice(self.opciones) #escogera otra columna
        else:#si no es una compurtadora
            s = input("Esta columna esta llena, por favor seleccione otra: ")
            seleccion = self.comprobar_seleccion(s, columnas_llenas=self.columnas_llenas)

    if sum(self.tablero[:, seleccion]) != 0:  #verificacion de la fila
        fila = np.argmax((self.tablero > 0)[:, seleccion]) - 1
    else:
        fila = -1
    if not computadora: #la ficha del jugador
        self.tablero[fila, seleccion] = int(jugador)
    else:
        self.tablero[fila, seleccion] = 3 #la ficha de la computadora

  def jugar(self): #funcion para jugar ;)
    while True: #esta funcion continuara hasta que alguin gane
      #jugador 1 turno
      time.sleep(.3)
      self.turno('1', computadora=False, seleccion='') #turno del jugador
      win, cadena = self.comprobar_ganar(self.tablero == 1, 'jugador') #comprobar si el jugador 1 gano
      if win: #si es verdad gana el jugador 1
        time.sleep(.3)
        os.system('clear')
        display(Matrix(self.tablero))
        print(cadena)
        break
         #turno de la computadora
      if self.modo == 1:  #esto hace que al seleccionar y jugar contra la computadora seleccione columnas aleatorias
        time.sleep(.3)
        self.turno('CPU', computadora=True, seleccion=np.random.choice(self.opciones))
        cadena = 'computadora'
        win, cadena = self.comprobar_ganar(self.tablero == 3, cadena)

      else: #turno para jugador 2
        time.sleep(.3)
        self.turno('2', computadora=False, seleccion='')
        cadena = 'jugador 2'
        win, cadena = self.comprobar_ganar(self.tablero == 2, cadena)

      if win:  #ganador jugador 2 o computadora
        time.sleep(.3)
        os.system('clear')
        display(Matrix(self.tablero))
        print(cadena)
        break

if __name__ == '__main__':
  cuatro_en_linea().jugar()