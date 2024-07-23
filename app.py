import http.server
import socketserver
import json
from gtts import gTTS
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

PORT = 8000


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == '/login':
            self.handle_login()
        elif self.path == '/chat':
            self.handle_chat()

    def handle_login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        username = data.get('username')
        password = data.get('password')

        users = {'chitra@gmail.com': 'chitra123'}

        if username in users and users[username] == password:
            tts = gTTS(f"Hello, {username.split('@')[0]}! Welcome back!")
            tts.save('greet.mp3')
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(
                json.dumps({'message': 'Login successful', 'status': 'success', 'audio': 'greet.mp3'}).encode())
        else:
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Invalid credentials', 'status': 'failure'}).encode())

    def handle_chat(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        user_message = data.get('message')
        bot_response = self.get_bot_response(user_message)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'message': bot_response}).encode())

    def get_bot_response(self, message):
        with open('leave_data.json', 'r') as file:
            leave_data = json.load(file)

        for leave_type, balance in leave_data.items():
            if leave_type.lower() in message.lower():
                return f"You have {balance} days of {leave_type} remaining."

        # If no specific leave type is found, use a language model to generate a response
        return self.generate_model_response(message)

    def generate_model_response(self, message):
        model_name = "microsoft/DialoGPT-medium"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        new_user_input_ids = tokenizer.encode(message + tokenizer.eos_token, return_tensors='pt')
        chat_history_ids = model.generate(new_user_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        bot_response = tokenizer.decode(chat_history_ids[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)

        return bot_response


Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
