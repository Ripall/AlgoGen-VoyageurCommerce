import pygame, sys
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
from collections import namedtuple
from random import shuffle, randint
import time

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

    def cross_breeding(self, individual):
        fa = True
        fb = True
        g = []
        n = len(self.cities)
        x = randint(0, n - 1)
        town = self.cities[x]
        y = individual.cities.index(town)
        g.append(town)
        while fa is True or fb is True:
            x = (x - 1) % n - 1
            y = (y + 1) % n - 1
            if fa is True:
                if self.cities[x] not in g:
                    g.insert(0, self.cities[x])
                else:
                    fa = False
            if fb is True:
                if individual.cities[y] not in g:
                    g.append(self.cities[y])
                else:
                    fb = False
        if len(g) < n:
            s = set(g)
            left = [x for x in self.cities if x not in s]
            shuffle(left)
            g = g + left
        return Individual(g)

    def fitness(self):
        value = 0
        for i, city in enumerate(self.cities):
            value += ((city.x-self.cities[i-1].x)**2+(city.y-self.cities[i-1].y)**2)**0.5
        self.score = value

    def __str__(self):
        string = ""
        for city in self.cities:
            string = string+" "+city.name
        return string



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
        self.individuals = sorted(self.individuals, key=lambda x: x.score)
        # prendre env 50 % des meilleurs et le reste aléa
        cut = int(self.size/2)
        remaining = self.size - cut
        temp = self.individuals.copy()
        self.individuals = self.individuals[:cut]
        temp = [x for x in temp if x not in self.individuals]
        shuffle(temp)
        for i in range(0, remaining):
            self.individuals.append(temp[i])

    def run(self, gui=False):
        # Crossover
        crossed = []
        for i in range(0, len(self.individuals)-1,2):
            if randint(0, 100) < self.crossRate:
                crossed.append(self.individuals[i].cross_breeding(self.individuals[i+1]))

        self.individuals = self.individuals+crossed

        # Mutation
        for individual in self.individuals:
            if randint(0, 100) < self.mutationRate:
                individual.mutate()

        # Selection
        self.selection()

        if gui:
            draw_path(self.individuals[0])

# Display constants
screen_x = 500
screen_y = 500

city_color = [10, 10, 200]  # blue
city_radius = 3

font_color = [255, 255, 255]  # white

def draw_path(individual):
    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Exemple')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)

    for i, city in enumerate(individual.cities):
        pygame.draw.line(screen, city_color, (individual.cities[i].x, individual.cities[i].y), (individual.cities[i-1].x, individual.cities[i-1].y))

    pygame.display.flip()


def read_from_gui():
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


def ga_solve(file=None, gui=True, maxTime = 0):
    startTime = time.time()
    cities = []
    if file is None:
        cities = read_from_gui()
    else:
        cities = reading_from_file(file)

    pop = Population(5, 5, 5, cities)

    if maxTime==0:
        average = 0
        stagnation = [-1]
        while average < stagnation[0]*0.99 or average > stagnation[0]*1.01:
            pop.run(gui)
            average=0
            stagnation.insert(0,pop.individuals[0].score)
            length = len(stagnation)
            if length>9:
                stagnation.pop()
                for n in stagnation:
                    average += n
                average /= length

    else:
        while time.time()-startTime < maxTime:
            pop.run(gui)

    names = [x.name for x in pop.individuals[0].cities]
    print (pop.individuals[0].score, names)
    return (pop.individuals[0].score, names)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ga_solve(sys.argv[1],True,0)
    else:
        ga_solve()
