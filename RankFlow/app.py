from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'rankflow-secret-key'

# Arquivo para armazenar dados
DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'products': [
            {
                'id': 1,
                'title': 'Oppenheimer',
                'category': 'movie',
                'release_date': '2023',
                'developer': 'Christopher Nolan',
                'description': 'A história de J. Robert Oppenheimer e o desenvolvimento da bomba atômica.',
                'created_at': '2024-01-01T00:00:00'
            },
            {
                'id': 2,
                'title': 'The Last of Us',
                'category': 'tv',
                'release_date': '2023',
                'developer': 'HBO',
                'description': 'Adaptação do aclamado jogo, mostrando a jornada de Joel e Ellie em um mundo pós-apocalíptico.',
                'created_at': '2024-01-02T00:00:00'
            },
            {
                'id': 3,
                'title': 'Duna: Parte Dois',
                'category': 'movie',
                'release_date': '2024',
                'developer': 'Denis Villeneuve',
                'description': 'Continuação épica da saga de Paul Atreides em Arrakis.',
                'created_at': '2024-01-03T00:00:00'
            },
            {
                'id': 4,
                'title': 'The Bear',
                'category': 'tv',
                'release_date': '2022',
                'developer': 'FX',
                'description': 'Um jovem chef retorna a Chicago para administrar o restaurante da família.',
                'created_at': '2024-01-04T00:00:00'
            },
            {
                'id': 5,
                'title': 'Parasita',
                'category': 'movie',
                'release_date': '2019',
                'developer': 'Bong Joon-ho',
                'description': 'Uma família pobre se infiltra na vida de uma família rica com consequências inesperadas.',
                'created_at': '2024-01-05T00:00:00'
            }
        ],
        'reviews': [
            {'id': 1, 'product_id': 1, 'type': 'critic', 'reviewer': 'Variety', 'score': 95, 'comment': 'Obra-prima cinematográfica.', 'created_at': '2024-01-01T00:00:00'},
            {'id': 2, 'product_id': 1, 'type': 'critic', 'reviewer': 'The Hollywood Reporter', 'score': 90, 'comment': 'Excelente narrativa histórica.', 'created_at': '2024-01-01T00:00:00'},
            {'id': 3, 'product_id': 1, 'type': 'user', 'reviewer': 'João Silva', 'score': 9.5, 'comment': 'Filme incrível!', 'created_at': '2024-01-01T00:00:00'},
            {'id': 4, 'product_id': 2, 'type': 'critic', 'reviewer': 'IGN', 'score': 92, 'comment': 'Adaptação perfeita do jogo.', 'created_at': '2024-01-02T00:00:00'},
            {'id': 5, 'product_id': 2, 'type': 'user', 'reviewer': 'Maria Santos', 'score': 9.0, 'comment': 'Série emocionante!', 'created_at': '2024-01-02T00:00:00'},
            {'id': 6, 'product_id': 3, 'type': 'critic', 'reviewer': 'Rotten Tomatoes', 'score': 88, 'comment': 'Espetáculo visual impressionante.', 'created_at': '2024-01-03T00:00:00'},
            {'id': 7, 'product_id': 3, 'type': 'user', 'reviewer': 'Pedro Costa', 'score': 8.5, 'comment': 'Melhor que a primeira parte!', 'created_at': '2024-01-03T00:00:00'},
            {'id': 8, 'product_id': 4, 'type': 'critic', 'reviewer': 'The New York Times', 'score': 93, 'comment': 'Drama intenso e envolvente.', 'created_at': '2024-01-04T00:00:00'},
            {'id': 9, 'product_id': 5, 'type': 'critic', 'reviewer': 'Metacritic', 'score': 96, 'comment': 'Obra-prima sul-coreana.', 'created_at': '2024-01-05T00:00:00'},
            {'id': 10, 'product_id': 5, 'type': 'user', 'reviewer': 'Ana Lima', 'score': 10.0, 'comment': 'Perfeito em todos os aspectos!', 'created_at': '2024-01-05T00:00:00'}
        ]
    }

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def calculate_metascore(product_id, data):
    """Calcula o Metascore (média ponderada das avaliações de críticos)"""
    critic_reviews = [r for r in data['reviews'] if r['product_id'] == product_id and r['type'] == 'critic']
    if not critic_reviews:
        return None
    return round(sum(r['score'] for r in critic_reviews) / len(critic_reviews), 1)

