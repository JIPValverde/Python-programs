from mrjob.job import MRJob, MRStep

import string

class MRGrafos(MRJob):

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
				#print 'arista,[key, nodo]', 'arista',[key, nodo]
				yield key, nodo

	def reducer_02(self,key,values):
		# recibe las aristas, utilizando como key el primer nodo, cuenta el numero de aristas que tienen
		# al nodo en esa posicion, y crea una lista que luego devuelve con las apariciones del nodo Key
		nodos_secundarios = []
		grado_nodo_princ = 0
		for nodo in values:
			grado_nodo_princ += 1
			nodos_secundarios.append(nodo)
		for nodo in nodos_secundarios:
			#ordena las aristas antes de enviarlas
			if nodo > key:
				yield [key,nodo],[grado_nodo_princ,0]
			elif key > nodo:
				yield [nodo,key],[0,grado_nodo_princ]

	def reducer_03(self,key,values):
		# recibe dos aristas iguales, en una se da el grado del primer nodo y en la otra la del segundo
		# despues simplemente se suman los valores y se devuelve una unica arista con la lista de los 
		# grados de los nodos como value
		grado = [0,0]
		for grados in values:
			grado[0] += grados[0]
			grado[1] += grados[1]
		yield key,grado
		
	def steps(self):
        	return [MRStep(mapper = self.mapper,reducer = self.reducer_01),MRStep(reducer = self.reducer_02),MRStep(reducer = self.reducer_03)]

	
if __name__ == '__main__':
	import sys
	sys.stderr = open('localerrorlog.txt','w')
	MRGrafos.run()
