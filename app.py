from flask import Flask
app = Flask(__name__)
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
