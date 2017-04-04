import matplotlib.pylab as plt
import numpy as np
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

class Lagrange():
	def __init__(self,fig,ax):
		self.lista_puntos = []
		self.cid_click = fig.canvas.mpl_connect('button_press_event', self.raton_presionado)
        	self.cid_movimiento = fig.canvas.mpl_connect('motion_notify_event', self.raton_movido)
        	self.cid_suelta_raton = fig.canvas.mpl_connect('button_release_event', self.raton_soltado)
		self.lista_centros = []		
		self.fig = fig
		self.ax = ax
		self.punto_tocado = None
		self.t = np.linspace (-20,20,100,endpoint = True)
		self.puntos_control = None

	def raton_presionado(self, event):
		if event.button == 3:
	            fig.canvas.mpl_disconnect(self.cid_click)
	            fig.canvas.mpl_disconnect(self.cid_movimiento)
	            fig.canvas.mpl_disconnect(self.cid_suelta_raton)
	            return
	            
	        for punto in self.lista_puntos:
	            contiene, attr = punto.contains(event)
	            if contiene:
	                self.punto_tocado = punto
	                self.x0_inicial, self.y0_inicial = punto.center  
	                self.click_event = event
	                return
        
	        centro = (event.xdata, event.ydata)
	        c = Circle(centro, 0.5)
	        self.lista_puntos.append(c)
		self.lista_centros.append(centro)
        	self.puntos_control = np.array([punto.center for punto in self.lista_puntos])
		if len(self.lista_centros) > 0:
			self.curva = Line2D(self.t,self.lagrange(self.t))	
	        self.ax.add_patch(c)
	      	self.curva.set_xdata(self.t)
        	self.curva.set_ydata(self.lagrange(self.t))
		if len(self.lista_centros) > 1:
			del self.ax.lines[-1]
        	self.ax.add_line(self.curva)
		self.fig.canvas.draw()

	def raton_soltado(self, event):
	        self.punto_tocado = None
	        return

	def raton_movido(self, event):
	        if self.punto_tocado == None:
	            return
	        dx = event.xdata - self.click_event.xdata
	        dy = event.ydata - self.click_event.ydata
	        self.punto_tocado.center = self.x0_inicial + dx, self.y0_inicial + dy
		self.lista_centros = []
		for punto in self.lista_puntos:
			self.lista_centros.append(punto.center)
		self.puntos_control = np.array([punto.center for puntos in self.lista_puntos])
	      	self.curva.set_xdata(self.t)
        	self.curva.set_ydata(self.lagrange(self.t))
		self.fig.canvas.draw()

	def lagrange(self,t):	
		x0 = self.t
		x1 = np.array([self.inter_lagrange(x0)])
		return x1		
			
	def inter_lagrange(self,x0):
			tamano_lista = len(self.lista_centros)
			i = 0
			x1 = 0
			while i <= (tamano_lista -1):		
				L = 1
				j = 0
				while j <= tamano_lista - 1:
					if not(i == j):
						L = L * ((x0 - self.lista_centros[j][0])/(self.lista_centros[i][0] - self.lista_centros[j][0]))
					j = j+1
				x1 = x1+L*self.lista_centros[i][1]
				i = i+1
			return x1


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
dibuja_curva = Lagrange(fig, ax)
plt.show()
