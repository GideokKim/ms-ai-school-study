# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

def numerical_diff(f, x, h=1e-4):
    """함수의 미분값을 수치적으로 계산"""
    return (f(x+h) - f(x-h)) / (2*h)

def function_1(x):
    """2차 함수 정의"""
    return 0.01*x**2 + 0.1*x 

def tangent_line(f, x0):
    """x0에서의 접선을 계산하는 함수"""
    d = numerical_diff(f, x0)
    y0 = f(x0)
    # 접선 식: y = f(x0) + f'(x0)(x - x0)
    return lambda x: d*(x - x0) + y0

# 🎨 그래프 생성
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)

# 함수 그래프 데이터 생성
x = np.arange(-10.0, 20.0, 0.1)
y = function_1(x)

# 🔹 특정 점에서의 접선 추가
x0 = 5  # 접점의 x 좌표
tf = tangent_line(function_1, x0)
y2 = tf(x)

# 그래프 그리기
ax.plot(x, y, label='f(x)', linewidth=2)
ax.plot(x, y2, '--', color='red', label='Tangent Line', linewidth=2)

# 🔹 접점 표시
ax.scatter([x0], [function_1(x0)], color='red', s=100, label='Tangent Point')

# 축 설정
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.set_title('2D Function with Tangent Line')
ax.legend(loc='upper left')

# 그리드 추가
ax.grid(True, linestyle='--', alpha=0.7)

plt.show()