def calculate_user_score(product_id, data):
    """Calcula a pontuação dos usuários"""
    user_reviews = [r for r in data['reviews'] if r['product_id'] == product_id and r['type'] == 'user']
    if not user_reviews:
        return None
    return round(sum(r['score'] for r in user_reviews) / len(user_reviews), 1)

@app.route('/')
def index():
    data = load_data()
    products_with_scores = []
    
    for product in data['products']:
        product_copy = product.copy()
        product_copy['metascore'] = calculate_metascore(product['id'], data)
        product_copy['user_score'] = calculate_user_score(product['id'], data)
        product_copy['critic_count'] = len([r for r in data['reviews'] if r['product_id'] == product['id'] and r['type'] == 'critic'])
        product_copy['user_count'] = len([r for r in data['reviews'] if r['product_id'] == product['id'] and r['type'] == 'user'])
        products_with_scores.append(product_copy)
    
    # Ordenar por Metascore (maiores primeiro)
    products_with_scores.sort(key=lambda x: x['metascore'] if x['metascore'] else 0, reverse=True)
    
    return render_template('index.html', products=products_with_scores)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    data = load_data()
    product = next((p for p in data['products'] if p['id'] == product_id), None)
    
    if not product:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('index'))
    
    product_copy = product.copy()
    product_copy['metascore'] = calculate_metascore(product_id, data)
    product_copy['user_score'] = calculate_user_score(product_id, data)
    
    critic_reviews = [r for r in data['reviews'] if r['product_id'] == product_id and r['type'] == 'critic']
    user_reviews = [r for r in data['reviews'] if r['product_id'] == product_id and r['type'] == 'user']
    
    return render_template('product_detail.html', 
                         product=product_copy, 
                         critic_reviews=critic_reviews,
                         user_reviews=user_reviews)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        data = load_data()
        
        new_product = {
            'id': len(data['products']) + 1,
            'title': request.form['title'],
            'category': request.form['category'],
            'release_date': request.form['release_date'],
            'developer': request.form.get('developer', ''),
            'description': request.form.get('description', ''),
            'created_at': datetime.now().isoformat()
        }
        
        data['products'].append(new_product)
        save_data(data)
        
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('product_detail', product_id=new_product['id']))
    
    return render_template('add_product.html')

@app.route('/product/<int:product_id>/add-review', methods=['GET', 'POST'])
def add_review(product_id):
    data = load_data()
    product = next((p for p in data['products'] if p['id'] == product_id), None)
    
    if not product:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        new_review = {
            'id': len(data['reviews']) + 1,
            'product_id': product_id,
            'type': request.form['type'],
            'reviewer': request.form['reviewer'],
            'score': float(request.form['score']),
            'comment': request.form.get('comment', ''),
            'created_at': datetime.now().isoformat()
        }
        
        data['reviews'].append(new_review)
        save_data(data)
        
        flash('Avaliação adicionada com sucesso!', 'success')
        return redirect(url_for('product_detail', product_id=product_id))
    
    return render_template('add_review.html', product=product)

@app.route('/category/<category>')
def category_view(category):
    data = load_data()
    products = [p for p in data['products'] if p['category'] == category]
    
    products_with_scores = []
    for product in products:
        product_copy = product.copy()
        product_copy['metascore'] = calculate_metascore(product['id'], data)
        product_copy['user_score'] = calculate_user_score(product['id'], data)
        products_with_scores.append(product_copy)
    
    products_with_scores.sort(key=lambda x: x['metascore'] if x['metascore'] else 0, reverse=True)
    
    return render_template('category.html', category=category, products=products_with_scores)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
