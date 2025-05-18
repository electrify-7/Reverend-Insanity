import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_chapters(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    chap_num = 0

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        chap_num += 1
        # Get plain text
        html = item.get_content()
        text = BeautifulSoup(html, 'html.parser').get_text(separator='\n')
        # Use item.get_name() or item.get_id() as raw title if needed
        title = item.get_name()
        chapters.append((chap_num, title, text))

    return chapters

if __name__ == '__main__':
    import sys
    epub_file = sys.argv[1]
    out = extract_chapters(epub_file)
    print(f"Extracted {len(out)} chapters from {epub_file}")
    # Optionally: pickle or json-dump for inspection
