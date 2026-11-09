# tp02 - programacion i - controlador de misiones
# grupo 3
# comision: ....................

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO



def es_numero(valor):
    return type(valor) == int or type(valor) == float



def comando_es_valido(comando):
    tipos_validos = ("avanzar", "girar", "detenerse", "saludar")

    if type(comando) != tuple and type(comando) != list:
        return False
    if len(comando) == 0:
        return False

    tipo = comando[0]
    if tipo not in tipos_validos:
        return False

    if tipo == "avanzar" or tipo == "girar":
        if len(comando) != 3:
            return False
        velocidad = comando[1]
        tiempo = comando[2]
        if not es_numero(velocidad) or not es_numero(tiempo):
            return False
        if tiempo <= 0:
            return False
    elif len(comando) != 1:
        return False

    return True



def ejecutar_comando(robot, comando):
    tipo = comando[0]
    try:
        if tipo == "avanzar":
            velocidad = comando[1]
            tiempo = comando[2]
            robot.avanzar(velocidad=velocidad, tiempo=tiempo)
            return f"avanzar ejecutado (velocidad={velocidad} m/s, tiempo={tiempo} s)"
        elif tipo == "girar":
            velocidad = comando[1]
            tiempo = comando[2]
            robot.girar(velocidad=velocidad, tiempo=tiempo)
            return f"girar ejecutado (velocidad={velocidad} rad/s, tiempo={tiempo} s)"
        elif tipo == "detenerse":
            robot.detenerse()
            return "detenerse ejecutado"
        elif tipo == "saludar":
            robot.saludar()
            return "saludar ejecutado"
    except ErrorDeSeguridad as e:
        return f"RECHAZADO por el robot: {e}"

    # no deberia pasar si se valido antes, pero asi nunca devuelve None
    return "RECHAZADO: tipo desconocido"



def ejecutar_mision(robot, mision, historial):
    print(f"\n=== Iniciando mision: {len(mision)} comando(s) ===")

    for comando in mision:
        registro = {"comando": comando, "ejecutado": False, "distancia": 0, "tiempo": 0}

        if not comando_es_valido(comando):
            registro["motivo"] = "Comando invalido (formato o tipo incorrecto)"
            print(f"[OMITIDO] {comando} -> {registro['motivo']}")
            historial.append(registro)
            continue

        resultado = ejecutar_comando(robot, comando)
        registro["motivo"] = resultado

        if resultado.startswith("RECHAZADO"):
            print(f"[OMITIDO] {comando} -> {resultado}")
        else:
            registro["ejecutado"] = True
            # para el reporte: distancia = velocidad x tiempo
            if comando[0] == "avanzar" or comando[0] == "girar":
                registro["tiempo"] = comando[2]
            if comando[0] == "avanzar":
                registro["distancia"] = abs(comando[1] * comando[2])
            print(f"[OK] {resultado}")

        historial.append(registro)

    print(" Mision finalizada \n")



def generar_reporte(historial):
    total = len(historial)
    ejecutados = 0
    distancia_total = 0
    duracion_total = 0
    for registro in historial:
        if registro["ejecutado"]:
            ejecutados = ejecutados + 1
            distancia_total = distancia_total + registro["distancia"]
            duracion_total = duracion_total + registro["tiempo"]
    rechazados = total - ejecutados

    print("=" * 40)
    print(" REPORTE DE MISION")
    print("=" * 40)
    print(f" Comandos totales    : {total}")
    print(f" Ejecutados          : {ejecutados}")
    print(f" Rechazados          : {rechazados}")
    print(f" Distancia recorrida : {round(distancia_total, 2)} m")
    print(f" Duracion estimada   : {round(duracion_total, 2)} s")

    if rechazados > 0:
        print("\n Motivos de rechazo:")
        for registro in historial:
            if not registro["ejecutado"]:
                print(f"  - {registro['comando']}: {registro['motivo']}")
    print("=" * 40)



def correr_mision(robot, nombre, mision):
    print(f"\n {nombre} ")
    historial = []
    ejecutar_mision(robot, mision, historial)
    generar_reporte(historial)
    robot.detenerse()


def crear_mi_mision():
    # mision propia: 6 comandos, dos invalidos a proposito
    mi_mision = [
        ("avanzar", 0.2, 2.0),
        ("girar", 0.5, 3.14),        # 0.5 rad/s x 3.14 s = 90 grados a la izquierda
        ("saludar",),
        ("avanzar", 5.0, 2.0),       # invalido: lo rechaza el robot por velocidad
        ("volar", 1.0, 1.0),         # invalido: tipo que no existe
        ("detenerse",),
    ]
    return mi_mision


def main():
    robot = Robot()
    robot.conectar()
    try:
        correr_mision(robot, "MISION BASICA", MISION_BASICA)
        correr_mision(robot, "MISION CON ERRORES", MISION_CON_ERRORES)
        correr_mision(robot, "MISION CUADRADO", MISION_CUADRADO)
        correr_mision(robot, "MI MISION PROPIA", crear_mi_mision())
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
