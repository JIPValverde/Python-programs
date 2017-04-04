from mrjob.job import MRJob, MRStep
import string

class MRTriciclos(MRJob):

	SORT_VALUES = True
	
	def mapper(self,_,line):
		#extrae las aristas del fichero de texto, las convierte en pares de la forma [a,b] 
		#y los envia al reducer del derecho y del reves, mientras se encarga de filtrar los ciclos [a,a].
		line = line.replace('"',"")
		grafo = line.split(',')
		if grafo[0] < grafo[1]:
			yield grafo[0] , grafo[1]
			yield grafo[1] , grafo[0]
		elif grafo[0] > grafo[1]: 
			yield grafo[0] , grafo[1]
			yield grafo[1] , grafo[0]
	
	def reducer_01(self,key,values):
		#se encarga de quitar las aristas repetidas
		grafo_total = []
		for nodo in values:
			if [key, nodo] not in grafo_total:
				grafo_total.append([key, nodo])
				yield key, nodo
	
	def reducer_02(self,key,values):
		# recibe las aristas, utilizando como key el primer nodo, cuenta el numero de aristas que tienen
		# al nodo en esa posicion, y crea una lista que luego devuelve con una lista de los nodos secundarios 
		#asociados
		nodos_secundarios = []
		for nodo in values:
			nodos_secundarios.append(nodo)
		for nodo in nodos_secundarios:
			#Ordena las aristas antes de enviarlas
			if nodo > key:
				yield [key,nodo],[nodos_secundarios,0]
			elif key > nodo:
				yield [nodo,key],[0,nodos_secundarios]
	
	def reducer_03(self,key,values):
		# comprueba los nodos relacionados con el nodo de la izquierda y de la derecha
		# en caso de que algun nodo coincida se guarda la terna [nodo_izq,nodo_der,nodo_encontrado]
		# ordenada siempre y cuando no este ya en una lista auxiliar (para evitar repeticines)
		nodos_usados = []
		nodos_izq = []
		nodos_der = []
		triangulos_usados=[]
		for nodos in values:
			if nodos[0] != 0:
				nodos_izq = nodos[0]
			if nodos[1] != 0:
				nodos_der = nodos[1]
		if len(nodos_izq) > 1 and len(nodos_der) > 1:
			for nodo_1 in nodos_izq:
				for nodo_2 in nodos_der:
					if nodo_1 == nodo_2:
						nodos_usados.append(nodo_1)
						triangulo = sorted([key[0],key[1],nodo_1])
						if triangulo not in triangulos_usados:
							triangulos_usados.append(triangulo)
							yield triangulo,triangulo

	def reducer_04(self,key,values):
		#hace una ultima criba para evitar repeticiones
		triangulos_usados = []
		for triangulo in values:
			if triangulo not in triangulos_usados:
				triangulos_usados.append(triangulo)
				yield triangulo,None

	def steps(self):
        	return [MRStep(mapper = self.mapper,reducer = self.reducer_01),MRStep(reducer = self.reducer_02),MRStep(reducer = self.reducer_03),MRStep(reducer = self.reducer_04)]

	
if __name__ == '__main__':
	import sys
	sys.stderr = open('localerrorlog.txt','w')
	MRTriciclos.run()
