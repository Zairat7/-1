# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Review
from utils.services import ReviewProcessor

app = Flask(__name__)
# Безопасность: в реальном проекте взять из .env через os.getenv
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Инициализация базы данных
with app.app_context():
    db.create_all()

@app.route('/reviews', methods=['GET'])
def get_reviews():
    """GET /reviews — получить список отсортированных отзывов"""
    all_reviews = Review.query.all()
    # Применяем кастомный алгоритм сортировки слиянием
    sorted_reviews = ReviewProcessor.merge_sort(all_reviews)
    return render_template('index.html', reviews=sorted_reviews)

@app.route('/reviews', methods=['POST'])
def add_review():
    """POST /reviews — добавить отзыв через HTML-форму"""
    product = request.form.get('product')
    text = request.form.get('text')
    rating = request.form.get('rating')

    if product and text and rating:
        new_review = Review(product=product, text=text, rating=int(rating))
        db.session.add(new_review)
        db.session.commit()
    
    return redirect(url_for('get_reviews'))

@app.route('/reviews/upload', methods=['POST'])
def upload_json():
    """POST /reviews/upload — загрузить JSON-файл"""
    if 'file' not in request.files:
        return redirect(url_for('get_reviews'))
    
    file = request.files['file']
    if file and file.filename.endswith('.json'):
        # Временное сохранение для обработки менеджером контекста
        file_path = os.path.join('instance', file.filename)
        file.save(file_path)
        
        # Вызов Класса 2 для обработки данных
        data = ReviewProcessor.load_from_json(file_path)
        
        for item in data:
            review = Review(
                product=item.get('product'),
                text=item.get('text'),
                rating=int(item.get('rating', 0))
            )
            db.session.add(review)
        
        db.session.commit()
        os.remove(file_path) # Удаляем временный файл
        
    return redirect(url_for('get_reviews'))

@app.route('/reviews/delete/<int:id>', methods=['POST', 'DELETE'])
def delete_review(id):
    """DELETE/POST /reviews/<id> — удалить отзыв"""
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('get_reviews'))

if __name__ == '__main__':
    app.run(debug=True)
