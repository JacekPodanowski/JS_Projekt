import random
import sys
import pygame
import numpy as np
from Settings import *


std_dev = 50

def normal_dist_rand(mean,std_dev,min,max):
    while True:
        num = int(np.random.normal(mean, std_dev))
        if min <= num <= max:
            return num

def generate_line_points(WIDTH, HEIGHT, lines_num):
    line_points = []
    mean = WIDTH//lines_num
    x=0
    tmp_point_tab=[]
    for i in range(lines_num):
        segment_len = normal_dist_rand(mean,std_dev,0,WIDTH)
        x = x + segment_len
        y = random.randint(int(HEIGHT / 2), HEIGHT)
        tmp_point_tab.append([x,y])
    
    # Sortowanie punktów po współrzędnej x
    tmp_point_tab.sort(key=lambda point: point[0])
    
    scale=WIDTH/tmp_point_tab[-1][0]
    for i in range(len(tmp_point_tab)):
        tmp_point_tab[i][0] = int(tmp_point_tab[i][0]*scale) #skalowanie punktów
    

    for i in tmp_point_tab:
        line_points.append((i[0], i[1]))

    startY = line_points[0][1]
    line_points[0] = (0, startY)

    endY = line_points[-1][1]
    line_points[-1] = (WIDTH, endY)
    return line_points

def choose_landing_zone(line_points, landing_zone_min_size):
    while True:
        landing_point = random.randint(2, len(line_points) - 3)
        if (line_points[landing_point][0] - line_points[landing_point - 1][0] >= landing_zone_min_size):
            return landing_point

def check_valid_landings(line_points, landing_zone_min_size):
    for i in range(1, len(line_points) - 1):
        if (line_points[i][0] - line_points[i - 1][0] >= landing_zone_min_size):
            if i >= 2 and len(line_points) - i > 2:
                return True
    return False


def generate_map_parameters(day): # Trudnośc rośnie do 30 dnia, potem jest stała
    lines_num = int(random.randint(-2,2) + 15 + (day/3)) if day <= 30 else random.randint(-2,2) + 25
    landing_zone_min_size = 60 - day if day <= 30 else 30
    landing_zone_height_scale = 0.75 + 0.005 *day if day <= 30 else 0.9
    return lines_num,landing_zone_min_size,landing_zone_height_scale

def generate_random_map(WIDTH, HEIGHT,day):
    lines_num,landing_zone_min_size,landing_zone_height_scale=generate_map_parameters(day)
    
    line_points = generate_line_points(WIDTH, HEIGHT, lines_num)
    map_counter = 0
    while(check_valid_landings(line_points,landing_zone_min_size)==False):
        line_points = generate_line_points(WIDTH, HEIGHT, lines_num)
        map_counter+=1
        if(map_counter>10000):
            print("Can't generate map with given parameters. Exiting...")
            sys.exit(1)

    landing_point = choose_landing_zone(line_points, landing_zone_min_size)

    #wysokość strefy ladowonaia
    landingY = max((HEIGHT * landing_zone_height_scale), (line_points[landing_point][1])) # niższy punkt z : Wysokość * skala lub wygenerowana wysokosc
    
    # Poziomowanie strefy ladowania
    startX = line_points[landing_point - 1][0]
    endX = line_points[landing_point][0]
    
    line_points[landing_point - 1] = (startX, landingY)#przesiuniecie poczatku
    line_points[landing_point] = (endX, landingY)#przesiuniecie konca
    
    return landing_point, line_points