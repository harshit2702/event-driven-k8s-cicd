from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

messages = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.form.get('message')
        if msg:
            messages.append(msg)
            if len(messages) > 20:
                messages.pop(0)
        return redirect(url_for('index'))
    return render_template_string("""
    <html>
    <body>
        <h1>Messages</h1>
        <form method="post">
            <input name="message" placeholder="Type a message" required>
            <input type="submit" value="Add">
        </form>
        <ul>
        {% for msg in messages %}
            <li>{{ msg }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """, messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

