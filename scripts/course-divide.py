#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Sorts subjects based on evaluation responses and divides among n people """
#    course-divide.py
#    Copyright (C) 2016  Ole Herman Schumacher Elgesem

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os
from bs4 import BeautifulSoup

__author__ = "Ole Herman Schumacher Elgesem"
__email__ = "olehelg@uio.no"
__version__ = "0.1"

def subject_data(subject, linenum):
    linenum -= 1
    filep = open(subject+".html", "r")
    empty = False
    str = "result"
    for i, line in enumerate(filep):
        if i == linenum:
            str = line
            break
        elif i == 32:
            if(line.strip() == "Dette skjemaet har ikke mottatt noen svar"):
                empty = True
                break
        elif i > linenum:
            break
    filep.close()
    if(empty == True):
        return (subject, 0)
    return (subject, int(str.strip()))

def course_divide(folder, num):
    subjects = []
    for file in os.listdir(folder):
        if file.endswith(".html"):
            subjects.append(file[0: -5])
    data = []
    for s in subjects:
        data.append(subject_data(s, 37))
    data.sort(key=lambda x: x[1]);
    data.reverse()

    print("There are "+str(len(data))+" courses total.")

    people = []
    for i in range(num):
        people.append([])
    i = 0
    order = []
    while i < len(data):
        for j in range(num):
            order.append(j)
            i += 1
        for j in range(num):
            order.append(num-j-1)
            i += 1

    i = 0
    while i < len(data):
        subject = data[i]
        if(subject[1] == 0):
            break
        people[order[i]].append(subject)
        i += 1
    empty_courses = []
    while i < len(data):
        empty_courses.append(data[i])
        i += 1

    for i, p in enumerate(people):
        print("Person " + str(i) + ":")
        print(people[i])
        sum = 0
        for s in people[i]:
            sum += s[1]
    print("Empty evaluations("+str(len(empty_courses))+"):")
    print(empty_courses)

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Usage: ./course_divide.py num [folder]")
        exit()
    folder = sys.argv[2]
    num = int(sys.argv[1])
    course_divide(folder, num)