from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
DB = 'novel.db'

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ''
    minc = ''
    maxc = ''
    if request.method == 'POST':
        query = request.form.get('q', '').strip()
        minc  = request.form.get('min', '').strip() or 1
        maxc  = request.form.get('max', '').strip() or 9999
        # run the search
        conn = sqlite3.connect(DB)
        cur  = conn.cursor()
        sql  = '''
            SELECT chapter_id,
                   snippet(chapters,'[',']','…',10)
            FROM chapters
            WHERE content MATCH ?
              AND chapter_id BETWEEN ? AND ?
            ORDER BY chapter_id
            LIMIT 50;
        '''
        cur.execute(sql, (query, minc, maxc))
        results = cur.fetchall()
        conn.close()

    return render_template('index.html',
                           results=results,
                           query=query,
                           minc=minc,
                           maxc=maxc)

if __name__ == '__main__':
    # listen on all interfaces so your phone can reach it on Wi-Fi
    app.run(host='0.0.0.0', port=5000, debug=True)
