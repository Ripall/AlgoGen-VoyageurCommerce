import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
from collections import namedtuple
import sys
from random import shuffle


City = namedtuple('City', 'name,x,y')


class Individual:

    def __init__(self, cities):
        self.cities = cities
        print(self.cities)

    def mutate(self):
        pass

    def cross_breeding(self,individual):
        pass

    def fitness(self):
        value = 0
        for i, city in enumerate(self.cities):
            value += abs(city.x-city[i-1].x)+abs(city.y-city[i-1].y)
        return value


class Population:

    def __init__(self, size, mutationRate, crossRate, cities):
        self.individuals = []
        self.size = size
        self.mutationRate = mutationRate
        self.crossRate = crossRate
        for i in range(size):
            shuffle(cities)
            self.individuals.append(Individual(cities))


def read_from_gui():
    screen_x = 500
    screen_y = 500

    city_color = [10, 10, 200]  # blue
    city_radius = 3

    font_color = [255, 255, 255]  # white

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Exemple')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)

    def draw(listCities):
        screen.fill(0)
        for city in listCities:
            pygame.draw.circle(screen, city_color, (city.x, city.y), city_radius)
        text = font.render("Nombre: %i" % len(listCities), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

    cities = []
    draw(cities)

    collecting = True
    cityCounter = 0

    while collecting:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
            elif event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                cities.append(City(f"v{cityCounter}", x, y))
                cityCounter += 1
                draw(cities)

    return cities


def reading_from_file(filename):
    cityList = []
    with open(filename) as file:
        for line in file:
            args = line.split()
            cityList.append(City(args[0], args[1], args[2]))
    return cityList


def ga_solve(file=None, gui=True, maxtime=0):
    cities = []
    if file is None:
        cities = read_from_gui()
    else:
        cities = reading_from_file(file)

    pop = Population(10, 0.001, 7, cities)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ga_solve(sys.argv[1])
    else:
        ga_solve()
