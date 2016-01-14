# Tool Function for RecommEngine

def get_zero_vec(num):
	zero = []
	for i in range(num):
		zero.append(0)
	return zero

def get_concat(idx, num, ran) :
	concat = []
	cnt = 0
	while cnt < num:
		concat.append(idx%ran)
		idx+=1
		cnt+=1
	return concat

def save_mat2csv(filename, mat, colname, rowname):
	f = open(filename, 'w')
	for cc in colname :
		f.write(str(cc)+",")
	f.write("\n")
	for rr in rowname :
		f.write(str(rr)+",")
	f.write("\n")
	for row in mat :
		for elem in row :
			f.write(str(elem)+",")
		f.write("\n")
	f.close()
	print filename, " file SAVED"

def read_csv2mat(filename) :
	f = open(filename, 'r')
	mat = []
	line = f.readline()
	col_list = line[:-2].split(',')
	line = f.readline()
	row_list = line[:-2].split(',')
	while True:
		line = f.readline()
		if not line : break

		row = map(int,line[:-2].split(','))
		mat.append(row)
	
	return [col_list, row_list, mat]

def calculate_jaccard(test_stream, friend_stream) : 
	union = 0
	intersection = 0
	for i in range(len(test_stream)):
		if test_stream[i] or friend_stream[i] :
			union+=1
		if test_stream[i] and friend_stream[i] : 
			intersection +=1
	return float(intersection)/float(union)
