'''
Ejercicio 1
Escriba una función llamada "score" que tome como argumento
el nombre de cualquiera de los estudiantes del grupo y me regrese su calificación final con letra:
* score = 20% (promedio tareas) + 80% (promedio exámenes)
e.g. Si a la función "score" le paso como argumento "Aleja" me debería regresar => "ocho punto seis" (redondear a 1 dígito)
'''

# REST
from rest_framework.validators import ValidationError

# Utils
from decimal import Decimal

#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'jbge'

MONEDA_SINGULAR = 'peso'
MONEDA_PLURAL = 'pesos'

CENTIMOS_SINGULAR = 'centavo'
CENTIMOS_PLURAL = 'centavos'

MAX_NUMERO = 999999999999

UNIDADES = (
    'cero',
    'uno',
    'dos',
    'tres',
    'cuatro',
    'cinco',
    'seis',
    'siete',
    'ocho',
    'nueve'
)

DECENAS = (
    'diez',
    'once',
    'doce',
    'trece',
    'catorce',
    'quince',
    'dieciseis',
    'diecisiete',
    'dieciocho',
    'diecinueve'
)

DIEZ_DIEZ = (
    'cero',
    'diez',
    'veinte',
    'treinta',
    'cuarenta',
    'cincuenta',
    'sesenta',
    'setenta',
    'ochenta',
    'noventa'
)

CIENTOS = (
    '_',
    'ciento',
    'doscientos',
    'trescientos',
    'cuatroscientos',
    'quinientos',
    'seiscientos',
    'setecientos',
    'ochocientos',
    'novecientos'
)


def numero_a_letras(numero, new_format=None):
    numero_entero = int(numero)

    if numero_entero > MAX_NUMERO:
        raise OverflowError('Número demasiado alto')
    if numero_entero < 0:
        return 'menos %s' % numero_a_letras(abs(numero))

    # parte decimal
    letras_decimal = ''
    parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))

    if new_format is not None:
        letras_decimal = "{}/100 M.N.".format(parte_decimal)
    else:
        if parte_decimal > 9:
            letras_decimal = 'punto %s' % numero_a_letras(parte_decimal)
        elif parte_decimal > 0:
            letras_decimal = 'punto cero %s' % numero_a_letras(parte_decimal)

    # entero
    if (numero_entero <= 99):
        resultado = leer_decenas(numero_entero)
    elif (numero_entero <= 999):
        resultado = leer_centenas(numero_entero)
    elif (numero_entero <= 999999):
        resultado = leer_miles(numero_entero)
    elif (numero_entero <= 999999999):
        resultado = leer_millones(numero_entero)
    else:
        resultado = leer_millardos(numero_entero)
    resultado = resultado.replace('uno mil', 'un mil')
    resultado = resultado.strip()
    resultado = resultado.replace(' _ ', ' ')
    resultado = resultado.replace('  ', ' ')

    # Se juntan las 2 conversiones y se regresan
    if parte_decimal > 0:
        resultado = "{} PESOS".format(resultado.upper())
        resultado = '%s %s' % (resultado, letras_decimal)
    return resultado


def numero_a_moneda(numero):
    numero_entero = int(numero)
    parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
    centimos = ''
    if parte_decimal == 1:
        centimos = CENTIMOS_SINGULAR
    else:
        centimos = CENTIMOS_PLURAL
    moneda = ''
    if numero_entero == 1:
        moneda = MONEDA_SINGULAR
    else:
        moneda = MONEDA_PLURAL
    letras = numero_a_letras(numero_entero)
    letras = letras.replace('uno', 'un')
    letras_decimal = 'con %s %s' % (numero_a_letras(
        parte_decimal).replace('uno', 'un'), centimos)
    letras = '%s %s %s' % (letras, moneda, letras_decimal)
    return letras


def leer_decenas(numero):
    if numero < 10:
        return UNIDADES[numero]
    decena, unidad = divmod(numero, 10)
    if numero <= 19:
        resultado = DECENAS[unidad]
    elif numero <= 29:
        if numero == 20:
            resultado = "veinte"
        else:
            resultado = 'veinti%s' % UNIDADES[unidad]
    else:
        resultado = DIEZ_DIEZ[decena]
        if unidad > 0:
            resultado = '%s y %s' % (resultado, UNIDADES[unidad])
    return resultado


def leer_centenas(numero):
    centena, decena = divmod(numero, 100)
    if numero == 0:
        resultado = 'cien'
    else:
        resultado = CIENTOS[centena]
        if decena > 0:
            resultado = '%s %s' % (resultado, leer_decenas(decena))
    return resultado


def leer_miles(numero):
    millar, centena = divmod(numero, 1000)
    resultado = ''
    if (millar == 1):
        resultado = ''
    if (millar >= 2) and (millar <= 9):
        resultado = UNIDADES[millar]
    elif (millar >= 10) and (millar <= 99):
        resultado = leer_decenas(millar)
    elif (millar >= 100) and (millar <= 999):
        resultado = leer_centenas(millar)
    resultado = '%s mil' % resultado
    if centena > 0:
        resultado = '%s %s' % (resultado, leer_centenas(centena))
    return resultado


def leer_millones(numero):
    millon, millar = divmod(numero, 1000000)
    resultado = ''
    if (millon == 1):
        resultado = ' un millon '
    if (millon >= 2) and (millon <= 9):
        resultado = UNIDADES[millon]
    elif (millon >= 10) and (millon <= 99):
        resultado = leer_decenas(millon)
    elif (millon >= 100) and (millon <= 999):
        resultado = leer_centenas(millon)
    if millon > 1:
        resultado = '%s millones' % resultado
    if (millar > 0) and (millar <= 999):
        resultado = '%s %s' % (resultado, leer_centenas(millar))
    elif (millar >= 1000) and (millar <= 999999):
        resultado = '%s %s' % (resultado, leer_miles(millar))
    return resultado


def leer_millardos(numero):
    millardo, millon = divmod(numero, 1000000)
    return '%s millones %s' % (leer_miles(millardo), leer_millones(millon))


students = [
    {"name": "Raymundo", "age": 25, "homeworks": [90.0, 95, 85.5, 90], "test": [75, 65.5, 85]},
    {"name": "Aleja", "age": 23, "homeworks": [72.0, 89.5, 95, 100], "test": [90, 90, 85]},
    {"name": "Victor", "age": 28, "homeworks": [95, 80, 100, 0], "test": [70, 85, 65]}
]


def calculate_average(scores):
    total = 0

    for score in scores:
        total += score

    average = total / len(scores)

    return round(average, 1)


def score(name):
    # current studend
    current_student = None

    for student in students:
        if student.get("name") == name:
            current_student = student
            break

    if current_student is None:
        raise ValidationError("El estudiante no se encontro")

    # get homework averages
    homework_average = str(calculate_average(current_student.get("homeworks")))
    homework_average = homework_average.replace(".", "")

    # get test averages
    test_average = str(calculate_average(current_student.get("test")))
    test_average = test_average.replace(".", "")

    homework_points = 2 * Decimal("0.{}".format(homework_average))
    test_points = 8 * Decimal("0.{}".format(test_average))

    score = homework_points + test_points

    return numero_a_letras(score)
