from flask import Flask, render_template, request
import requests
from pymongo import MongoClient
import datetime
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # MongoDB 연결
    with MongoClient('mongodb://localhost:27017/') as client:
        db = client['news']
        data = db['nwer']

        # 쿼리 가져오기
        page = request.args.get('page', type=int, default=1)  # 페이지
        query = request.args.get('query')
        query1_str = request.args.get('query1')
        query2_str = request.args.get('query2')

        # 쿼리1과 쿼리2가 비어있는 경우 처리
        if not query1_str or not query2_str:
            return render_template('result.html', news=[], page=page, total_pages=0)

        query1 = datetime.datetime.strptime(query1_str, "%Y-%m-%d")  # query값 년월일로 변환
        query2 = datetime.datetime.strptime(query2_str, "%Y-%m-%d")
        news = []

        for movie in data.find({'PressCompany': query}):  # 언론사 
            first = datetime.datetime.strptime(movie['date'][0:10], "%Y.%m.%d")  # date값 년월일로 변환
            if query1 <= first <= query2:  # 시작일 <= 내가 찾는 데이터 날짜 <= 마지막일
                date = movie['date']
                Category = movie['Category']
                PressCompany = movie['PressCompany']
                Title = movie['Title']
                Article = movie['Article']
                Url = movie['Url']
                news.append({'date': date, 'Category': Category, 'PressCompany': PressCompany, 'Title': Title, 'Article': Article, 'Url': Url})

        # 페이징 처리
        per_page = 10  # 페이지당 결과 수
        total_results = len(news)
        total_pages = (total_results + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_news = news[start:end]

        return render_template('result.html', news=paginated_news, page=page, total_pages=total_pages)




if __name__ == '__main__':
    app.run(debug=True)
