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

def proceso(nombre, env, ram, memoria, instrucciones, tiempo_instruccion):
    # Nuevo proceso creado
    yield env.timeout(random.expovariate(1.0 / INTERVALO))
    print(f'Proceso {nombre} creado en tiempo {env.now}, requiere {memoria} de RAM.')
    
    # Solicitar RAM
    yield ram.get(memoria)
    print(f'Proceso {nombre} obtuvo la RAM necesaria en tiempo {env.now}.')
    
    while instrucciones > 0:
        # Solicitar acceso al CPU
        with CPU.request() as req:
            yield req
            # Ejecutar instrucciones
            ejecutadas = min(instrucciones, tiempo_instruccion)
            yield env.timeout(ejecutadas)
            instrucciones -= ejecutadas
            print(f'Proceso {nombre} ejecutó {ejecutadas} instrucciones. {instrucciones} pendientes.')
        
        # Simular I/O o espera (opcional)
        if instrucciones:
            yield env.timeout(1)  # Simulación de operación de I/O
    
    # Liberar RAM
    yield ram.put(memoria)
    print(f'Proceso {nombre} terminado en tiempo {env.now}. Liberó {memoria} de RAM.')
    
# Crear procesos
for i in range(NUMERO_PROCESOS):
    memoria_requerida = random.randint(1, 10)  # Memoria requerida por proceso
    instrucciones = random.randint(1, 10)  # Instrucciones del proceso
    ENVIRONMENT.process(proceso(f'P{i}', ENVIRONMENT, RAM, memoria_requerida, instrucciones, 3))
    
# Iniciar la simulación
ENVIRONMENT.run()