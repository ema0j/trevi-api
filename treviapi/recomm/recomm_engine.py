import os
import json
import sqlite3

from recomm_tool import *
from recomm_random_list import generate_random_list

class RecommEngine() :
	def __init__(self, dbpath) : 
		self.dbdata = dbpath
		
		self.playlist_list = []
		self.track_list = []
		self.mat = []

		self.cluster_id = []
		self.cluster_set = []
	
	def run(self):
		### Part 1 : fetch data and make mat ###
		conn = sqlite3.connect(self.dbdata)
		sql = "select recomm_music.track from recomm_music"
		res = conn.execute(sql)
		track_data = res.fetchall()

		for elem in track_data :
			if elem[0] not in self.track_list :
				self.track_list.append(elem[0])
		
		sql = "select recomm_music.playlist_id, count(*) from recomm_music group by recomm_music.playlist_id"
		res = conn.execute(sql)
		playlistgroup_data = res.fetchall()
		#valid check
		if len(playlistgroup_data[0][0]) == 0 :
			playlistgroup_data.remove(playlistgroup_data[0])
		for i in range(len(playlistgroup_data)):
			sql = "select recomm_music.track from recomm_music where playlist_id='%d'" % int(playlistgroup_data[i][0])
			res = conn.execute(sql)
			data = res.fetchall()
			zero_vec = get_zero_vec(len(self.track_list))
			for j in range(len(data)) : 
				zero_vec[self.track_list.index(data[j][0])] = 1
			self.mat.append(zero_vec)
			self.playlist_list.append(playlistgroup_data[i][0])
		print "fill the matrix DONE ... size : ", len(self.mat), len(self.mat[0])


		### Part 2 : hash-reduced mat ###
		rlist_file = "./recomm/rlist_set.txt"
		reduced_mat = []
		if len(self.playlist_list) < 50 : 
			generate_random_list(rlist_file, len(self.playlist_list), len(self.playlist_list))
		else : 
			generate_random_list(rlist_file, len(self.playlist_list), 50)

		hash_func = self.hash_from_file(rlist_file)
		for h in hash_func:
			reduced_mat.append(self.get_hashed_row(h))	
		print "hash-reduced mat DONE ... size : ", len(reduced_mat), len(reduced_mat[0])
			
	
		### Part 3 : clustering ### 50 sig-concat w/ 4 rows
		#make cluster
		if len(self.playlist_list) < 50 : 
			sig_len = 2
		else : 
			sig_len = 4

		cluster_id = []
		cluster_set = []
		for i in range(len(reduced_mat[0])) : 
			for j in range(len(reduced_mat)) :
				concat = get_concat(j, sig_len, len(reduced_mat))
				cid = [j]
				for k in range(sig_len) :
					cid.append(reduced_mat[concat[k]][i])
				if cid not in cluster_id :
					cluster_id.append(cid)
					cluster_set.append([i])
				else :
					idx = cluster_id.index(cid)
					cluster_set[idx].append(i)
			if i%200 == 0 : 
				print "clustering ... ", i
	
		new_cluster_id = []
		new_cluster_set = []
		for i in range(len(cluster_set)):
			if len(cluster_set[i])>3: # Threshold 3
				new_cluster_id.append(cluster_id[i])
				new_cluster_set.append(cluster_set[i])
		self.cluster_id = new_cluster_id
		self.cluster_set = new_cluster_set
	
		del reduced_mat
		del cluster_id
		del cluster_set
		del new_cluster_id
		del new_cluster_set

	def get_recomm(self, test_title):
		test_idx = self.title_list.index(test_title)
		
		test_stream = [] 
		for k in range(len(self.mat)):
			test_stream.append(self.mat[k][test_idx])

		# test_stream to hashed sig
		hash_func = self.hash_from_file("./recomm/rlist_set.txt")
		minhash=[]
		for h in hash_func:
			idx = 0
			while True:
				if idx == len(test_stream) :
					minhash.append(0)
					break
				if test_stream[h[idx]] == 1 :
					minhash.append(idx+1)
					break
				idx += 1
		
		# concat and find cluster
		friends=[]
		for i in range(len(minhash)) :
			concat = get_concat(i, 4, len(minhash))
			cid = [i]
			for k in range(4) :
				cid.append(minhash[concat[k]])
			if cid in self.cluster_id :
				idx = self.cluster_id.index(cid)
				for check in self.cluster_set[idx] :
					if check in friends :
						r = friends.index(check)
						del friends[r]
				friends += self.cluster_set[idx]

		# calculate similarity in clusters
		result = []
		for idx in friends : 
			friend_stream = []
			for k in range(len(self.mat)):
				friend_stream.append(self.mat[k][idx])
			result.append((self.title_list[idx], calculate_jaccard(test_stream, friend_stream)))
		result = sorted(result, key = lambda x:x[1], reverse=True)
		return result

	def hash_from_file(self,hfile) :
		f = open(hfile, 'r')
		hash_set = []
		while True :
			line = f.readline()
			if not line : break

			s = map(int, line[:-1].split(','))
			hash_set.append(s)
		return hash_set

	def get_hashed_row(self, hf) :
		row = []
		for i in range(len(self.mat[0])):
			idx = 0
			while True:
				if idx == len(self.mat) :
					row.append(0)
					break
				if self.mat[hf[idx]][i] == 1 :
					row.append(idx+1)
					break
				idx += 1
		return row
