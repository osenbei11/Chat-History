from pyproject import connect_db as db

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '00'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def show_add_form():
    if request.method == 'POST':
        title = request.form['title']
        my_question = request.form['my_question']
        teacher_answer = request.form['teacher_answer']

        session['preview_data'] = {'title': title, 'my_question': my_question, 'teacher_answer': teacher_answer}

        return redirect(url_for('show_preview'))
    else:
        return render_template('add.html')

@app.route('/preview', methods=['GET', 'POST'])
def show_preview_form():
    if request.method == 'POST':
        title = request.form['title']
        my_question = request.form['my_question']
        teacher_answer = request.form['teacher_answer']

        session['preview_data'] = {'title': title, 'my_question': my_question, 'teacher_answer': teacher_answer}

        return redirect(url_for('show_preview'))
    else:
        return render_template('add.html')

@app.route('/preview/show', methods=['GET'])
def show_preview():
    preview_data = session.get('preview_data')

    return render_template('preview.html', preview_data=preview_data)

@app.route('/preview/edit', methods=['POST'])
def edit_chat():
    preview_data = session.get('preview_data')

    if preview_data:
        return render_template('add.html', preview_data=preview_data)
    else:
        return redirect(url_for('show_add_form'))

@app.route('/preview/submit', methods=['POST'])
def submit_chat():
    preview_data = session.get('preview_data')

    if preview_data:
        db.insert_chat(preview_data['title'], preview_data['my_question'], preview_data['teacher_answer'])
        session.pop('preview_data', None)
        return redirect(url_for('show_add_form'))
    else:
        return redirect(url_for('show_add_form'))

@app.route('/read')
def read_chats():
    db.initialize_database()
    chats = db.get_all_chats()
    return render_template('read.html', chats=chats)

@app.route('/show_chat/<int:index>')
def show_chat(index):
    db.initialize_database()
    chats = db.get_all_chats()

    if 0 <= index < len(chats):
        chat = chats[index]

        chat_id = chat[0]

        prev_index = index - 1 if index > 0 else None
        next_index = index + 1 if index < len(chats) - 1 else None
        return render_template('show_chat.html', chat=chat, chat_id=chat_id,
                               prev_index=prev_index, next_index=next_index)
    else:
        return "Invalid index"

if __name__ == '__main__':
     app.run(debug=True)