### CS 441, Fall 2022 - Program #2 - 11/13/22 - Dan Jang
### Solving the 8-Queens Problem using a Genetic Algorithm Agent

import numpy as np
import math
from matplotlib import pyplot
import random as rnd

## I. Initialization of Global Constants & Variables

POPULATION = 1000

ROWS = 8
COLUMNS = 8
QUEENS = 8

MUTATIONRATE = 1

## II. Setup Classes & Helper Functions

class ChessPos:
    def __init__(self, pos=None):
        
        self.pos = pos if pos else genPos()
        
        self.fitness = genFit(self.pos)

def genPos():
    return genRows()

def genRows():
    pos = list(range(ROWS))
    rnd.shuffle(pos)
    
    return pos

def random():
    randompos = []
    
    for _ in range(ROWS):
        randompos.append(rnd.randrange(0, COLUMNS))
        
    return randompos

def initPopulation():
    newpopulation = []
    
    for _ in range(POPULATION):
        newpopulation.append(ChessPos())
    
    return newpopulation

## III. Genetic Algorithm Functions, e.g. fitness, crossover, mutation, etc.

def attackCrissCross(col1, col2, row1, row2):
    return (row1 + col1) == (row2 + col2) or \
        ((ROWS - 1 - row1) + col1) == ((ROWS - 1 - row2) + col2)

def attackHorizontal(row1, row2):
    return row1 == row2

def attack(col1, col2, row1, row2):
    return attackCrissCross(col1, col2, row1, row2) \
        or attackHorizontal(row1, row2)
    
def concurrentAttacks(pos):
    attacks = 0
    
    for idx1 in range(QUEENS):
        for idx2 in range(idx1 + 1, QUEENS):
            if attack(idx1, idx2, pos[idx1], pos[idx2]):
                attacks += 1

    return attacks

def maxConcurrentAttacks():
    return math.comb(QUEENS, 2)

def genFit(pos):
    # return maxConcurrentAttacks() - concurrentAttacks(pos)
    return maxConcurrentAttacks() - concurrentAttacks(pos) + 1

def totalFitnessSum(population):
    score = 0
    for idx in population:
        score += idx.fitness
    
    return score

def avgFitness(population):
    return totalFitnessSum(population) / \
        ((maxConcurrentAttacks()+1) * POPULATION)
        
def parentalSelection(population):
    
    count = 0
    
    fitnessScore = totalFitnessSum(population)
    firstParentValue = rnd.randrange(0, fitnessScore)
    secondParentValue = rnd.randrange(0, fitnessScore)
    
    firstParent = secondParent = population[0]
    
    for idx in range(len(population)):
        
        if count >= firstParentValue:
            firstParent = population[idx]
            break
        
        count += population[idx].fitness
    
    count = 0
    
    for idx2 in range(len(population)):
        if count >= secondParentValue:
            secondParent = population[idx2]
            count += population[idx2].fitness
            break
        count += population[idx2].fitness
        
    return firstParent, secondParent
        
def crossOver(firstparent, secondparent):
    firstchild, secondchild = uniqueCriss(firstparent, secondparent)
    
    firstchild = mutation(firstchild)
    secondchild = mutation(secondchild)
    
    return ChessPos(firstchild), ChessPos(secondchild)
    
def uniqueCriss(firstparent, secondparent):
    
    randpos = rnd.randrange(1, COLUMNS - 1)
    
    firstchild = []
    secondchild = []
    
    for idx1 in range(0, COLUMNS):
        for idx2 in range(0, randpos):
            if secondparent.pos[idx1] == firstparent.pos[idx2]:
                firstchild.append(secondparent.pos[idx1])
    
    for idx in range(randpos, COLUMNS):
        firstchild.append(firstparent.pos[idx])
        
    for idx in range(0, randpos):
        secondchild.append(secondparent.pos[idx])
        
    
    for idx1 in range(0, COLUMNS):
        for idx2 in range(randpos, COLUMNS):
            if firstparent.pos[idx1] == secondparent.pos[idx2]:
                secondchild.append(firstparent.pos[idx1])
                
    return firstchild, secondchild

def mutation(child):
    if rnd.uniform(0,1) < MUTATIONRATE / 100:
        idx = rnd.sample(range(0, COLUMNS), 2)
        curr = child[idx[0]]
        
        child[idx[0]] = child[idx[1]]
        child[idx[1]] = curr

        return child
    
## III. Main Function to Run the Genetic Algorithm for the 8-Queen Puzzle Problem


def main():
    improvementCount = 0
    
    x = np.empty(1)
    y = np.empty(1)
    
    herd = initPopulation()
    avgfit = avgFitness(herd)
    
    print ("Average Fitness Scores: " + str(avgfit))
    
    x = np.append(x, 0)
    y = np.append(y, avgfit)
    
    for idx1 in range(1000):
        parents = herd
        herd = []
        
        for idx2 in range(int(POPULATION / 2)):
            if idx1 == 0 or idx1 == 100 or idx1 == 999:
                print("At position " + str(idx2) + ", individual: ", str(parents[idx2].pos), " - Fitness: " + str(parents[idx2].fitness))

            firstparent, secondparent = parentalSelection(parents)
            firstchild, secondchild = crossOver(firstparent, secondparent)
            
            pFit = genFit(firstparent.pos) + genFit(secondparent.pos)
            cFit = genFit(firstchild.pos) + genFit(secondchild.pos)
            
            if pFit < cFit:
                improvementCount += 1
                
            if pFit == cFit and rnd.randrange(0, 2) == 1:
                improvementCount += 1
                
            herd.append(firstchild)
            herd.append(secondchild)
            
        avgfit = avgFitness(herd)
        
        print("Average Fitness Score of Population of Population #" + str(idx1 + 1) + "): " + str(avgfit))
        
        x = np.append(x, idx1 + 1)
        y = np.append(y, avgfit)
        
    percentCalc = (improvementCount / ((POPULATION / 2) * 1000)) * 100
    print("Percent of Improvement was " + str(percentCalc) + "%.")
    
    pyplot.plot(x,y)
    pyplot.xlim([0, 1000])
    pyplot.ylim([0, 1])
    
    pyplot.show()
    
if __name__ == '__main__':
    main()