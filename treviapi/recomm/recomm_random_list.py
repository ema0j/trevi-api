import numpy as np

def generate_random_list(filename, ran, num) :
	cnt = 0
	glist = []
	f = open(filename, 'w')
	while cnt < num : 
		rlist = []
		for i in range(ran) :
			rlist.append(i)
		rlist = np.random.permutation(rlist)
		rlist = [str(k) for k in rlist]
		if rlist not in glist :
			glist.append(rlist)
			cnt+=1
			s = ",".join(rlist)
			f.write(s)
			f.write('\n')
	f.close()

#generate_random_list(5000, 50)
