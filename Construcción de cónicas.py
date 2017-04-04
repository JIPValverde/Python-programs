import matplotlib.pylab as plt
import numpy as np
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

class Conica: #definimos la conica
    def __init__(self, fig, ax):

        self.lista_circulos = []  
        # movimientos y clicks del raton
        self.cid_click = fig.canvas.mpl_connect('button_press_event', self.raton_presionado)
        self.cid_movimiento = fig.canvas.mpl_connect('motion_notify_event', self.raton_movido)
        self.cid_suelta_raton = fig.canvas.mpl_connect('button_release_event', self.raton_soltado)
        #coordenadas del nuevo punto
        self.x_inicial = None
        self.y_inicial = None          
        self.circulo_tocado = None
        self.puntos = None
        #datos de la funcion que define las conicas
        self.datos_funcion = None         
        # grafica de la figura
        self.contorno = None      
        self.fig = fig
        self.ax = ax
        # entre que valores se pueden encontrar los puntos 
        self.x = np.arange(-20.0, 20.0, 1)
        self.y = np.arange(-20.0, 20.0, 1)
        # coordenadas de los puntos x, y dadas como matrices
        self.xx, self.yy = np.meshgrid(self.x, self.y)
        

    def raton_presionado(self, event):
        # aplicaciones de pulsar el primer boton del raton 
        if event.button == 3:
            fig.canvas.mpl_disconnect(self.cid_click)
            fig.canvas.mpl_disconnect(self.cid_movimiento)
            fig.canvas.mpl_disconnect(self.cid_suelta_raton)
            return

        for  circulo in self.lista_circulos:
            contiene, attr = circulo.contains(event)
            if contiene:
                self.circulo_tocado = circulo
                self.x_inicial, self.y_inicial = circulo.center
                self.click_event = event
                return
        #datos de los circulos
        centro = (event.xdata, event.ydata)
        c = Circle(centro, 0.5)
        self.lista_circulos.append(c)
        self.puntos = np.array([circulo.center for circulo in self.lista_circulos])
        # matriz que define la conica que estamos creando
        Matriz = self.Matriz()
        m, e, mu = np.linalg.svd(Matriz)
        # matriz unitaria
        self.datos_funcion = mu[5]  
   
        for circulo in self.lista_circulos:
            self.ax.add_patch(circulo)

        # si el circulo pertenece a la grafica de la funcion
        if self.contorno == None:        
            self.zz = self.funcion(self.xx, self.yy)
            self.contorno = plt.contour(self.xx, self.yy, self.zz, [0], colors = 'green')

        # si el circulo no pertenece a la grafica de la funcion
        if not self.contorno == None:
            self.zz = self.funcion(self.xx, self.yy)
            del self.ax.collections[0]
            self.contorno = plt.contour(self.xx, self.yy, self.zz, [0], colors = 'green')
            
        self.ax.add_patch(c)
        self.fig.canvas.draw()

    def raton_soltado(self, event):
        # soltamos el raton
        self.circulo_tocado = None
		
    def raton_movido(self, event):
        #lo que ocurre si movemos el raton
        if self.circulo_tocado == None:
            return
        # modificamos los datos del punto en base a los movimientos del raton para que se mueva
        dx = event.xdata - self.click_event.xdata
        dy = event.ydata - self.click_event.ydata
        self.circulo_tocado.center = self.x_inicial + dx, self.y_inicial + dy
        self.puntos = np.array([circulo.center for circulo in self.lista_circulos])
        #Matriz de la conica
        Matriz = self.Matriz()
        m, e, mu = np.linalg.svd(Matriz)
        # matriz unitaria de la conica
        self.datos_funcion = mu[5]

        # si el punto pertence a la grafica de la funcion
        if self.contorno == None:
            self.zz = self.funcion(self.xx, self.yy)
            self.contorno = plt.contour(self.xx, self.yy, self.zz, [0], colors = 'green')

        # si el punto no pertenece a la grafica de la funcion
        if not self.contorno == None:
            self.zz = self.funcion(self.xx, self.yy)
            del self.ax.collections[0]
            self.contorno = plt.contour(self.xx, self.yy, self.zz, [0], colors = 'green')

        for circulo in self.lista_circulos:
            self.ax.add_patch(circulo)
        #dibuja la figura
        self.fig.canvas.draw()
        
    # funcion de la conica
    def funcion(self, x, y):

        funcion_de_la_conica = np.dot(self.datos_funcion, np.array([x**2, y**2, 2*x*y, 2*x, 2*y, 1]))
        return funcion_de_la_conica
    # matriz de la conica
    def Matriz(self):

        Matriz_de_la_conica = [np.array([(punto[0])**2, (punto[1])**2, 2 * (punto[0]) * (punto[1]), 2 * (punto[0]), 2 * (punto[1]), 1]) for punto in self.puntos]
        return Matriz_de_la_conica

fig = plt.figure()
ax = fig.add_subplot(111)
ax.axis("image")  
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
dibuja_curva = Conica(fig, ax)
# inicia la grafica
plt.show()
