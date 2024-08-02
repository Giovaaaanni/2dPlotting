import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random
import re
import copy
import matplotlib

#matplotlib.use('TkAgg')
random.seed(0)


class Points(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Bin(object):

    def __init__(
            self,
            binID,
            leftGravityPoints,
            itemList,
            W,
            H
    ):
        self.binID = binID
        self.leftGravityPoints = leftGravityPoints
        self.itemList = itemList
        self.W = W
        self.H = H


class Item(object):

    def __init__(
            self,
            itemID,
            w,
            h,
            posizioneItem,
    ):
        self.itemID = itemID
        self.h = h
        self.w = w
        self.posizioneItem = Points(posizioneItem[0], posizioneItem[1])

    def Xfinal(self):
        return self.w + self.posizioneItem.x

    def Yfinal(self):
        return self.h + self.posizioneItem.y


def print_plot(current_bin):
    # define Matplotlib figure and axis
    fig, ax = plt.subplots()

    # initialize the plot
    ax.plot()

    # add rectangle to plot
    for item in current_bin.itemList:
        ax.add_patch(Rectangle((item.posizioneItem.x, item.posizioneItem.y), item.w, item.h,
                               edgecolor='black', fill=False, lw=1))
        ax.text((item.posizioneItem.x + item.Xfinal()) / 2, (item.posizioneItem.y + item.Yfinal()) / 2, item.itemID,
                ha='center', va='center')

    x_position = range(0, bin_list[0].W + 1, math.floor(bin_list[0].W / 10))
    y_position = range(0, bin_list[0].H + 1, math.floor(bin_list[0].H / 10))
    # x_position = range(0, bin_list[0].W + 1, 1)
    # y_position = range(0, bin_list[0].H + 1, 1)

    ax.set_axisbelow(True)  #metto la griglia in secondo piano rispetto ai rettangoli
    ax.set_aspect('equal')  #per avere gli assi nella stessa scala
    # metto la griglia con frequenza 10 per cento delle dimensioni dei bin
    ax.set_xticks([tick for tick in x_position])
    ax.set_yticks([tick for tick in y_position])
    ax.set_xticks(x_position, minor=True)
    ax.set_yticks(y_position, minor=True)
    ax.grid(which='both')
    # ax.autoscale()

    plt.title("Bin " + str(current_bin.binID))
    # metto in evidenza i placement points
    plt.plot([corner.x for corner in current_bin.leftGravityPoints], [corner.y for corner in current_bin.leftGravityPoints], marker='o', linestyle='none')
    # i puntini neri sono l'estremo sx inferiore dell'item
    plt.plot([item.posizioneItem.x for item in current_bin.itemList], [item.posizioneItem.y for item in current_bin.itemList], marker='.', color='black', linestyle='none')
    plt.show()


def printBins(bin_list):
    for b in range(3):
        print(bin_list[b].binID, " ha gli item: ")
        for item in bin_list[b].itemList:
            print(item.itemID, " ha gli posizione: ", item.posizioneItem.x, ";", item.posizioneItem.y,
                  " ha gli dimensioni ", item.w, " e ", item.h)


def objects_equal(bin1, bin2):
    if bin1.binID != bin2.binID:
        return False
    if len(bin1.itemList) != len(bin2.itemList):
        return False
    for item in range(len(bin1.itemList)):
        if bin1.itemList[item].itemID != bin2.itemList[item].itemID:
            return False
    if len(bin2.leftGravityPoints) != len(bin1.leftGravityPoints):
        return False
    for corner in range(len(bin1.leftGravityPoints)):
        if bin1.leftGravityPoints[corner].x != bin2.leftGravityPoints[corner].x or bin1.leftGravityPoints[corner].y != bin2.leftGravityPoints[corner].y:
            return False
    return True


def readSolution():
    file = open(path, 'r')

    # Read the entire content of the file
    input_sol = file.read()
    help1 = input_sol.split("W: ")[1]
    bin_width = int(re.match(r'(\d+)', help1).group(1))
    help2 = input_sol.split("H: ")[1]
    bin_height = int(re.match(r'(\d+)', help2).group(1))
    bin_sections = input_sol.split("Bin: ")[1:]
    bin_list = []

    for bin_section in bin_sections:
        lines = bin_section.strip().split("Corner:")
        bin_info = lines[0].strip()
        corner_info = lines[1].strip()

        # Extract bin ID
        bin_id = int(re.match(r'(\d+)', bin_info).group(1))  # uses a regular expression to find the first sequence of one or more digits (\d+)
        # group(1) retrieves the first matched group (the digits found).

        item_info = bin_info.strip().split("Item:")

        # Extract item information
        item_pattern = re.compile(r'\s*(\d+)\s*pos:\s*(\d+)\s*;\s*(\d+)\s*e\s*dim:\s*(\d+)\s*;\s*(\d+)')  # creo un oggetto simil item, es Item:  3 pos: 0;0 e dim: 9;9
        # \s*: Matches any whitespace characters (like spaces or tabs), zero or more times.
        items = []
        for match in item_pattern.finditer(
                item_info[1]):  # The finditer() function matches a pattern in a string and returns an iterator that yields the Match objects of all non-overlapping matches
            item_id = int(match.group(1))
            pos_x = int(match.group(2))
            pos_y = int(match.group(3))
            dim_w = int(match.group(4))
            dim_h = int(match.group(5))
            item = Item(item_id, dim_w, dim_h, (pos_x, pos_y))
            items.append(item)

        # Extract corner points
        #bin_list[0].leftGravityPoints.append(Points(p.x, p.y))
        corner_points = [Points(int(c.split(';')[0]), int(c.split(';')[1])) for c in corner_info.split() if int(c.split(';')[0]) >= 0]

        # Create Bin object
        bin_obj = Bin(binID=bin_id, leftGravityPoints=corner_points, itemList=items, W=bin_width, H=bin_height)
        bin_list.append(bin_obj)
    # else:
    #     print("Programma terminato")
    #     exit()
    return bin_list


def readParziale(parz):
    input_sol = parz
    help1 = input_sol.split("W: ")[1]
    bin_width = int(re.match(r'(\d+)', help1).group(1))
    help2 = input_sol.split("H: ")[1]
    bin_height = int(re.match(r'(\d+)', help2).group(1))
    bin_sections = input_sol.split("Bin: ")[1:]
    bin_list = []

    for bin_section in bin_sections:
        lines = bin_section.strip().split("Corner:")
        bin_info = lines[0].strip()
        corner_info = lines[1].strip()

        bin_id = int(re.match(r'(\d+)', bin_info).group(1))  # uses a regular expression to find the first sequence of one or more digits (\d+)
        item_info = bin_info.strip().split("Item:")
        item_pattern = re.compile(r'\s*(\d+)\s*pos:\s*(\d+)\s*;\s*(\d+)\s*e\s*dim:\s*(\d+)\s*;\s*(\d+)')  # creo un oggetto simil item, es Item:  3 pos: 0;0 e dim: 9;9
        items = []
        for match in item_pattern.finditer(
                item_info[1]):  # The finditer() function matches a pattern in a string and returns an iterator that yields the Match objects of all non-overlapping matches
            item_id = int(match.group(1))
            pos_x = int(match.group(2))
            pos_y = int(match.group(3))
            dim_w = int(match.group(4))
            dim_h = int(match.group(5))
            item = Item(item_id, dim_w, dim_h, (pos_x, pos_y))
            items.append(item)

        corner_points = [Points(int(c.split(';')[0]), int(c.split(';')[1])) for c in corner_info.split() if int(c.split(';')[0]) >= 0]

        bin_obj = Bin(binID=bin_id, leftGravityPoints=corner_points, itemList=items, W=bin_width, H=bin_height)
        bin_list.append(bin_obj)

    return bin_list


def readIncrementSolution():
    file = open(path_increment, 'r')

    input_sol = file.read()

    split_data = input_sol.split("Start:")

    global parziali

    parziali = [("Start:" + part).strip() for part in split_data if part.strip()]


def plotFinalSolution(bin_list, specific_bin):
    if specific_bin < 0:
        for bin in bin_list:
            print_plot(bin)
    else:
        print_plot(bin_list[specific_bin])


corner_generation_strategies = ['V1Base', 'V2CornProj', 'V2CornProjDel', 'V3Crainic']
corn_gen = corner_generation_strategies[1]
placement_strategies = ["FirstFit", "FV"]
plac_strat = placement_strategies[1]
item_sorting_strategies = ["DAFHS", "DAFWS", "DH", "DW"]
item_strat = item_sorting_strategies[0]
corner_sorting_strategies = ["YX", "XY"]
corn_sort = corner_sorting_strategies[0]
inst = 'Martello_cl_1_item_25'
inst = 'cl_04_080_07'
inst = 'Blum_cl_1_inst_29_item_60'
inst = 'A10_44'
inst = 'item30_W20_H35'

path = ('C:/Users/ADMIN/Desktop/Lavoro/2DFirstFit/Instance_Results/' + inst + '/' + inst + "_" + corn_gen + '_' + plac_strat + '_'
        + item_strat + '_' + corn_sort + '.txt')  #'_current.txt'
path_increment = ('C:/Users/ADMIN/Desktop/Lavoro/2DFirstFit/Instance_Results/' + inst + '/' + inst + "_" + corn_gen + '_' + plac_strat + '_'
                  + item_strat + '_' + corn_sort + '_incremental.txt')  # _incremental_current.txt

parziali = []  # var in cui metto tutte le sol parziali della incrementale

def plotIncrementalSolution(specific_bin=None):
    if specific_bin is None:
        for parz in parziali:
            bin_list = readParziale(parz)
            for bin in bin_list:
                print_plot(bin)
    else:
        bin_state = Bin(binID=-1, leftGravityPoints=0, itemList=0, W=0, H=0)
        for parz in parziali:
            bin_list = readParziale(parz)
            for bin in bin_list:
                if bin.binID == specific_bin:
                    if not objects_equal(bin, bin_state):
                        bin_state = copy.deepcopy(bin_list[specific_bin])
                        print_plot(bin_list[specific_bin])  #posizionare qui il breakpoint
                        break
                    else:
                        continue


if __name__ == '__main__':
    bin_list = []
    bin_list = readSolution()
    readIncrementSolution()

    #plotIncrementalSolution(3)

    plotFinalSolution(bin_list, -1)
