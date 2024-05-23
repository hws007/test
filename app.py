from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

def draw_ellipse(point1, point2, distance_sum):
    center = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)
    d = np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    a = (d / 2) + (distance_sum / 2)
    b = np.sqrt((distance_sum / 2)**2 - (d / 2)**2)
    theta = np.arctan2(point2[1] - point1[1], point2[0] - point1[0])
    t = np.linspace(0, 2 * np.pi, 100)
    x = center[0] + a * np.cos(t) * np.cos(theta) - b * np.sin(t) * np.sin(theta)
    y = center[1] + a * np.cos(t) * np.sin(theta) + b * np.sin(t) * np.cos(theta)

    plt.plot(x, y)
    plt.scatter([point1[0], point2[0], center[0]], [point1[1], point2[1], center[1]], color='red')
    plt.text(point1[0], point1[1], '  P1', fontsize=10)
    plt.text(point2[0], point2[1], '  P2', fontsize=10)
    plt.text(center[0], center[1], '  Center', fontsize=10)
    plt.axis('equal')
    plt.grid()

    # 그래프를 base64 이미지로 변환
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        x1 = float(request.form['x1'])
        y1 = float(request.form['y1'])
        x2 = float(request.form['x2'])
        y2 = float(request.form['y2'])
        distance_sum = float(request.form['distance_sum'])

        point1 = (x1, y1)
        point2 = (x2, y2)

        img_base64 = draw_ellipse(point1, point2, distance_sum)
        return render_template('result.html', img_data=img_base64)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
