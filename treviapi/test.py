import sqlite3
	
def get_zero_vec(num):
	zero = []
	for i in range(num):
		zero.append(0)
	return zero

def test() : 
	conn = sqlite3.connect("./db.sqlite3")
	sql = "select recomm_music.track from recomm_music"
	res = conn.execute(sql)
	track_data = res.fetchall()

	track_list = []
	tag_list = [] #tag name list
	mat = []
	
	for elem in track_data :
		if elem[0] not in track_list :
			track_list.append(elem[0])
	
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
		zero_vec = get_zero_vec(len(track_list))
		for j in range(len(data)) : 
			zero_vec[track_list.index(data[j][0])] = 1
		mat.append(zero_vec)
		
	return mat

