from datetime import datetime

# Función para simular y registrar la respuesta al incidente
def registrar_respuesta(usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("respuesta.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha}, USUARIO_BLOQUEADO, {usuario}\n")
    return fecha

intentos = {}

# Leer eventos registrados en el log
try:
    with open("eventos.log", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = [p.strip() for p in linea.strip().split(",")]
            if len(partes) >= 3:
                fecha, tipo, usuario = partes[0], partes[1], partes[2]
                if tipo == "LOGIN_FALLIDO":
                    if usuario not in intentos:
                        intentos[usuario] = []
                    intentos[usuario].append(fecha)
except FileNotFoundError:
    print("El archivo eventos.log aún no existe. Genera eventos primero en la aplicación web.")

# Evaluar intentos y calcular métricas MTTD y MTTR
for usuario, registros in intentos.items():
    if len(registros) >= 3:
        print("ALERTA DE SEGURIDAD")
        print("Usuario:", usuario)
        print("Intentos fallidos:", len(registros))
        print("Primer intento:", registros[0])
        print("Detección:", registros[2])

        # Registrar la acción de respuesta
        fecha_respuesta = registrar_respuesta(usuario)
        print("Acción aplicada: bloqueo de usuario")
        print("Respuesta:", fecha_respuesta)

        # Cálculo de fechas
        inicio = datetime.strptime(registros[0], "%Y-%m-%d %H:%M:%S")
        deteccion = datetime.strptime(registros[2], "%Y-%m-%d %H:%M:%S")
        respuesta = datetime.strptime(fecha_respuesta, "%Y-%m-%d %H:%M:%S")

        # Cálculo de métricas
        mttd = (deteccion - inicio).total_seconds()
        mttr = (respuesta - deteccion).total_seconds()

        print("MTTD:", mttd, "segundos")
        print("MTTR:", mttr, "segundos")
        print("-" * 30)