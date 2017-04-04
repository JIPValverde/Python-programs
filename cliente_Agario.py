from multiprocessing.connection import Client
from multiprocessing import Manager
from Tkinter import Tk, Frame, Canvas, Label
import tkFont

size = [1200,800]
posicion = [150,150]
tamanio_alimento = 5
tamanio_virus = 30

print "trying to connect"

conn = Client(address=('127.0.0.1', 6000), authkey='secret password')
#conn = Client(address=('147.96.18.75', 6000), authkey='secret password')
	
print 'connection accepted'
nombre = raw_input('Dime tu nombre ')
#nombre = "Jose"

window = Tk()
window.title("Jose Ignacio agar.io")    
  	
frame = Frame(window)
frame.pack()
	
canvas = Canvas(frame, width=size[0], height=size[1], bg='#FFFFFF') 
canvas.pack()

def motion(event):
	# devuelve la posicion del raton
	x = event.x 
	y = event.y 
	global posicion
	posicion = [x, y]

window.bind('<Motion>', motion)

def dibujar_tablero(canvas,tablero):
	#Dibuja el tablero de las celulas
	for key in tablero:
		#print 'key ', key
		pos, tamanio, color, nombre = tablero[key]
		canvas.create_oval(pos[0]+tamanio/2,pos[1]+tamanio/2,pos[0]-tamanio/2,pos[1]-tamanio/2,fill = color)
		canvas.create_text(pos[0],pos[1],text=nombre)


def dibujar_tablero_alimentos(canvas,tablero_alimentos):
	#Dibuja el tablero de los alimentos
	t = tamanio_alimento
	for key in tablero_alimentos:
		#print 'key ', key
		pos, color = tablero_alimentos[key]
		canvas.create_oval(pos[0]+t/2,pos[1]+t/2,pos[0]-t/2,pos[1]-t/2,fill = color)

def dibujar_tablero_virus(canvas,tablero_virus):
	#Dibuja el tablero de los virus
	t = tamanio_virus
	for key in tablero_virus:
		#print 'key ', key
		pos, color = tablero_virus[key]
		canvas.create_oval(pos[0]+t/2,pos[1]+t/2,pos[0]-t/2,pos[1]-t/2,fill = color)

def mostrar_game_over(canvas):
	#Muestra un game over por pantalla
	mensaje = tkFont.Font(family = "Helvetica", size= 50, weight = "bold")
	canvas.create_text(size[0]/2,size[1]/2,text="Game Over",fill= "#FF0000",font = mensaje)	

#print 'trying to connect'
conn.send(nombre)
while True:   
		message = posicion
    		tablero_total = conn.recv() 
		#print 'tablero', tablero_total
		identidad = tablero_total[0]
		tablero = tablero_total[1]
		tablero_alimentos = tablero_total[2]
		tablero_virus = tablero_total[3]
		#print 'el tablero es ', tablero
		canvas.delete('all')
		dibujar_tablero_alimentos(canvas,tablero_alimentos)
		dibujar_tablero(canvas,tablero)
		dibujar_tablero_virus(canvas,tablero_virus)
		if identidad not in tablero:
			mostrar_game_over(canvas)
		conn.send(message)
    		window.update() 
conn.close()

