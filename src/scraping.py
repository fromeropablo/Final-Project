from selenium import webdriver
import time
import pandas as pd
import json
import numpy as npS

"""Important note: For the first three functions, you have to use Selenium opening the webdriver with the following url: http://jv.acb.com/es/101266/cartadetiro

Also, you have to switch the menu at the left zone from "Semana" to "Jornada".

"""

def names():
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    """
    This function helps us to get the names of the players from a single game."""

    lista = driver.find_elements_by_css_selector("td.ta-col.ta-col--name")
    nombres = []
    for i in lista:
        name = i.text
        nombres.append(name)
    return nombres

def get_shots():

    """
    This function get all the shots from a single game grouping them by player. 

    1. The first part consists in getting the elements of each game from the HTML using selenium. The variable "pincho" contains the name of every player from the game
    which will be clicked inside the loop.

    2. The second part is the second for loop. The big one. We have to click in every single player in order to get the info from each shot. The empty list "gran_reg"
    gets, in order, if the shot is good or not, its coordinate x and its coordinate y. We finish this part clicking again in the same player to avoid the cumulation
    of shots. 

    3. The last part consists in filling the empty dictionary which it has the name of the players as keys and all the info from their shots as a value (it will be a
    list).

    """

    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    driver.get('http://jv.acb.com/es/101266/cartadetiro')
    driver.implicitly_wait(10)
    primer = driver.find_element_by_class_name("sm")
    segun = primer.find_elements_by_class_name("ge-btn.ge-btn")
    for chart in segun:
        chart.click()

    pincho = driver.find_elements_by_css_selector("td.ta-col.ta-col--name")
    result = {}
    gran_reg = []

    for i in pincho:
        dentro = []
        coord_x = []
        coord_y = []
        i.click()
        time.sleep(1)
        a = driver.find_element_by_css_selector("div.sm-gra")
        b = a.find_element_by_tag_name("svg")
        tiros = b.find_elements_by_tag_name("use")
        tiros = tiros[6:] #It's always 6 because of the HTML from the page!!!
        for s in tiros:
            shot = s.get_attribute("xlink:href")
            x = s.get_attribute("x")
            y = s.get_attribute("y")
            dentro.append(shot)
            dentro.append(x)
            dentro.append(y)
        gran_reg.append(dentro)
        i.click()
    nombres = names()
    mix = list(zip(nombres, gran_reg))
    for m in mix:
        result[m[0]] = m[1]
    return result



def season(first_gameday, last_gameday):
    """ 
    This function gets the info from above but with a range of gamedays within the season 2020-21 of the Spanish Basketball League (Liga Endesa).

    It consists on clicking in the first gameday chose and getting all the info from above but for a whole gameday. Afterwards, it does the same until the last 
    gameday chosen. 
    
    The result is a large dictionary with the number of the gameday as a key and a dictionary of dictionaries as a value for each gameday. 
    """

    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    driver.get('http://jv.acb.com/es/101266/cartadetiro')
    driver.implicitly_wait(10)

    final = {}
    for i in range (first_gameday, last_gameday + 1):
        try:
            semana = driver.find_element_by_class_name("nav-top-sec-round").click()
            nueva = driver.find_elements_by_class_name("nav-opt")
            nueva[-(i)].click()
            datos_jornada = {}
            intermedio = []
            buscador = driver.find_element_by_class_name("nav-cont.nav-cont--day")
            jornada = buscador.find_elements_by_class_name("nav-day-match")
            for game in jornada:
                game.click()
                data = get_shots()
                datos_jornada.update(data)
            intermedio.append(datos_jornada)
            final[i] = intermedio
        except TypeError:
            raise "This game has not started yet"
            
    return final


"---------------------------------------------------------------------------------------------------------------------------------"

"""Important note: For these functions, you have to use Selenium opening the webdriver with the following url: 

https://basketball.realgm.com/international/league/4/Spanish-ACB/stats/2021/Averages/All/All/points/All/desc/1/Regular_Season

"""

def players_name(class_name):
    """
    Here we obtain the headers from our future stats tables.  

    To obtain headers from general info about players: "tablesaw.tablesaw-swipe.tablesaw-sortable"

    To obtain headers from stats about players: "tablesaw.compact.tablesaw-swipe"

    """

    tablita = driver.find_element_by_class_name(class_name)
    columnas = tablita.find_elements_by_tag_name("th")
    interm = []
    for a in columnas:
        interm.append(a)
    columns_name = []
    for name in interm: 
        columns_name.append(name.text)
    
    return columns_name
    

def table_stats(class_name):
    """
    In this function we can obtain a stats table with general individual statistics from 2020/21 in Liga Endesa. 

    Depending if you are in average stats or per minute stats, you will have to use one class_name or another:

    -Average stats class_name: "tablesaw.compact.tablesaw-swipe"    url: https://basketball.realgm.com/international/league/4/Spanish-ACB/stats/2021/Averages/All/All/points/All/desc/1/Regular_Season

    -Per minute stats class_name: "tablesaw.compact.tablesaw-swipe"  url: https://basketball.realgm.com/international/league/4/Spanish-ACB/stats/2021/Per_Minute/All/All/points/All/desc/1/Regular_Season

    -General statistics: "tablesaw.tablesaw-swipe.tablesaw-sortable"  url: https://basketball.realgm.com/international/league/4/Spanish-ACB/team/649/Acunsa-GBC/rosters

    """

    buscador = driver.find_element_by_xpath('//*[@id="site-takeover"]/div[3]/div/div[1]/div[4]/select')
    options = buscador.find_elements_by_tag_name("option") #get all the options into a list

    optionsList = []
    for option in options: #iterate over the options, place attribute value in list
        optionsList.append(option.get_attribute("value"))
    optionsList = optionsList[1:]

    stats_list = [] 
    final = []
    for optionValue in optionsList: 
        print("starting loop on option %s" % optionValue)
        select = Select(driver.find_element_by_xpath('//*[@id="site-takeover"]/div[3]/div/div[1]/div[4]/select'))
        select.select_by_value(optionValue)
        tablita = driver.find_element_by_class_name(class_name)
        players = tablita.find_elements_by_tag_name("tr")
        for player in players:
            stats = player.find_elements_by_tag_name("td")
            for stat in stats:
                stats_list.append(stat.text)
                
    return stats_list

