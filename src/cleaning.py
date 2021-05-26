import pandas as pd
import json
import re

def shots_per_player(df):
    """
    Using our dataframe with all the shots of the season, we get a list of repeated names of players which each name is a shot made by him. 

    The parameter df is the DataFrame from we obtain the names. 
    """

    length = []
    first = []
    for i in range(1, len(df)):
        names = []
        cosa = df.iloc[i]
        hola = cosa[1]
        p = re.compile('(?<!\\\\)\'')
        hola = p.sub('\"', hola)
        otra = json.loads(hola)
        shots = otra[0]
    #getting the names
        for k,v in shots.items():
            length.append(len(v)//3)
            first.append(k)
        res_list = [length[i] * str(first[i] + ", ") for i in range(len(length))]
        for i in range(len(res_list)):
            primero = res_list[i].split(",")
            for n in primero:
                names.append(n)

    return names


def cumulat_shots(df):
    """
    Again, we will use our DataFrame to calculate the cumulative shots per gameday.

    The parameter df is the DataFrame of shots.
    """
    prueba = []
    jornadas = []
    for i in range(1, len(df)):
        cosa = df.iloc[i]
        hola = cosa[1]
        p = re.compile('(?<!\\\\)\'')
        hola = p.sub('\"', hola)
        otra = json.loads(hola)
        shots = otra[0]
        valores = list(shots.values())
        for i in valores:
            for n in i:
                prueba.append(n)
        jornadas.append(len(prueba))
    jornadas[:] = [x // 3 for x in jornadas]    
    return jornadas, prueba



def change_names(df):
    """In this function we create a new list where we append the surname of each player to merge multiple DataFrames. 
    """
    nombres = list(df["PLAYER_NAME"])
    cambio_nombre = []
    for s in nombres:
        l = s.split()
        new = ""
        for i in range(len(l)-1):
            s = l[i]
            new += (s[0].upper()+'. ')
        new += l[-1].title()
        cambio_nombre.append(new)
    return cambio_nombre