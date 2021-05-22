import sys
import re

def calcular_porcentaje_diccionario(diccionario, total_jugadas):
    diccionario_nuevo={}
    for key in diccionario.keys():
        porcentaje_usado = round((diccionario[key][0]/total_jugadas)*100,2)
        porcentaje_ganado = round((diccionario[key][1]/diccionario[key][0])*100,2)
        if porcentaje_usado>=0.2:
            diccionario_nuevo[key] = ["{:.2f}".format(porcentaje_usado), "{:.2f}".format(porcentaje_ganado)]
    return diccionario_nuevo

def programa_1(complete_text):
    jugada = '(\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n)'
    regex = '(?<=\[Opening ").+?(?=:)|(?<=\[Opening ").+?(?="\])'
    resultado = '(?<=\[Result ").+(?="\])'
    regex_variacionews = ''
    dic_aperturas = {}
    contador_blancas = 0
    dic_porcentajes = {}
    regex_variaciones = ''
    cont_aperturas_totales = 0
    jugadas_encontradas = re.findall(jugada,complete_text)
    cont_apariciones = 0
    cont_ganadas = 0
    texto_porcentajes = ''''''
    for game in jugadas_encontradas:
        cont_aperturas_totales += 1
        opening = re.findall(regex,game)[0]
        result = re.findall(resultado,game)[0]
        if opening not in dic_aperturas.keys():
            dic_aperturas[opening] =[{}, 1,0]
            if result == '1-0':
                dic_aperturas[opening][2] +=1
            elif result == '1/2 -1/2':
                dic_aperturas[opening][2] += 0.5
        else:
            dic_aperturas[opening][1] +=1
            if result == '1-0':
                dic_aperturas[opening][2] +=1
            elif result == '1/2-1/2':
                dic_aperturas[opening][2] += 0.5
        opening = str(opening)
        if opening == '?':
            regex_variaciones = '(?<=\\' + opening + ': )(.+)?(?="\])'
        else:
            regex_variaciones = '(?<=' + opening + ': )(.+)?(?="\])'
        variacion_encontrada = re.findall(regex_variaciones,game)
        if len(variacion_encontrada) > 0:
            if variacion_encontrada[0] not in dic_aperturas[opening][0].keys():
                dic_aperturas[opening][0][variacion_encontrada[0]] = [1,0]
                if result == '1-0':
                    dic_aperturas[opening][0][variacion_encontrada[0]][1]+= 1
                elif result == '1/2-1/2':
                    dic_aperturas[opening][0][variacion_encontrada[0]][1] += 0.5
            else:
                dic_aperturas[opening][0][variacion_encontrada[0]][0] += 1
                if result == '1-0':
                    dic_aperturas[opening][0][variacion_encontrada[0]][1]+= 1
                elif result == '1/2-1/2':
                    dic_aperturas[opening][0][variacion_encontrada[0]][1] += 0.5
        else:
            if ' ' not in dic_aperturas[opening][0].keys():
                dic_aperturas[opening][0][' '] = [1,0]
                if result == '1-0':
                    dic_aperturas[opening][0][' '][1]+= 1
                elif result == '1/2-1/2':
                    dic_aperturas[opening][0][' '][1] += 0.5
            else:
                dic_aperturas[opening][0][' '][0] += 1
                if result == '1-0':
                    dic_aperturas[opening][0][' '][1]+= 1
                elif result == '1/2-1/2':
                    dic_aperturas[opening][0][' '][1] += 0.5
    for apertura in dic_aperturas.keys():
        dic_variaciones_porcentaje= calcular_porcentaje_diccionario(dic_aperturas[apertura][0], cont_aperturas_totales)
        veces_usado = round((dic_aperturas[apertura][1]/cont_aperturas_totales)*100,2)
        veces_ganado = round((dic_aperturas[apertura][2]/dic_aperturas[apertura][1])*100,2)
        if veces_usado >= 0.20:
            dic_porcentajes[apertura] = [dic_variaciones_porcentaje, "{:.2f}".format(veces_usado), "{:.2f}".format(veces_ganado)]

    dic_porcentajes = dict(sorted(dic_porcentajes.items(), key=lambda item: item[1][1], reverse=True))
    for key in dic_porcentajes.keys():
        dic_porcentajes[key][0] = dict(sorted(dic_porcentajes[key][0].items(), key=lambda item: item[1][0], reverse=True))

    for key in dic_porcentajes.keys():
        porcentaje_uso = dic_porcentajes[key][1]
        porcentaje_ganado = dic_porcentajes[key][2]
        texto_porcentajes += porcentaje_uso + '% ' + key + ' ( ' + porcentaje_ganado + '% for white)\n'
        for variation in dic_porcentajes[key][0].keys():
            texto_porcentajes += '    ' + dic_porcentajes[key][0][variation][0] + '% ' + variation + ' ( ' + dic_porcentajes[key][0][variation][1] + '% for white)\n'
    return texto_porcentajes

def programa_2(complete_text):
    texto_limpio =''''''
    regex_extra_info = '\{.+?\}'
    texto_limpio = re.sub(regex_extra_info, '', complete_text)
    regex_simbolos = '(\?!)|(\?+)'
    texto_limpio = re.sub(regex_simbolos, '', texto_limpio)
    regex_numeros = '\d+\.\.\.'
    texto_limpio = re.sub(regex_numeros,'', texto_limpio)
    return texto_limpio

def programa_3(complete_text):
    regex_completo = '(\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\n\d.+)'
    regex_juegos ='(?<=\n)\d+.+'
    regex_movimientos = '\d+\. '
    contador_movimientos = 0
    texto_nuevo = ''''''
    info_nueva = ''
    regex_informacion = '\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n\[.+\n'
    jugadas = re.findall(regex_completo, complete_text)
    for jugada in jugadas:
        contador_movimientos = 0
        juegos = re.findall(regex_juegos, jugada)
        juego = juegos[0]
        movimientos = re.findall(regex_movimientos, juego)
        for movimiento in movimientos:
            contador_movimientos +=1
        informaciones = re.findall(regex_informacion, jugada)
        informacion = informaciones[0]
        info_nueva = informacion
        info_nueva += '[Moves "'+str(contador_movimientos)+'"]'
        texto_nuevo += info_nueva + '\n\n' + juego +'\n\n'
    return texto_nuevo

archivo = open(sys.argv[1],"r")
texto = archivo.read()

text1 = programa_1(texto)
text2 = programa_2(texto)
text3 = programa_3(texto)

archivo.close()
print("Ingrese 1 para el pograma 1, 2, para el segundo programa, 3 para el tercero, 0 para salir\n")
choice = input()
while(choice != '0'):
    if choice == '1':
        print(text1)
    elif choice =='2':
        print(text2)
    elif choice == '3':
        print(text3)
    else:
        print("input inválido")
    print("Ingrese 1 para el pograma 1, 2, para el segundo programa, 3 para el tercero, 0 para salir\n")
    choice = input()
