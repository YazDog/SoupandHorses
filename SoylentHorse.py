from selenium import webdriver
from bs4 import BeautifulSoup
import time
import numpy
import json
import random
# plotly sucks balls
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from DoggySeleniumV2 import race_souper, race_name, fetch_race


#html = open('todayshtml.html', 'r')
#
#soup = BeautifulSoup(html, 'html.parser')
#


def flucsIsolate(horse):

    flux = json.loads(horse['flux'])
    win = float(horse['win'])
    flux.append(win)

    flucsmag = numpy.array([num / flux[-1] for num in flux])
    flucs = numpy.array(flux)



    return flucs, flucsmag



# graphs from yasin's race object, more work is needed to graph from tim's
# more work is needed in general
def grapher(race):

    xdir = numpy.linspace(0, 7, 7)


    graphlist = []
    maxflucmag = 1
    minflucmag = 1
    
    for horse in race:
      if not horse['win'] == 'SCR':
        hname = horse['name']
        flucs, flucsmag = flucsIsolate(horse)
      
      else:
        continue
        
      plt.plot(xdir, flucsmag, label=hname)
    
        
    fontP = FontProperties()
    fontP.set_size('small')
    # plt.ylim(minflucmag, maxflucmag*1.3)

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
              ncol=3, fancybox=True, shadow=True, prop=fontP)

    plt.show()



def userBetting(race):
    names = []
    for horse in race:
        names.append(horse[1])
    horses = []
    while True:
        horse_name = input('Enter a horse name ')
        if horse_name in names:
            horses.append(horse_name)
        elif horse_name == 'quit':
            break
    print(horses)

# grapher(race)


class Race(object):

    def __init__(self, race):
        self.race = race
        self.goodhorses = {}


    def simpleInv(self):
        print('doing simpleInv')
        for horse in race:
            name = horse['name']
            if not json.loads(horse['flux']):
                continue
            else: # horse has flucs, is not scratched
                flucs, flucsmag = flucsIsolate(horse)

            if flucsmag[0] > 1:
                self.goodhorses[name] = {'odds': [horse['win'], horse['place']]}

        return self.goodhorses



    def drvInv(self): # not done yet
        print('doing drvInv')
        xdir = numpy.linspace(0, 6, 6)
        for horse in race:
            name = horse['name']
            if not json.loads(horse['flux']):
                continue
            else: # horse has flucs, is not scratched
                flucs, flucsmag = flucsIsolate(horse)

            f = flucsmag
            FMD = numpy.array([f[1]-f[0], f[2]-f[1], f[3]-f[2], f[4]-f[3], f[5]-f[4], f[6]-f[5]])

            plt.plot(xdir, FMD, label= horse['name'])
            if FMD[5] < 0:
                self.goodhorses[name] = {'odds': [horse['win'], horse['place']]}

        fontP = FontProperties()
        fontP.set_size('small')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                   ncol=3, fancybox=True, shadow=True, prop=fontP)
        plt.show()

        return self.goodhorses

    def randInv(self): # randomly generates a horse from the race list
        print('doing randInv')
        holdinghorses = []
        for horse in race:
            if not json.loads(horse['flux']):
                continue
            else:  # horse has flucs, is not scratched
                holdinghorses.append(horse)

        goodhorse = random.choice(holdinghorses)
        name = goodhorse['name']
        self.goodhorses[name] = {'odds': [goodhorse['win'], goodhorse['place']]}

        return self.goodhorses

    def RRInv(self): # Randomly generates up to 5 horses from the race list
        print('doing RRInv')
        holdinghorses = []
        for horse in race:
            if not json.loads(horse['flux']):
                continue
            else:  # horse has flucs, is not scratched
                holdinghorses.append(horse)

        size = random.choice([1,2,3,4,5])

        for i in range(size):
            goodhorse = random.choice(holdinghorses)
            name = goodhorse['name']
            self.goodhorses[name] = {'odds': [goodhorse['win'], goodhorse['place']]}

        return self.goodhorses # Rand

    def overTenBet(self):
        pass

#print(race)
#print(simpleInve(race))
#drvInv(race)


html = fetch_race('https://www.tab.com.au/racing/2016-10-20/PAKENHAM/PAK/R/8')
race = race_souper(html)
# print(race)

R = Race(race)
print(R.race)
R.drvInv()
print(R.goodhorses)
