from app import create_app
from flask_cors import CORS

# Создаём приложение сразу, на верхнем уровне
app = create_app()

# Настраиваем CORS (можешь расширить список origin-ов)
CORS(app, resources={r"/*": {"origins": [
    "https://yourdomain.com"
]}})

# Это нужно только для локального запуска
if __name__ == '__main__':
    app.run(debug=True)
