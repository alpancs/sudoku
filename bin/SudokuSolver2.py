import sys
import io
import os
import time

# mapper
# arr[x][y][v]: baris x kolom y nilai v di map ke suatu nilai
# toR: mapping dari nilai ke baris
# toC: mapping dari nilai ke kolom
# toC: mapping dari nilai ke nilai isi

arr = [[[0 for x in xrange(100)] for x in xrange(100)] for x in xrange(101)]
toR = [0 for x in xrange(1000001)]
toC = [0 for x in xrange(1000001)]
toV = [0 for x in xrange(1000001)]

# ukuran dari papan
size = int(raw_input())

box = -1

for i in xrange(1, size + 1):
	if (i * i == size):
		box = i
		break

# ukuran papan harus bilangan kuadrat

if (box == -1):
	print "Not a valid sudoku"
	exit()
	
# masukan sudoku
sudo = [[0 for x in xrange(100)] for x in xrange(100)]

# preprocess mapping

def preprocess():
	cnt = 1;

	for i in xrange(size):
		for j in xrange(size):
			for k in xrange(1, size + 1):
				arr[i][j][k] = cnt
				toR[cnt] = i
				toC[cnt] = j
				toV[cnt] = k
				cnt = cnt + 1

# menghitung CNF

def countCNF():
	ret = 0
	su = ""
	# Filled fields
	for i in xrange(size):
		for j in xrange(size):
			if (sudo[i][j] != 0):
				ret = ret + 1
				su += str(arr[i][j][sudo[i][j]]) + ' 0\n'

	# Each field contains at least 1 number
	for i in xrange(size):
		for j in xrange(size):
			for k in xrange(1, size + 1):
				su += str(arr[i][j][k]) + ' '
			ret = ret + 1
			su += ' 0\n'
		
	# No field contains two numbers
	for i in xrange(size):
		for j in xrange(size):
			for k1 in xrange(1, size + 1):
				for k2 in xrange(k1 + 1, size + 1):
					ret = ret + 1
					su += str(-arr[i][j][k1]) + ' ' + str(-arr[i][j][k2]) + ' 0\n'

	# Each number must occur exactly once in each row
	for j in xrange(size):
		for k in xrange(1, size + 1):
			for i in xrange(size):
				su += str(arr[i][j][k]) + ' '
			ret = ret + 1
			su += '0\n'

	for i1 in xrange(size):
		for i2 in xrange(i1 + 1, size):
			for j in xrange(size):
				for k in xrange(1, size + 1):
					ret = ret + 1
					su += str(-arr[i1][j][k]) + ' ' + str(-arr[i2][j][k]) + ' 0\n'

	# Each number must occur exactly once in each column
	for i in xrange(size):
		for k in xrange(1, size + 1):
			for j in xrange(size):
				su += str(arr[i][j][k]) + ' '
			ret = ret + 1
			su += '0\n'

	for i in xrange(size):
		for j1 in xrange(size):
			for j2 in xrange(j1 + 1, size):
				for k in xrange(1, size + 1):
					ret = ret + 1
					su += str(-arr[i][j1][k]) + ' ' + str(-arr[i][j2][k]) + ' 0\n'

	# Each number must occur exactly once in each box (sqrt(N) * sqrt(N))

	for ii in xrange(box):
		for jj in xrange(box):
			for i in xrange(box):
				for j in xrange(box):
					for k in xrange(1, size + 1):
						su += str(arr[ii * box + i][jj * box + j][k]) + ' '
					ret = ret + 1
					su += '0\n'

	for ii in xrange(box):
		for jj in xrange(box):
			for i1 in xrange(size):
				for i2 in xrange(i1 + 1, size):
					for k in xrange(1, size + 1):
						ret = ret + 1
						su += (str(-arr[ii * box + i1 / box][jj * box + i1 % box][k]) + ' ' + str(-arr[ii * box + i2 / box][jj * box + i2 % box][k]) + ' 0\n')
	
	for i in xrange(size):
		for j in xrange(size):
			if (sudo[i][j] != 0):
				ret = ret + 1
				su += (str(arr[i][j][sudo[i][j]]) + ' 0\n')
				
	return (ret, su)

#######

preprocess()

for i in xrange(size):
	sudo[i] = map(int, raw_input().split(' '))

# menghitung banyaknya clauses dari CNF	
(num, CNF) = countCNF()

variable = size * size * size
nsol = 7

solution = [[[0 for i in xrange(size)] for j in xrange(size)] for k in xrange(nsol)]

sol = 0

for k in xrange(nsol):

	curfile = open('minisat.in', 'wb')

	curfile.write('p cnf ' + str(variable) + ' ' + str(num) + '\n')

	curfile.write(CNF)

	curfile.close()

	# menjalankan minisat
	os.system("./minisat minisat.in minisat.out")

	curfile = open('minisat.out', 'rb')
	st = curfile.read().splitlines()
	# print st[0]
	if (st[0] == "SAT"):
		dummy = ""
		res = map(int, st[1].split(' '))
		for i in xrange(len(res)):
			if (res[i] > 0):
				dummy += str(-res[i]) + ' '
				solution[sol][toR[res[i]]][toC[res[i]]] = toV[res[i]]
		dummy += '0\n'
		sol += 1
		num += 1
		CNF += dummy
	else:
		break
			
outputfile = open('result.txt', 'wb')
outputfile.write(str(sol) + '\n')
for k in xrange(sol):
	for i in xrange(size):
		for j in xrange(size - 1):
			outputfile.write(str(solution[k][i][j]) + ' ')
		outputfile.write(str(solution[k][i][size - 1]) + '\n')

outputfile.close()