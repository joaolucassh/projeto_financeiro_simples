from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financeiro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Lancamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Lancamento {self.id} - {self.descricao}>'

@app.route('/')
def index():
    lancamentos = Lancamento.query.order_by(Lancamento.data.desc()).all()
    return render_template('index.html', lancamentos=lancamentos)

@app.route('/novo', methods=['POST'])
def novo():
    tipo = request.form['tipo']
    descricao = request.form['descricao']
    valor = float(request.form['valor'])
    lanc = Lancamento(tipo=tipo, descricao=descricao, valor=valor)
    db.session.add(lanc)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    lanc = Lancamento.query.get_or_404(id)
    if request.method == 'POST':
        lanc.tipo = request.form['tipo']
        lanc.descricao = request.form['descricao']
        lanc.valor = float(request.form['valor'])
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', lanc=lanc)

@app.route('/deletar/<int:id>')
def deletar(id):
    lanc = Lancamento.query.get_or_404(id)
    db.session.delete(lanc)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

