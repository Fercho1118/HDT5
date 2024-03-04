import simpy
import random
import statistics

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
    #Registrar hora de inicio
    start_time = env.now
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
    TIEMPOS_EJECUCION.append(env.now - start_time)
    
# Crear procesos
for i in range(NUMERO_PROCESOS):
    memoria_requerida = random.randint(1, 10)  # Memoria requerida por proceso
    instrucciones = random.randint(1, 10)  # Instrucciones del proceso
    ENVIRONMENT.process(proceso(f'P{i}', ENVIRONMENT, RAM, memoria_requerida, instrucciones, 3))
    
# Iniciar la simulación
ENVIRONMENT.run()

#Calcular y mostrar estadísticas
tiempo_promedio = statistics.mean(TIEMPOS_EJECUCION)
desviacion_estandar = statistics.stdev(TIEMPOS_EJECUCION)
print(f'\nTiempo promedio de ejecución: {tiempo_promedio:.2f} unidades de tiempo.')
print(f'Desviación estándar del tiempo de ejecución: {desviacion_estandar:.2f} unidades de tiempo.')
