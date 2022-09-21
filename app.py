from audioop import reverse
from importlib.resources import contents
from os import name
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decouple import config
import sys


app = Flask(__name__)
Bootstrap(app)
#db_connect = config('CONNECT_STRING')
#app.config["SQLALCHEMY_DATABASE_URI"] = db_connect #string de conexão privada SQLALCHEMY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

"""
CREATE TABLE tasks (
    id int NOT NULL,
    content varchar(200) NOT NULL,
    completed INT,
    PRIMARY KEY (id)  
);
"""

#modelo de dados do BD
class Tarefas(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    details = db.relationship("Detalhes", backref='task', uselist=False) #ultimo campo garante que eh 1:1 

    def __repr__(self):
        return '<Task %r>' % self.content

class Detalhes(db.Model):
    __tablename__ = "details"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))


"""
pra construir o BD:

flask shell
from app import db
"""
db.create_all()
#quit()
"""
"""
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        #task = Tarefas.query.order_by(Tarefas.id.desc()).first()

        new_task = request.form['content']
        task_details = Detalhes(content=request.form['details'])
        new_task = Tarefas(content=new_task, details=task_details)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Erro ao escrever no banco"
    else:
        tasks = Tarefas.query.order_by(Tarefas.id).all()
        return render_template('index.html', tasks=tasks)

@app.route('/complete/<int:id>')
def complete(id):
    task = Tarefas.query.get_or_404(id)
    task.completed = 1
    try:
        db.session.commit()
        return redirect('/')
    except:
        return "Erro ao atualizar campo concluir"
    

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Tarefas.query.get_or_404(id)
    detalhes = task_to_delete.details # não esquecer de apagar das tabelas adicionais
    try:
        db.session.delete(task_to_delete)
        db.session.delete(detalhes)
        db.session.commit()
        return redirect('/')
    except:
        return "Erro deletar banco de dados"

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update (id):
    task = Tarefas.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        task.details.content = request.form['details']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Erro update banco de dados'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
