from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/',methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@app.route('/users-profile',methods=['POST', 'GET'])
def info_usuario():
    return render_template('users-profile.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)