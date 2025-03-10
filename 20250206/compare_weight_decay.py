# coding: utf-8
import os
import sys

# 프로젝트 루트 디렉토리의 절대 경로를 얻습니다
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)  # 프로젝트 루트를 파이썬 경로의 첫 번째로 추가

import numpy as np
import matplotlib.pyplot as plt
from dataset.mnist import load_mnist  # dataset 폴더에서 mnist 모듈 import
from common.multi_layer_net import MultiLayerNet
from common.optimizer import SGD

print(f"Project root directory: {ROOT_DIR}")  # 디버깅을 위한 경로 출력
print(f"Python path: {sys.path}")  # 파이썬 경로 출력

plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

# 데이터 로드
(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True)

# 과대적합을 재현하기 위해 학습 데이터 수를 줄임
x_train = x_train[:300]
t_train = t_train[:300]

# 하이퍼파라미터 설정
max_epochs = 201
train_size = x_train.shape[0]
batch_size = 100
hidden_size_list = [100, 100, 100, 100, 100, 100]
learning_rate = 0.01
weight_decay_lambda = 0.1

# 두 네트워크 생성
network_normal = MultiLayerNet(input_size=784, hidden_size_list=hidden_size_list, output_size=10)
network_decay = MultiLayerNet(input_size=784, hidden_size_list=hidden_size_list, output_size=10,
                            weight_decay_lambda=weight_decay_lambda)

optimizer_normal = SGD(lr=learning_rate)
optimizer_decay = SGD(lr=learning_rate)

# 결과 저장용 리스트
train_acc_list_normal = []
test_acc_list_normal = []
train_acc_list_decay = []
test_acc_list_decay = []

iter_per_epoch = max(train_size / batch_size, 1)
epoch_cnt = 0

# 학습 루프
for i in range(1000000000):
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]

    # 일반 네트워크 업데이트
    grads_normal = network_normal.gradient(x_batch, t_batch)
    optimizer_normal.update(network_normal.params, grads_normal)

    # 가중치 감쇠 네트워크 업데이트
    grads_decay = network_decay.gradient(x_batch, t_batch)
    optimizer_decay.update(network_decay.params, grads_decay)

    if i % iter_per_epoch == 0:
        train_acc_normal = network_normal.accuracy(x_train, t_train)
        test_acc_normal = network_normal.accuracy(x_test, t_test)
        train_acc_list_normal.append(train_acc_normal)
        test_acc_list_normal.append(test_acc_normal)

        train_acc_decay = network_decay.accuracy(x_train, t_train)
        test_acc_decay = network_decay.accuracy(x_test, t_test)
        train_acc_list_decay.append(train_acc_decay)
        test_acc_list_decay.append(test_acc_decay)

        print(f"epoch:{epoch_cnt}")
        print(f"Without weight decay - train acc:{train_acc_normal:.3f}, test acc:{test_acc_normal:.3f}")
        print(f"With weight decay    - train acc:{train_acc_decay:.3f}, test acc:{test_acc_decay:.3f}")
        print("---")

        epoch_cnt += 1
        if epoch_cnt >= max_epochs:
            break

# 그래프 그리기
plt.figure(figsize=(10, 6))
x = np.arange(max_epochs)

# 일반 네트워크
plt.plot(x, train_acc_list_normal, label='train (without weight decay)', 
         linestyle='--', marker='o', markevery=10, alpha=0.8)
plt.plot(x, test_acc_list_normal, label='test (without weight decay)', 
         linestyle='--', marker='s', markevery=10, alpha=0.8)

# 가중치 감쇠 네트워크
plt.plot(x, train_acc_list_decay, label=f'train (with weight decay λ={weight_decay_lambda})', 
         marker='o', markevery=10)
plt.plot(x, test_acc_list_decay, label=f'test (with weight decay λ={weight_decay_lambda})', 
         marker='s', markevery=10)

plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.ylim(0, 1.0)
plt.legend(loc='lower right')
plt.grid(True)
plt.title("Weight Decay Comparison")

plt.tight_layout()
plt.savefig('weight_decay_comparison.png')
plt.show()

# 최종 결과 출력
print("\nFinal Results:")
print("Without Weight Decay:")
print(f"Final train accuracy: {train_acc_list_normal[-1]:.3f}")
print(f"Final test accuracy: {test_acc_list_normal[-1]:.3f}")
print(f"Gap: {train_acc_list_normal[-1] - test_acc_list_normal[-1]:.3f}")
print("\nWith Weight Decay:")
print(f"Final train accuracy: {train_acc_list_decay[-1]:.3f}")
print(f"Final test accuracy: {test_acc_list_decay[-1]:.3f}")
print(f"Gap: {train_acc_list_decay[-1] - test_acc_list_decay[-1]:.3f}") 