# trevi :fountain:
Trevi, a fountain spouting with musics all over the world.

Current Status
-------------

- Simple music recommendation page using LastFM api
- Implemented collaborative filtering algorithm using clustering
- http://127.0.0.1:8000/musics/
- Use Django

# Usage
- List DB : http://127.0.0.1:8000/musics/
- Get music recommendation : http://127.0.0.1:8000/musics/recomm/get/0/3/
- Upload music and get music recommendation : http://127.0.0.1:8000/musics/recomm/update/0/she+will+be+loved/3/




Last Status
--------------
cf_simple.zip
- 데이터 파일(data.csv), 코드 파일(cf_sample.py) 
- user 1257명의 가수 285명에 대한 선호도 데이터(Last.fm)를 바탕으로 collaborative filtering하는 간단한 예제 코드
- 각 user에게 추천 아이템을 정해주기까지(Item-based 추천 한 뒤 이를 바탕으로 다시 user-based 추천) 시간이 굉장히 오래 걸리므로 이 부분을 해결할 방법 필요
- Minhash을 이용한 추천엔진 또는 map-reduced 대용량 추천 알고리즘(아래 링크 참조) 등 참고 가능
- 현재 데이터가 정적으로 주어졌을 때 추천할 아이템을 한꺼번에 계산해내는 방식 -> 실시간(streaming)으로 데이터를 얻을 때 어떤 식으로 적용할 수 있는지 생각해봐야함


Raw Data
- Last.fm에서 얻을 수 있음. http://labrosa.ee.columbia.edu/millionsong/lastfm#work
- Getting the dataset 참조


Ref
- 예제 출처 http://www.salemmarafi.com/code/collaborative-filtering-with-python/
- 매우 가벼운 실시간 추천 엔진(MinHash) http://bakyeono.net/post/2015-09-15-naver-deview-day-2-session-6-realtime-recommendation-engine-on-laptop.html#minhash
- Map-reduced 대용량 추천 알고리즘 http://readme.skplanet.com/?p=2509
