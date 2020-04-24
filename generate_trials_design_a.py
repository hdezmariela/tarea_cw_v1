import random
import csv
from collections import Counter
import pandas as pd
import numpy as np

# Experimento 1B (Pág. 22 de Souza, Rerko y Oberauer, 2015)
# Donde se seleccionar disco target al azar

# Genera grados HSL que colorean los 6 discos para los 390 ensayos
grados_discos = ["030", "090", "150", "210", "270", "330"]
ensayos_grados_colores = []

for ensayo in range(1, 396):

    grados_colores = [random.randint(0, 361)]

    ensayos_grados_colores.append(grados_colores)

    while len(grados_colores) < len(grados_discos):

        grados_aleatorios = random.randint(0, 361)
        diferencias = [abs(candidato - grados_aleatorios) for candidato in grados_colores]
        res_verifica = all(diferencias >= 20 for diferencias in diferencias)
        if res_verifica == True:
            grados_colores.append(grados_aleatorios)
        else:
            continue

# Produce archivo .csv con los colores de los 6 discos para todos los ensayos
# La última columna corresponde al número de ensayo
ensayos_grados_colores = pd.DataFrame(ensayos_grados_colores)
ensayos_grados_colores.columns = ['color_disco030', 'color_disco090', 'color_disco150', 'color_disco210', 'color_disco270', 'color_disco330']

# Crea secuencias aleatorias de arrows
nomb_fle = ["arrow" + grado + ".png" for grado in grados_discos]

ABCD = [] # 0-refreshing y 1-refreshing
opciones_ABCD = ['cero_refrescado', 'uno_refrescado']
candi_target_ABCD = []

ABAC = [] # 0-refreshing, 1-refreshing y 2-refreshing
opciones_ABAC = ['cero_refrescado', 'uno_refrescado', 'dos_refrescado']
candi_target_ABAC = []

ABCB = [] # 0-refreshing, 1-refreshing y 2-refreshing
opciones_ABCB = ['cero_refrescado', 'uno_refrescado', 'dos_refrescado']
candi_target_ABCB = []

ABCA = [] # 0-refreshing, 1-refreshing y 2-refreshing
opciones_ABCA = ['cero_refrescado', 'uno_refrescado', 'dos_refrescado']
candi_target_ABCA = []

ABAB = [] # 0-refreshing y 2-refreshing
opciones_ABAB = ['cero_refrescado', 'dos_refrescado']
candi_target_ABAB = []

for ensayo in range(79):

    # Secuencias tipo ABCD
    secABCD = random.sample(nomb_fle, 4)
    ABCD.append(secABCD)
    opciones_ABCD = opciones_ABCD[::-1]
    candi_target_ABCD.append(opciones_ABCD[0])

    # Secuencias tipo ABAC
    nomb_fle2 = nomb_fle[:]
    A = random.choice(nomb_fle2)
    nomb_fle2.remove(A)
    B = random.choice(nomb_fle2)
    nomb_fle2.remove(B)
    C = random.choice(nomb_fle2)
    secABAC = [A, B, A, C]
    ABAC.append(secABAC)
    candi_target_ABAC.append(list(np.roll(opciones_ABAC, ensayo))[0])

    #  Secuencias tipo ABCB
    nomb_fle3 = nomb_fle[:]
    A = random.choice(nomb_fle3)
    nomb_fle3.remove(A)
    B = random.choice(nomb_fle3)
    nomb_fle3.remove(B)
    C = random.choice(nomb_fle3)
    secABCB = [A, B, C, B]
    ABCB.append(secABCB)
    candi_target_ABCB.append(list(np.roll(opciones_ABCB, ensayo))[0])

    # Secuencias tipo ABCA
    nomb_fle4 = nomb_fle[:]
    A = random.choice(nomb_fle4)
    nomb_fle4.remove(A)
    B = random.choice(nomb_fle4)
    nomb_fle4.remove(B)
    C = random.choice(nomb_fle4)
    secABCA = [A, B, C, A]
    ABCA.append(secABCA)
    candi_target_ABCA.append(list(np.roll(opciones_ABCA, ensayo))[0])

    # Secuencias tipo ABAB
    nomb_fle5 = nomb_fle[:]
    A = random.choice(nomb_fle5)
    nomb_fle5.remove(A)
    B = random.choice(nomb_fle5)
    secABAB = [A, B, A, B]
    ABAB.append(secABAB)
    opciones_ABAB = opciones_ABAB[::-1]
    candi_target_ABAB.append(opciones_ABAB[0])

