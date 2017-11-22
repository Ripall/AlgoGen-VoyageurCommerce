import pygame, sys
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
from collections import namedtuple
from random import shuffle, randint

City = namedtuple('City', 'name,x,y')


class Individual:

    def __init__(self, cities):
        self.cities = list(cities)
        self.score = 0

    def mutate(self):
        valMax = len(self.cities)-1
        i1 = randint(0,valMax)

        i2 = randint(0,valMax)
        while i2 == i1:
            i2 = randint(0,valMax)

        temp = self.cities[i1]
        self.cities[i1] = self.cities[i2]
        self.cities[i2] = temp

    def cross_breeding(self,individual):
        pass

    def fitness(self):
        value = 0
        for i, city in enumerate(self.cities):
            value += abs(city.x-self.cities[i-1].x)+abs(city.y-self.cities[i-1].y)
        self.score = value


class Population:

    def __init__(self, size, mutationRate, crossRate, cities):
        self.individuals = []
        self.size = size
        self.mutationRate = mutationRate
        self.crossRate = crossRate
        for i in range(size):
            shuffle(cities)
            self.individuals.append(Individual(cities))

    def selection(self):
        for individual in self.individuals:
            individual.fitness()
            print(individual.score)

        self.individuals = sorted(self.individuals, key=lambda x: x.score)

        self.individuals = self.individuals[:self.size]

    def run(self):
        # Crossover

        # Selection
        self.selection()
        # Mutation
        for individual in self.individuals:
            if randint(0,100) < self.mutationRate:
                individual.mutate()

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
            cityList.append(City(args[0], int(args[1]), int(args[2])))
    return cityList


def ga_solve(file=None, gui=True, maxtime=0):
    cities = []
    if file is None:
        cities = read_from_gui()
    else:
        cities = reading_from_file(file)

    pop = Population(5, 10, 7, cities)
    pop.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ga_solve(sys.argv[1])
    else:
        ga_solve()
