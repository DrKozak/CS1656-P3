import argparse
import collections
import csv
import glob
import itertools
import math 
import os
import pandas
import re
import string
import sys

#starts program
def init():
    inputs_file = sys.argv[1]
    outputs = sys.argv[2]
    min_support_percentage = float(sys.argv[3]) #need to be a float
    min_confidence = float(sys.argv[4]) #need to be a float 

#generate all combos
    combo_dic = {} # count
    support_dic = {} # support
    rcounter = 0
    input_file = open(inputs_file)
    input_csv = csv.reader(input_file)
    for row in input_csv:
        input_list = list(row)
        
        input_list.pop(0)
        #convert list of items to string
        input_list = ''.join(input_list)
        list_len = len(input_list)
        for x in range(1, list_len + 1):
            power_set = list(itertools.combinations(input_list, x))
            for y in power_set:
        #convert each subset into single string
                y = ''.join(y)
                if y not in combo_dic:
                    combo_dic[y] = 1
                else:
                    combo_dic[y] = combo_dic[y] + 1
        rcounter = rcounter + 1       

#calculate elements + add to support_dic
    remove = []
    for element in combo_dic:
        support = combo_dic[element]/rcounter
        
        if support >= min_support_percentage:
            support_dic[element] = support
        else:
            remove.append(element)
    for element in remove:
        del combo_dic[element]

    supportList = []
    for element in support_dic:
        elementList = list(element)
        strSupp = support_dic[element]
       
        strrelement = "S," + "{0:.4f}".format(strSupp) + ","
        #hmmmmmmmmmmmmmmmmmm
        for con in elementList:
            strrelement = strrelement + con + ","
        strrelement = strrelement[:-1]
        supportList.append(strrelement)

