import json
import openai
from flask import Flask, request, jsonify
from handler.main import ChatGPT

app = Flask(__name__)
apikey = "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"


@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', '')
    message = f"Hello, {name}!" if name else "Hello, World!"
    return jsonify({'message': message})


@app.route('/CreateUser', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    with open('handler/user_messages.json', 'r') as um:
        content = um.read()
        um_json = json.loads(content) if len(content) > 0 else {}
    um_json.update({f"{username}": []})
    with open('handler/user_messages.json', 'w') as um:
        json.dump(um_json, um)
    message = f"创建用户名成功,请记住你的用户名,后面会根据用户名与我交流哦~ 你的用户名为{username}"
    return jsonify({'message': message})


@app.route('/GetChat', methods=['GET'])
def get_chat():
    username = request.args.get('username', "")
    mq = request.args.get('message', "")
    openai.api_key = apikey
    chat_m = ChatGPT(username)
    with open('user_messages.json', 'r') as f:
        content = json.loads(f.read())
    flag = False
    for i, v in content.items():
        if i == username:
            flag = True
    if flag:
        for i in content[f"{username}"]:
            chat_m.messages.append(i)

    chat_m.messages.append({"role": "user", "content": mq})
    answer = chat_m.ask_gpt()
    chat_m.messages.append({"role": "assistant", "content": answer})
    chat_m.writeTojson()
    message = f"{answer}"
    return jsonify({'[萝卜GPT]': message})


@app.route('/Chat', methods=['POST'])
def chat():
    data = request.json
    username = data.get('username', "")
    mq = data.get('message', "")
    openai.api_key = apikey
    chat_m = ChatGPT(username)
    with open('user_messages.json', 'r') as f:
        content = json.loads(f.read())
    flag = False
    for i, v in content.items():
        if i == username:
            flag = True
    if flag:
        for i in content[f"{username}"]:
            chat_m.messages.append(i)

    chat_m.messages.append({"role": "user", "content": mq})
    answer = chat_m.ask_gpt()
    chat_m.messages.append({"role": "assistant", "content": answer})
    chat_m.writeTojson()
    message = f"{answer}"
    return jsonify({'[萝卜GPT]': message})


if __name__ == '__main__':
    app.run()
