import pygame


class City:

    def __init__(self,name,x,y):
        self.name = name
        self.x = x
        self.y = y


def ga_solve(file=None, gui=True, maxtime=0):
    print("ga_solve")
