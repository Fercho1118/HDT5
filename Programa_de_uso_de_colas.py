import simpy
import random

#Configuración de la simulación
ENVIRONMENT = simpy.Environment()
RAM = simpy.Container(ENVIRONMENT, init=100, capacity=100)
CPU = simpy.Resource(ENVIRONMENT, capacity=1)
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
TIEMPOS_EJECUCION = []
NUMERO_PROCESOS = 25
INTERVALO = 10