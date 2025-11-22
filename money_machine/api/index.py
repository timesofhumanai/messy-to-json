from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "Alive! The server is working. Now we can add the AI back."

# Required for Vercel
if __name__ == '__main__':
    app.run()
