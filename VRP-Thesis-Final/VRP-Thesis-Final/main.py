from Solution import Solution
from Graph import Graph
from Vertix import Vertix
from Tools import Tools
from Sector import Sector
import numpy as np
import Vertix
import csv
import math
import subprocess
import os
import openpyxl
import copy
import threading
import random
import folium
from timeit import default_timer as timer
 
def main():  
    start = timer()

    coordinatesFile = 'TurkishCitiesCoordinates (Anakara Depot)1.csv'
    criteriaFile = 'TurkishCitiesDistances(Ankara).xlsx'
    weightsFile = 'Weights-test.xlsx'
    sectorsFilesDirectory = 'Sectors'

    ###Solving Variables###
    numberOfSectors = 8                            #The number of sectors in the graph which is depenedant on the number of vehicles 
    optimizationIterations = 990                  #The Optimization iterations after which the execution will be terminated
    neighbourhoodMin = 0.6
    neighbourhoodMax = 1.5
    localPheromoneUpdateValue = 0.05
    globalPheromoneUpdateValue = -0.03
    deadEndCounterInitial = 10
    performanceMonitorCounterInitial = 20
    numberOfVerticesToObtainInitial = 1
    numberOfCandidatesFromEachSectorInitial = 1
    repeatCounterInitial = 20
    InitialAnalysisPercentage = 1.2
    sectorMinSize = 8                              #The minimum size allowed for each sector in the graph
    sectorMaxSize = 12                             #The maximum size allowed for each sector in the graph


    neighbourhoodStepSize = (neighbourhoodMax - neighbourhoodMin) / (deadEndCounterInitial - 1)
    sectorsFilesNameInitial = sectorsFilesDirectory + "/iteration"
    Tools.sectorFilesCleaner(sectorsFilesDirectory)

    masterGraph = Graph(numberOfSectors, coordinatesFile, criteriaFile, weightsFile, sectorMinSize, sectorMaxSize)
    masterGraph.initiateSectors()
        #print('error!')
        #a = 1
    masterGraph.mapWrite('Maps/map.html')

    masterGraph.calculateRoutes('TSP-Bruno.mod',
                                '%s' %(sectorsFilesNameInitial),
                                '%s' %(sectorsFilesNameInitial))
    bestScore = masterGraph.updateTotalCost()
    bestScoreIndex = 0
    bestScoreCombinedDiameters = masterGraph.getcombinedDiameters() * InitialAnalysisPercentage

    solutions = np.array([], Solution)
    terminals = np.array([], int)
    currentSolution = Solution(masterGraph)


    currentSolution.setfatherId(None)
    #solutions.flags.__setattr__(zerosize_ok, True)
    currentSolution.setlocalTime(timer() - start)
    currentSolution.setglobalTime(timer() - start)
    currentSolution.graph.updateCostsForAllSectors()
    currentSolution.writeToXlsx('Solutions/Solution.xlsx')
    solutions = np.append(solutions, [copy.deepcopy(currentSolution)])
    prevSolutionIndex = 0

    currentSolution.graph.initiateOptimization()
    performanceCounter = performanceMonitorCounterInitial
    terminationFlag = 0

    for i in range(1, optimizationIterations):
        if terminationFlag == 1:
            break

        print ('Iteration #%s Started!' %(i))
        loopTimeStart = timer()    
        neighbourhoodSize = neighbourhoodMin
        numberOfVerticesToObtain = numberOfVerticesToObtainInitial
        numberOfVerticesToObtainPerSector = numberOfCandidatesFromEachSectorInitial
        repeatCounter = repeatCounterInitial

        counter = deadEndCounterInitial
        while True:
            uniqueSolutionFlag = 0
            if counter <= 0:
                if repeatCounter <= 0:
                    terminationFlag = 1
                    break

                else:
                    terminals = np.append(terminals, [i - 1])
                    currentSolution = copy.deepcopy(solutions[bestScoreIndex])
                    prevSolutionIndex = bestScoreIndex
                    counter = deadEndCounterInitial
                    performanceCounter = performanceMonitorCounterInitial
                    neighbourhoodSize = neighbourhoodMin
                    numberOfVerticesToObtain += 1
                    numberOfVerticesToObtainPerSector += 1

                    repeatCounter -= 1
                    print ('Dead End! Starting back at solution #%s' %(bestScoreIndex))

            elif performanceCounter <= 0:
                terminals = np.append(terminals, [i - 1])
                currentSolution = copy.deepcopy(solutions[bestScoreIndex])
                performanceCounter = performanceMonitorCounterInitial
                prevSolutionIndex = bestScoreIndex
                counter = deadEndCounterInitial
                repeatCounter = repeatCounterInitial
                neighbourhoodSize = neighbourhoodMin
                print ('Performance Error! Starting back at solution #%s' %(bestScoreIndex))

            if terminationFlag == 1:
                break

            if currentSolution.graph.optimizationIteration(numberOfVerticesToObtain, neighbourhoodSize, localPheromoneUpdateValue, globalPheromoneUpdateValue) > 0:
                if currentSolution.isUnique(solutions):
                    #currentSolution.graph.mapWrite('test.html', neighbourhoodSize)
                    uniqueSolutionFlag = 1

                else:
                    print ('solution not unique!')
                    #currentSolution.graph.mapWrite('test.html', neighbourhoodSize)
                    currentSolution.graph.globalPheromoneUpdate(-1 * globalPheromoneUpdateValue)

            #print ('iteration no. %s' %(i))
            neighbourhoodSize += neighbourhoodStepSize
            counter -= 1
            if uniqueSolutionFlag == 1:
                break


        if terminationFlag == 1:
            break

        currentSolutionCombinedDiameters = currentSolution.graph.getcombinedDiameters()
        if currentSolution.graph.getcombinedDiameters() > (bestScoreCombinedDiameters * 2):
            print ('Diameters too big: %s, %s' %(currentSolution.graph.getcombinedDiameters(), bestScoreCombinedDiameters))
            currentSolution.graph.settotalCost(None)
            performanceCounter -= 1


        if currentSolution.graph.gettotalCost() is not None:
            currentSolution.graph.calculateRoutes('TSP-Bruno.mod', '%s%s' %(sectorsFilesNameInitial, i), '%s%s' %(sectorsFilesNameInitial, i))
            currentSolution.graph.updateCostsForAllSectors()
            currentSolution.graph.updateTotalCost()
            if currentSolution.graph.gettotalCost() < bestScore:
                bestScore = currentSolution.graph.gettotalCost()
                bestScoreIndex = i
                performanceCounter = performanceMonitorCounterInitial
                bestScoreCombinedDiameters = currentSolution.graph.getcombinedDiameters() * InitialAnalysisPercentage

            else:
                performanceCounter -= 1

        currentSolution.graph.mapWrite('Maps/map%s.html' %(i), neighbourhoodSize)
        print('Best Score Index: %s' %(bestScoreIndex))
        currentSolution.setfatherId(prevSolutionIndex)
        currentSolution.setlocalTime(timer() - loopTimeStart)
        currentSolution.setglobalTime(timer() - start)
        if currentSolution.graph.gettotalCost() is not None:
            currentSolution.writeToXlsx('Solutions/solution%s.xlsx' %(i))

        solutions = np.append(solutions, [copy.deepcopy(currentSolution)])
        prevSolutionIndex = i
        print ('Iteration time: %s, execution time: %s' %(currentSolution.getlocalTime(), currentSolution.getglobalTime()))

        print ('Counters: Performance: %s, DeadEnd: %s, Repeat: %s' %(performanceCounter, counter, repeatCounter))
        print('-------------------------------------------------------------')

    terminals = np.append(terminals, [len(solutions) - 1])
    end = timer()
    print ('time: %s' %(end - start))
    Tools.soltuionPathWriter('Solutions/SolutionTree.txt', solutions, terminals)
    Tools.sectorFilesCleaner(sectorsFilesDirectory)
    return 0


if __name__ == "__main__": main()