refrescamientos = ABCD + ABAC + ABCB + ABCA + ABAB
candi_target = candi_target_ABCD + candi_target_ABAC + candi_target_ABCB + candi_target_ABCA + candi_target_ABAB

# Identifica discos 0-refreshing
cero_refrescados = []
for ensayo in range(len(refrescamientos)):
    no_refrescados = [item for item in nomb_fle if item not in refrescamientos[ensayo]]
    cero_refrescados.append(no_refrescados)
cero_refrescados = [["non_existent"] if x == [] else x for x in cero_refrescados]

# Identifica discos 1-refreshing
uno_refrescados = []
for ensayo in range(len(refrescamientos)):
    un_refrescados = [k for k,v in Counter(refrescamientos[ensayo]).items() if v == 1]
    uno_refrescados.append(un_refrescados)
uno_refrescados = [["non_existent"] if x == [] else x for x in uno_refrescados]

# Identifica discos 2-refreshing
dos_refrescados = []
for ensayo in range(len(refrescamientos)):
    doble_refrescados = [k for k,v in Counter(refrescamientos[ensayo]).items() if v > 1]
    dos_refrescados.append(doble_refrescados)
dos_refrescados = [["non_existent"] if x == [] else x for x in dos_refrescados]

# Discos n-refrescados para cada ensayo
discos_n_refres = pd.DataFrame([cero_refrescados, uno_refrescados, dos_refrescados]).transpose()
discos_n_refres.columns = ["cero_refrescado", "uno_refrescado", "dos_refrescado"]

# Conversión de lista refrescamientos a data frame
refrescamientos = pd.DataFrame(refrescamientos)
refrescamientos.columns = ["arrow_1", "arrow_2", "arrow_3", "arrow_4"]

# target candidato
candi_target = pd.DataFrame(candi_target)
candi_target.columns = ["candi_target"]

# Concantenar refrescamientos con información sobre cantidad de refrescamientos por disco
refrescamientos = pd.concat([refrescamientos, discos_n_refres, candi_target], axis = 1, sort = False)

# Seleccionar disco target al azar
# Si el target candidato es 1-refreshing, selecciona al azar de entre las primeras dos arrows 1° y 2°
target_disco = []

for ensayo in range(395):

    if refrescamientos.loc[ensayo , "candi_target"] == 'cero_refrescado':
        target_disco.append((random.choice(refrescamientos.loc[ensayo , "cero_refrescado"])))

    if refrescamientos.loc[ensayo , "candi_target"] == 'uno_refrescado':
        target_disco.append(random.choice(list(refrescamientos.loc[ensayo , "arrow_1":"arrow_2"]))) # Experimento 1A (Pág. 22 de Souza, Rerko y Oberauer, 2015)

    if refrescamientos.loc[ensayo , "candi_target"] == 'dos_refrescado':
        target_disco.append(random.choice(refrescamientos.loc[ensayo , "dos_refrescado"]))

target_disco = [target_disco.replace('arrow', 'disc') for target_disco in target_disco]
target_disco = [target_disco.replace('.png', '') for target_disco in target_disco]
target_disco = pd.DataFrame(target_disco)
target_disco.columns = ["target_disco"]
refrescamientos = pd.concat([refrescamientos, target_disco, ensayos_grados_colores], axis = 1, sort = False)

target_color = [refrescamientos.loc[ensayo , "color_disco" + refrescamientos.loc[ensayo , "target_disco"][-3:]] for ensayo in range(395)]
target_color = pd.DataFrame(target_color)
target_color.columns = ["target_color"]
refrescamientos = pd.concat([refrescamientos, target_color], axis = 1, sort = False)

# Aleatoriza ensayos
refrescamientos = refrescamientos.sample(frac = 1, replace = False)

# Añade una primera columna con ID de ensayos
refrescamientos.insert(loc = 0, column = 'trial_ID', value = np.arange(1,396))

# Añade una última columna para identificar los ensayos de práctica
practice_trials = ["Yes"]*5 + ["No"]*390
refrescamientos.insert(loc = 17, column = 'practice_trial', value = practice_trials)

# Exporta todo a un .csv
refrescamientos.to_csv('design/trials_design_a.csv', index = False, header = True, sep = ";")