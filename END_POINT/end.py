from flask import Flask, jsonify

app = Flask(__name__)

# Функция проверки простого числа
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Контроллер: проверка на простоту
@app.route('/api/isprime/<int:number>', methods=['GET'])
def check_prime(number):
    result = is_prime(number)
    return jsonify({
        "number": number,
        "is_prime": result
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
