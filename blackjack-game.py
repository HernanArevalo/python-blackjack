import random
import time


def menu(pozo_):
    partidas_, victorias_, may_racha_cr_, racha_cr_, cant_bj_, may_perdida_, apuesta_tot_ = 0, 0, 0, 0, 0, 0, 0
    may_pozo_ = pozo_

    op = 1
    while op != 3:
        time.sleep(0.5)

        print('-----MENÚ-----')
        print('1. Apostar\n2. Jugar una mano\n3. Salir')
        op = int(input('Elija una opción: '))
        if op == 1:
            pozo_ = apostar(pozo_)
        elif op == 2:
            pozo_, partidas_, victorias_, racha_cr_, cant_bj_, perdida_, apuesta_ = jugar(pozo_, partidas_, victorias_, racha_cr_, cant_bj_)
            if pozo_ > may_pozo_:
                may_pozo_ = pozo_
            if racha_cr_ > may_racha_cr_:
                may_racha_cr_ = racha_cr_
            if perdida_ > may_perdida_:
                may_perdida_ = perdida_
            apuesta_tot_ += apuesta_

        elif op != 3:
            print('RESPUESTA INCORRECTA')
    salir(pozo_, partidas_, victorias_, racha_cr_, cant_bj_, may_pozo_, may_perdida_, apuesta_tot_)


def apostar(pozo__):
    s()
    print(f'Su pozo tiene un valor actual de: ${pozo__}')

    if pozo__ >= 100000:
        print('No puede sumar dinero al pozo cuando su valor es igual o mayor a $100.000')
    else:
        sumarpozo = monto_correcto('Ingrese una cantidad para sumar al pozo (el pozo no puede superar los $100.000', (100000-pozo))
        pozo__ += sumarpozo
        print(f'Su pozo ahora tiene un valor de: ${pozo__}')
    return pozo__


def jugar(pozo__, partidas__, victorias__, racha_cr__, cant_bj__):
    if pozo__ == 0:
        print('No tiene dinero en su pozo para apostar')
        return pozo__, partidas__, victorias__, racha_cr__, cant_bj__, 0, 0

    print(f'\nUsted tiene ${pozo__} en el pozo.')
    apuesta = int(monto_correcto(f'Ingrese la cantidad a apostar', pozo__, mult5=True))

    s()
    print('\n-----PARTIDA COMENZADA-----')
    print(f'Apuesta en juego: ${apuesta}')
    partidas__ += 1
    s()

    pj_suma, cr_suma, pj_ases, cr_ases, pj_cartas, cr_cartas = 0, 0, 0, 0, 0, 0

    # 2 CARTAS PJ Y 1 CARTA CR
    for i in range(3):

        if (i % 2) == 0:
            (pj_suma, pj_ases, pj_cartas) = pedir_carta(pj_suma, pj_ases, pj_cartas, owner='jugador')
        else:
            (cr_suma, cr_ases, cr_cartas) = pedir_carta(cr_suma, cr_ases, cr_cartas)
    if pj_suma == 21:
        cant_bj__ += 1

    # RESTO CARTAS JUGADOR
    while pj_suma <= 21:
        s()
        print(f'\nSu puntaje parcial es {pj_suma}')
        resp = input(f'Desea seguir pidiendo cartas? (S/N): ')
        s()
        if resp.upper() == 'S':
            (pj_suma, pj_ases, pj_cartas) = pedir_carta(pj_suma, pj_ases, pj_cartas, owner='jugador')

        elif resp.upper() == 'N':
            break

    pj_21 = puntaje_final(pj_suma, owner='jugador')
    s(2)

    # RESTO CARTAS CROUPIER
    while cr_suma < 17:

        (cr_suma, cr_ases, cr_cartas) = pedir_carta(cr_suma, cr_ases, cr_cartas)
        if cr_cartas == 2 and cr_suma == 21:
            cant_bj__ += 1
    cr_21 = puntaje_final(cr_suma)

    # GANADOR
    empate = False
    gano = False
    if pj_suma == cr_suma or (not pj_21 and not cr_21):
        empate = True
    elif pj_21:
        if pj_suma > cr_suma or not cr_21:
            gano = True
    s()
    print(f'\nPuntaje final del jugador: {pj_suma}\nPuntaje final del croupier: {cr_suma} ')
    s(2)

    if gano:
        print(f'\nGANA EL JUGADOR\nFELICITACIONES {nombre.upper()}')
        s()
        print(f'Ganaste ${apuesta}!!!')
        pozo__ += apuesta
        victorias__ += 1
        racha_cr__ = 0
        perdida__ = 0
    elif empate:
        if not pj_21:
            print('Se pasaron los dos')
        else:
            print(f'Ambos empataron con {pj_suma}')
        s()
        racha_cr__ = 0
        perdida__ = 0
        print(f'EMPATE\nSe devuelve la apuesta de ${apuesta}')
    else:
        print(f'GANA EL CROUPIER\nMEJOR SUERTE LA PROXIMA {nombre.upper()}')
        racha_cr__ += 1
        perdida__ = apuesta
        s()
        print(f'Perdiste ${apuesta} :(')

        pozo__ -= apuesta

    print(f'Tu pozo quedó con un valor de ${pozo__}')
    print('-' * 34)

    return pozo__, partidas__, victorias__, racha_cr__, cant_bj__, perdida__, apuesta


