import cache_api ,json
import sqlite3

conn = sqlite3.connect('Wordsdb.sqlite')
cur = conn.cursor()
#cur.execute('DROP TABLE IF EXISTS Movies')
cur.execute('''
CREATE TABLE IF NOT EXISTS Words (Word TEXT, rhy TEXT)''')

Word = input("Enter a word: ")
cur.execute('SELECT Word FROM Words WHERE Word=?', (Word,) )
if cur.fetchone() is None:
    baseurl = "https://api.datamuse.com/words"
    params={ 'rel_rhy':Word}
    res = cache_api.get(baseurl,params=params, temp_cache_file="datamuse_cache.txt")
    res = json.loads(res)
    res = [d['word'] for d in res]
    cur.execute('''INSERT INTO Words (Word, rhy)
    VALUES (?, ?)''', (Word,json.dumps(res)))
else:
    cur.execute('SELECT rhy FROM Words WHERE Word=?', (Word,) )
    res = cur.fetchone()

conn.commit()
cur.close()
print(res)
