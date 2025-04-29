from flask import Flask, request, render_template
import math

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def solve():
    result = None
    if request.method == 'POST':
        try:
            a = float(request.form['a'])
            b = float(request.form['b'])
            c = float(request.form['c'])
            if a == 0:
                result = "Это не квадратное уравнение (a не должно быть 0)."
            else:
                d = b**2 - 4*a*c
                if d > 0:
                    x1 = (-b + math.sqrt(d)) / (2*a)
                    x2 = (-b - math.sqrt(d)) / (2*a)
                    result = f"Два корня: x₁ = {round(x1,2)}, x₂ = {round(x2,2)}"
                elif d == 0:
                    x = -b / (2*a)
                    result = f"Один корень: x = {round(x,2)}"
                else:
                    result = "Нет вещественных корней."
        except Exception as e:
            result = f"Ошибка: {e}"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)