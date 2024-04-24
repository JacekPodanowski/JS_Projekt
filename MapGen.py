import random
import sys
import pygame

def generate_random_map(WIDTH,HEIGHT,maxLines):
    line_points = []    
    num_points = random.randint(8, maxLines)
    for i in range(num_points):
        x = random.randint(0, WIDTH)
        y = random.randint(int(HEIGHT/1.5), HEIGHT)
        line_points.append((x, y))
    
    # Sortowanie punktów po współrzędnej x
    line_points.sort(key=lambda point: point[0])
    
    startY=line_points[0][1]
    line_points[0]=(0,startY)
    
    endY=line_points[-1][1]
    line_points[-1]=(WIDTH,endY)

    # Wybierz losowy fragment linii do lądowania
    landing_point = random.randint(1, len(line_points) - 2)
    
    landingY = line_points[landing_point][1]
    #Poziomowanie strefy ladowania
    startX=line_points[landing_point-1][0]
    line_points[landing_point-1]=(startX,landingY)
    
    startX=line_points[landing_point+1][0]
    line_points[landing_point+1]=(startX,landingY)
    

    return [landing_point,line_points]