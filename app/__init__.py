from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_envvar('CHIMERA_DEVELOPMENT_SETTINGS')

@app.route('/')
def index():
    return 'Flask is running!'


@app.route('/data')
def names():
    data = {"names": ["John", "Jacob", "Julie", "Jennifer"]}
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
