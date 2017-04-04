# -*- coding: utf-8 -*-

from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Lock
from multiprocessing.connection import AuthenticationError
import random

proporcion_alimento = 120
size = (1200,800)
numero_virus = 30
tamanio_inicial_celulas = 10

def serve_client(conn,id, tablero_celulas,tablero_alimentos,tablero_virus,lock,nombre):
	#programa principal, se encarga de la comunicacion con los jugadores asi como las modificacions de los tableros
	nuevo_id(tablero_celulas,id[1],nombre)
	m = tablero_celulas[id[1]][0]
	while True:	
		lock.acquire()
		modificar_tablero_alimentos(tablero_celulas,tablero_alimentos)	
		lock.release()
		#print 'tablero = ', tablero
		#print 'tablero alimentos = ', tablero_alimentos
	        answer = [id[1],tablero_celulas.copy(),tablero_alimentos.copy(),tablero_virus.copy()]
	        try:
			#print 'el tablero enviado es ', answer
			
			conn.send(answer)
	        except IOError:
	            print 'No send, connection abruptly closed by client'
	            break
	        try:
	            m = conn.recv()
	        except EOFError:
	            print 'No receive, connection abruptly closed by client'
	            break
	        #print 'received message:', m, 'from', id
		lock.acquire()	
	       	modificar_tablero(tablero_celulas,id,m,nombre)
		lock.release()
	
	conn.close()
	print 'connection', id, 'closed'

def nuevo_id(tablero_celulas,id,nombre):
	#Crea un nuevo jugador
	color = color_aleatorio()
	tablero_celulas[id] = [[random.randint(0,size[0]),random.randint(0,size[1])],tamanio_inicial_celulas,color,nombre] 

def modificar_tablero(tablero_celulas,id,m,nombre):
	#actualiza el tablero de celulas, jugadores
	if id[1] in tablero_celulas:
		antigua_posicion = [0,0]
		antigua_posicion[0] = tablero_celulas[id[1]][0][0]
		antigua_posicion[1] = tablero_celulas[id[1]][0][1]
		tamanio = tablero_celulas[id[1]][1]
		color = tablero_celulas[id[1]][2]
		nombre = tablero_celulas[id[1]][3]
		nueva_posicion = posicion_velocidad(antigua_posicion,m,tamanio)
		tablero_celulas[id[1]] = [antigua_posicion, tamanio, color,nombre]
		alimentarse(id[1],tablero_celulas,tablero_alimentos)
		comer_jugadores(id[1],tablero_celulas)

def posicion_velocidad(antigua_posicion,posicion_tmp,tamanio):
	# mueve la celula del jugador en base a una velocidad calculada en funcion 
	dir1 = posicion_tmp[0] - antigua_posicion[0]
	dir2 = posicion_tmp[1] - antigua_posicion[1]
	velocidad = 80.0/tamanio
	# if norma(dir1,dir2) != 0 
	if norma(dir1,dir2) >= 5:
		antigua_posicion[0] += velocidad*dir1/norma(dir1, dir2) 
        	antigua_posicion[1] += velocidad*dir2/norma(dir1, dir2) 
	nueva_posicion = [antigua_posicion[0],antigua_posicion[1]]
	return nueva_posicion

def norma(x,y):
	#calcula la longitud de un vector
	norm = ((x)**2.0 + (y)**2.0)**(1/2.0)
	return norm

def modificar_tablero_alimentos(tablero_celulas,tablero_alimentos):
	#Creo la comida con color y posicion aleatoria	
	while len(tablero_alimentos) < (size[0]/size[1])*proporcion_alimento :
		tablero_alimentos[len(tablero_alimentos)] = [[random.randint(0,size[0]),random.randint(0,size[1])],color_aleatorio()]

def modificar_tablero_virus(tablero_virus):
	#Crea los virus con posicion aleatorio
	while len(tablero_virus) < numero_virus:
		tablero_virus[len(tablero_virus)] = [[random.randint(0,size[0]),random.randint(0,size[1])],"Black"]

def alimentarse(id,tablero_celulas,tablero_alimentos):
	#comprueba si la celula del jugador puede comer algun alimento
	jugador = tablero_celulas[id]
	for i in range(len(tablero_alimentos)):
		if distancia(jugador[0],tablero_alimentos[i][0]) < jugador[1]/2:
			alimento_comido(i,tablero_alimentos)
			modificar_radio_jugador(id,tablero_celulas,1)

def distancia(pos1,pos2):
	#calcula la distancia entre dos posiciones
	dis = ((pos1[0]-pos2[0])**2.0 + (pos1[1]-pos2[1])**2.0)**(1/2.0)
	return dis

def alimento_comido(alimento,tablero_alimentos):
	# modifica  la posicion de un alimento comido
	nueva_pos = [random.randint(0,size[0]),random.randint(0,size[1])]
	tablero_alimentos[alimento] = [nueva_pos,color_aleatorio()]
	tablero_alimentos[alimento][0] = nueva_pos

def comer_jugadores(id,tablero_celulas):
	#comprueba si el jugador come o es comido
	if id in tablero_celulas:
		jugador = tablero_celulas[id]
		for id2,value in tablero_celulas.items(): 
			if id2 != id: 
				dist = distancia(jugador[0],tablero_celulas[id2][0])
				tamanio_1 = jugador[1]
				tamanio_2 = tablero_celulas[id2][1]
				if  dist < tamanio_1/2:
					tablero_celulas = borrar_jugador(id2,tablero_celulas)
					modificar_radio_jugador(id,tablero_celulas,tablero_celulas[id][1]/2)
				elif dist < tamanio_2/2:
					tablero_celulas = borrar_jugador(id,tablero_celulas)					
					modificar_radio_jugador(id2,tablero_celulas,tablero_celulas[id2][1]/2)

def borrar_jugador(id,tablero_celulas):
	#borra un jugador del tablero de celulas
	tablero_celulas.pop(id)
	print "se ha eliminado a id",id
	return tablero_celulas

def modificar_radio_jugador(id,tablero_celulas,variacion):
	#aumenta o disminuye el radio de la celula a la que corresponde la id
	tablero_celulas[id] = [tablero_celulas[id][0],tablero_celulas[id][1]+variacion,tablero_celulas[id][2],tablero_celulas[id][3]]


def color_aleatorio():
	#da un color aleatorio en hexadecimal
	hex = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
	color = "#"
	for i in range(6):
		num = random.randint(0,len(hex)-1)
		color = color + hex[num]
	return color

if __name__ == '__main__':
	listener = Listener(address=('127.0.0.1', 6000), authkey='secret password')
	#listener = Listener(address=("147.96.18.76", 6000), authkey='secret password')
	print 'listener starting'
	manager = Manager()
	tablero_celulas = manager.dict()
	tablero_alimentos = manager.dict()
	tablero_virus = manager.dict()
	lock = Lock()
	lock.acquire()
	modificar_tablero_virus(tablero_virus)
	lock.release()
	while True:
	        print 'accepting conexions'
	        try:
	            conn = listener.accept()                
	            print 'connection accepted from', listener.last_accepted
                    nombre = conn.recv()
	            p = Process(target=serve_client, args=(conn,listener.last_accepted,tablero_celulas,tablero_alimentos,tablero_virus,lock,nombre))
	            p.start()
	        except AuthenticationError:
	            print 'Connection refused, incorrect password'
	listener.close()
	print 'end'