#create
    conf_list = []
   
    for element in combo_dic:
        ele_list = list(element)
        #loop to the string's length
        if len(ele_list) == 2:
            combo0 = ele_list[0]
            combo1 = ele_list[1]
            combo01 = combo0 + combo1
            # 0 to 1
            
            if combo_dic[combo01]/combo_dic[combo0] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo01]/combo_dic[combo0])
                strrelement = strrelement + "," + combo0 + "," + "\'=>\'" + "," +combo1 #good line
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 1 to 0
            
            if combo_dic[combo01]/combo_dic[combo1] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo01]/combo_dic[combo1])
                strrelement = strrelement + ","  + combo1 + "," + "\'=>\'" +  "," + combo0
                if strrelement not in conf_list:
                    conf_list.append(strrelement)

        if len(ele_list) == 3:
            combo0 = ele_list[0]
            combo1 = ele_list[1]
            combo2 = ele_list[2]
            combo01 = combo0 + combo1
            combo02 = combo0 + combo2
            combo12 = combo1 + combo2
            combo012 = combo01 + combo2
            # 0 to 12
            if combo_dic[combo012]/combo_dic[combo0] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo012]/combo_dic[combo0])
                strrelement = strrelement + "," + combo0 + "," + "\'=>\'" +  "," + combo12
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 1 to 02
            if combo_dic[combo012]/combo_dic[combo1] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo012]/combo_dic[combo1])
                strrelement = strrelement + "," + combo1 + ","  + "\'=>\'" +  "," + combo02
                if strrelement not in conf_list:
                    conf_list.append(strrelement)

            # 2 to 01
            if combo_dic[combo012]/combo_dic[combo2] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo012]/combo_dic[combo2])
                strrelement = strrelement + "," + combo2 + ","  + "\'=>\'" + "," + combo01
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 12 to 0
            if combo_dic[combo012]/combo_dic[combo12] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo012]/combo_dic[combo12])
                strrelement = strrelement + "," + combo12 + ","  + "\'=>\'" + "," + combo0
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 02 t0 1
            if combo_dic[combo012]/combo_dic[combo02] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo012]/combo_dic[combo02])
                strrelement = strrelement + "," +  combo02 +  "," + "\'=>\'" +  "," + combo1
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 01 to 2
            if combo_dic[combo012]/combo_dic[combo01] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo012]/combo_dic[combo01])
                strrelement = strrelement + "," + combo01 + "," +  "\'=>\'" + "," + combo2
                if strrelement not in conf_list:
                    conf_list.append(strrelement)

        if len(ele_list) == 4:
            combo0 = ele_list[0]
            combo1 = ele_list[1]
            combo2 = ele_list[2]
            combo3 = ele_list[3]
            combo01 = combo0 + combo1
            combo02 = combo0 + combo2
            combo03 = combo0 + combo3
            combo12 = combo1 + combo2
            combo13 = combo1 + combo3
            combo23 = combo2 + combo3
            combo012 = combo01 + combo2
            combo013 = combo01 + combo3
            combo023 = combo02 + combo3
            combo123 = combo12 + combo3
            combo0123 = combo01 + combo23

            # 0 to 123
            if combo_dic[combo0123]/combo_dic[combo0] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo0])
                strrelement = strrelement + "," + combo0 + "," + "\'=>\'" + "," + combo123
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 1 to 023
            if combo_dic[combo0123]/combo_dic[combo1] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo023])
                strrelement = strrelement + "," + combo1 + "," +  "\'=>\'" + "," +  combo023
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 2 to 013
            if combo_dic[combo0123]/combo_dic[combo2] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo2])
                strrelement = strrelement + "," + combo2 + "," + "\'=>\'" + "," +  combo013
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 3 to 012
            if combo_dic[combo0123]/combo_dic[combo3] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo3])
                strrelement = strrelement + "," + combo3 + "," + "\'=>\'" + "," + combo012
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 01 to 23
            if combo_dic[combo0123]/combo_dic[combo01] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo01])
                strrelement = strrelement + "," + combo01 + "," +  "\'=>\'" + "," +  combo23
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 02 to 13
            if combo_dic[combo0123]/combo_dic[combo02] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo02])
                strrelement = strrelement + "," + combo02 + "," + "\'=>\'" + "," + combo13
                if strrelement not in conf_list:
                    conf_list.append(strrelement)

            # 03 to 12
            if combo_dic[combo0123]/combo_dic[combo03] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo03])
                strrelement = strrelement + "," + combo03 + "," + "\'=>\'" + "," + combo12
                if strrelement not in conf_list:
                    conf_list.append(strrelement)

            # 23 to 01
            if combo_dic[combo0123]/combo_dic[combo23] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo23])
                strrelement = strrelement + "," + combo23 + "," +  "\'=>\'" + "," +  combo01
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 13 to 02
            if combo_dic[combo0123]/combo_dic[combo13] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo13])
                strrelement = strrelement + "," + combo2 + "," +  "\'=>\'" + "," + combo01
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 12 to 03
            if combo_dic[combo0123]/combo_dic[combo12] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo12])
                strrelement = strrelement + "," + combo12 + "," +  "\'=>\'" + "," +  combo03
                if strrelement not in conf_list:
                    conf_list.append(strrelement)

            # 123 to 0
            if combo_dic[combo0123]/combo_dic[combo123] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo123])
                strrelement = strrelement + "," + combo123 + "," +  "\'=>\'" + "," +  combo0
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 023 to 1
            if combo_dic[combo0123]/combo_dic[combo023] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo023])
                strrelement = strrelement + "," + combo023 + "," + "\'=>\'" + "," +  combo1
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 013 to 2

            if combo_dic[combo0123]/combo_dic[combo013] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo013])
                strrelement = strrelement + "," + combo013 + "," +  "\'=>\'" + "," +  combo2
                if strrelement not in conf_list:
                    conf_list.append(strrelement)
            # 012 to 3
            if combo_dic[combo0123]/combo_dic[combo012] >= min_confidence:
                strrelement = "R," + "{0:.4f}".format(support_dic[element])
                strrelement = strrelement + "," + "{0:.4f}".format(combo_dic[combo0123]/combo_dic[combo012])
                strrelement = strrelement + "," + combo012 + "," + "\'=>\'" + "," + combo3
                if strrelement not in conf_list:
                    conf_list.append(strrelement)

    with open(outputs, 'w+') as out:
        for s in supportList:
            out.write(s + "\n")
        for s in conf_list:
            out.write(s + "\n")
        

if __name__ == "__main__": init()