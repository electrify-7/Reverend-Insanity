import sqlite3
import sys
import extract_chapters  # assumes both scripts in same folder

DB_PATH = 'novel.db'

def create_db(conn):
    c = conn.cursor()
    # FTS5 virtual table: chapter_id unindexed (for filtering), title & content indexed
    c.execute('''
    CREATE VIRTUAL TABLE IF NOT EXISTS chapters
    USING fts5(
        chapter_id UNINDEXED,
        title,
        content
    );
    ''')
    conn.commit()

def load_chapters(conn, chapters):
    c = conn.cursor()
    # Replace or insert
    c.executemany(
        'INSERT INTO chapters (chapter_id, title, content) VALUES (?, ?, ?);',
        chapters
    )
    conn.commit()

if __name__ == '__main__':
    epub_file = sys.argv[1]
    chapters = extract_chapters.extract_chapters(epub_file)

    conn = sqlite3.connect(DB_PATH)
    create_db(conn)
    load_chapters(conn, chapters)
    conn.close()
    print(f"Loaded {len(chapters)} chapters into {DB_PATH}")