def salir(pozo__, partidas__, victorias__, racha_cr__, cant_bj__, may_pozo__, may_perdida__, apuesta_tot_):
    print(f'Su pozo quedó con un valor final de: ${pozo__}')

    # El porcentaje de victorias del jugador.
    porc_victorias = round((victorias__ / partidas__) * 100)
    print(f'El jugador ganó el {porc_victorias}% de sus partidas ({victorias__} de {partidas__})')
    # La racha más larga de victorias del croupier.
    print(f'Mayor racha de victorias del croupier: {racha_cr__} victorias')
    # La cantidad de manos donde hubo un blackjack natural
    print(f'Cantidad de blackjacks naturales: {cant_bj__}')
    # El monto máximo que llegó a tener el jugador en el pozo.
    print(f'Monto maximo que llego a tener el pozo: ${may_pozo__}')
    # El monto promedio del que dispuso el jugador para realizar apuestas.
    apuesta_promedio = apuesta_tot_ // partidas__
    print(f'El jugador realizó apuestas con un promedio de ${apuesta_promedio}')
    # La pérdida más grande que sufrió el jugador (si hubo alguna)
    if may_perdida__ > 0:
        print(f'La mayor perdida del jugador fue de: ${may_perdida__}')
    else:
        print('El jugador no sufrio pérdida de dinero')


def monto_correcto(mensaje, mx, mn=0, mult5=False):
    if mult5:
        mensaje += str(f' (entre ${mn} y ${mx}, y multiplo de 5): $')
    else:
        mensaje += str(f' (entre ${mn} y ${mx}): $')
    monto = int(input(mensaje))

    if mn > monto or monto > mx:
        print(f'ERROR... El monto no está entre ${mn} y ${mx}')
        monto_valido = False
    else:
        monto_valido = True
    if mult5 and (monto % 5) != 0:
        print('ERROR... El monto no es divisible por 5')
        monto_mult_5 = False
    else:
        monto_mult_5 = True

    while not monto_valido or not monto_mult_5:
        monto = int(input(mensaje))
        if mn > monto or monto > mx:
            print(f'ERROR... El monto no está entre ${mn} y ${mx}')
            monto_valido = False
        else:
            monto_valido = True

        if mult5 and (monto % 5) != 0:
            print('ERROR... El monto no es divisible por 5')
            monto_mult_5 = False
        else:
            monto_mult_5 = True

    return monto


def pedir_carta(suma, ases, carta_nro, owner='croupier'):

    carta_nro += 1
    carta = (random.choice(valores), random.choice(palos))

    print(f'\nCarta Nro {carta_nro} del {owner.upper()}:\n\t{carta[0]} de {carta[1]}')

    if carta[0] == 'A':
        suma += 11
        ases += 1
    elif type(carta[0]) == str:
        suma += 10
    else:
        suma += carta[0]

    while suma > 21 and ases > 0:
        suma -= 10
        ases -= 1
        print(f'Valor de AS cambiado de 11 a 1 (AS del {owner})')

    print(f'•PUNTAJE PARCIAL DEL {owner.upper()}:\n\t{suma}')
    s(3)
    return suma, ases, carta_nro


def puntaje_final(suma, owner='croupier'):
    s()
    if suma > 21:
        print(f'\n•• El {owner.upper()} se ha pasado de 21 ••')
        return False
    else:
        print(f'\n•• PUNTAJE FINAL DEL {owner.upper()}: {suma} ••')
        return True


def s(t=0.0):
    time.sleep(t)


valores = ('A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K')
palos = ('corazones', "diamantes", "tréboles", "picas")

print('•BLACKJACK•')
print('-' * 34)
s(0.5)
nombre = str(input('Ingrese su nombre: '))
pozo = monto_correcto('Ingrese el monto de su pozo', 100000, 0)

menu(pozo)
