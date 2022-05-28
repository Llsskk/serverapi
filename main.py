# This Python file uses the following encoding: utf-8
import os

from flask import Flask, jsonify, request
from flask_ngrok import run_with_ngrok
from flask_restful import Api, Resource, reqparse
from blogs import engine, blogs, session, get_authors, auhtor, get_blogs_, comments, \
    get_comment

# ПОДКЛЮЧАЕМ БИБЛИОТЕКИ И ЗАВИСИМОСТИ

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)
run_with_ngrok(app)


# ПОДКЛЮЧАЕМ NGROK СЕРВЕР


@app.route("/")
def hello():
    return "Hello server"


# ГЛАВНАЯ СТРАНИЦА


class BLOGS(Resource):

    def get(self):
        posts = get_blogs_()
        results = [dict(row) for row in posts]
        return jsonify({'results': [dict(row) for row in posts]})

    def post(self):
        data = request.get_json()
        for blog_s in data["blogs"]:
            data2 = blogs(blog_s['Author'], blog_s['Title'], blog_s['Content'], blog_s['DatePost'])
            session.add(data2)
        session.commit()

    def put(self, BlogID):
        data_ = request.get_json()
        data = session.query(blogs).get(BlogID)
        for blog_s in data_["blogs"]:
            data.Author = blog_s['Author']
            data.Title = blog_s['Title']
            data.Content = blog_s['Content']
            data.DatePost = blog_s['DatePost']
        session.commit()


# КЛАСС С РЕДАКТИРОВАНИЕМ БЛОГА

class AUTHORS(Resource):

    def get(self):
        posts = get_authors()
        return jsonify({'results': [dict(row) for row in posts]})

    def post(self):
        data_2 = request.get_json()
        for auhtor_s in data_2["auhtor"]:
            data2 = auhtor(auhtor_s['FirstName'], auhtor_s['LastName'], auhtor_s['Email'],
                           auhtor_s['Phone'], auhtor_s['DateRegistration'])
            session.add(data2)
        session.commit()

    def put(self, AuthorID):
        data_ = request.get_json()
        data = session.query(auhtor).get(AuthorID)
        for blog_s in data_["auhtor"]:
            data.Author = blog_s['Author']
            data.Title = blog_s['Title']
            data.Content = blog_s['Content']
            data.DatePost = blog_s['DatePost']
        session.commit()


# КЛАСС С РЕДАКТИРОВАНИЕМ АВТОРОВ


class BLOGSsearch(Resource):

    def get(self):
        data = request.form['name']
        # data = request.get_data(as_text=True)
        conns = engine.connect()
        with conns as conn:
            cur = conn.execute("SELECT Title, Content FROM blogs WHERE Title = '%s' " % data)
            posts = cur.fetchall()
        # results = [dict(row) for row in posts]
        return jsonify({'results': [dict(row) for row in posts]})


api.add_resource(BLOGSsearch, '/bl_search')


# ПОИСК БЛОГА
class AUTHsearch(Resource):

    def get(self):
        data = request.form['mail']
        # data = request.get_data(as_text=True)
        conns = engine.connect()
        with conns as conn:
            cur = conn.execute("SELECT FirstName, LastName FROM auhtor WHERE Email = '%s'" % data)
            posts = cur.fetchall()
        # results = [dict(row) for row in posts]
        return jsonify({'results': [dict(row) for row in posts]})


api.add_resource(AUTHsearch, '/au_search')


# ПОИСК АВТОРА
class comsearch(Resource):

    def get(self):
        data = request.form['author']
        # data = request.get_data(as_text=True)
        conns = engine.connect()
        with conns as conn:
            cur = conn.execute("SELECT FirstName, LastName FROM comments WHERE Author = '%s'" % data)
            posts = cur.fetchone()
        # results = [dict(row) for row in posts]
        return jsonify({'results': [dict(row) for row in posts]})


api.add_resource(comsearch, '/co_search')


# ПОИСК КОММЕНТАРИЯ
class COMMENTS(Resource):

    def get(self):
        posts = get_comment()
        return jsonify({'results': [dict(row) for row in posts]})

    def post(self):
        data_2 = request.get_json()
        for com_s in data_2["comments"]:
            data2 = comments(com_s['BlogID'], com_s['Author'], com_s['Content'], com_s['DateComment'])
            session.add(data2)
        session.commit()

    def put(self, CommentID):
        data_ = request.get_json()
        data = session.query(comments).get(CommentID)
        for blog_s in data_["comments"]:
            data.Author = blog_s['Author']
            data.Title = blog_s['Title']
            data.Content = blog_s['Content']
            data.DatePost = blog_s['DatePost']
        session.commit()


# КЛАСС С РЕДАКТИРОВАНИЕМ КОММЕНТАРИЯ

api.add_resource(BLOGS, '/bl', '/bl', '/bl_put/<BlogID>')
api.add_resource(AUTHORS, '/au', '/au', '/au_put/<AuthorID>')
api.add_resource(COMMENTS, '/co', '/co', '/co_put/<CommentID>')
# ДОБАВЛЯЕМ КЛАССЫ ДЛЯ ВЫЗОВА API МЕТОДОВ

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # БЕРЕТ ХОСТ ДЛЯ ПОДКЛЮЧЕНИЯ NGROK
    app.run()

