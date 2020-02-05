from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:060400@localhost/test'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean(), default = False)
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'error'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    delete_task = Todo.query.get_or_404(id)
    # if delete_task.deleted:
    #     abort(404)

    try:
        db.session.delete(delete_task)
        # delete_task.deleted = True
        db.session.commit()
        return redirect('/')
    except:
        return 'error'
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    update_task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        update_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return error
    else:
        return render_template('update.html', task = update_task)

if __name__ == "__main__":
    app.run(debug=True)