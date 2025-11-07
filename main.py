import requests
import sys
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# .envファイルの読み込み
load_dotenv()
 
# API-KEYの設定
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
 
# ISBNの出力の文体など
def get_bookinfo(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    
    response = requests.get(url)
    
    data = response.json()
    
    if "items" in data and len(data["items"]) > 0:
        title = data["items"][0]["volumeInfo"]["title"]
        authors = data["items"][0]["volumeInfo"]["authors"]
        return f"{title} : {authors}"    
    else:
        return "何の本を読んでんだ？"


def main():
    print("ISBNを入力してください。")
    input_isbn = input()
    if len(input_isbn) == 13:
        isbn = input_isbn
        book_info = get_bookinfo(isbn)
        print(book_info)
        time.sleep(1)
        gemini_pro = genai.GenerativeModel("gemini-2.5-flash")
        # book_infoを食わせる
        prompt = book_info + "という作品の主要な登場人物達の属性、役割、性格を一言で簡潔に箇条書きしていってください。一文に纏めて(、)で区切って出力してください"
        response = gemini_pro.generate_content(prompt)
        print(response.text)

    else:
        print(f"13文字の半角数字を入力してください")
        sys.exit(1)


if __name__ == "__main__":
    main()

    #9784101010038
    #9784150123543
    #9784150119553