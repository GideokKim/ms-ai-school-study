# 🧠 Neural Network Training Visualization

This directory contains implementations and visualizations of neural network training processes, focusing on a two-layer neural network trained on the MNIST dataset.

## 🖼️ Gallery

| Preview | Description |
|---------|-------------|
| <img src="https://github.com/user-attachments/assets/c0f5d3cf-fdcf-4271-9c35-3ada79e27cdb" width="400"/> | **Training vs Test Accuracy** <br> Visualization of the learning process showing: <br> • Training accuracy progression <br> • Test accuracy comparison <br> • Clear convergence pattern |
| <img src="https://github.com/user-attachments/assets/786d6398-b3b3-498a-94dc-59fe63233931" width="400"/> | **Two-Layer Network Architecture** <br> Visualization of the network structure: <br> • Input layer (784 neurons) <br> • Hidden layer (50 neurons) <br> • Output layer (10 neurons) |
| <img src="https://github.com/user-attachments/assets/6e6c50bb-c2d3-4963-a40e-311f2ce64122" width="400"/> | **Gradient Descent Visualization** <br> Interactive visualization of optimization: <br> • 3D surface plot with descent path <br> • Contour plot with convergence <br> • Start point to minimum trajectory |
| <img src="https://github.com/user-attachments/assets/8a028acd-cc9c-4261-9212-163018daf80c" width="400"/> | **Stochastic Gradient Descent** <br> Visualization of SGD optimization: <br> • Random sampling for gradients <br> • Noisy descent trajectory <br> • Exploration vs exploitation |
| <img src="https://github.com/user-attachments/assets/d39171d2-bcf6-4cea-b2d6-6f2f9b949d82" width="400"/> | **Momentum Gradient Descent** <br> Visualization of momentum-based optimization: <br> • Momentum acceleration effect <br> • Smoother convergence path <br> • Oscillation near minimum |
| <img src="https://github.com/user-attachments/assets/feba54f8-b84f-4475-b5c7-114ba1e6d9fa" width="400"/> | **AdaGrad Gradient Descent** <br> Visualization of AdaGrad optimization: <br> • Adaptive learning rates <br> • Parameter-specific updates <br> • Efficient early convergence |
| 🎯 Coming soon... | Next visualization here! |

## 🛠️ Implementation Details

### Network Architecture
- Input Size: 784 (28x28 MNIST images)
- Hidden Layer: 50 neurons
- Output Layer: 10 neurons (digit classes)
- Activation Functions: Sigmoid (hidden), Softmax (output)

### Training Parameters
```python
iters_num = 10000    # Total iterations
batch_size = 100     # Mini-batch size
learning_rate = 0.1  # Learning rate
```

### Gradient Descent Parameters
```python
lr = 0.4             # Learning rate for GD
iterations = 30      # Number of steps
function = "1/10 * x^2 + y^2"  # Target function
```

### Stochastic Gradient Descent Parameters
```python
lr = 0.4             # Learning rate for SGD
batch_size = 10      # Mini-batch size
iterations = 30      # Number of steps
function = "1/10 * x^2 + y^2"  # Target function
```

### Momentum Gradient Descent Parameters
```python
lr = 0.04            # Learning rate for Momentum
momentum = 0.9       # Momentum coefficient
iterations = 30      # Number of steps
function = "1/10 * x^2 + y^2"  # Target function
```

### AdaGrad Gradient Descent Parameters
```python
lr = 1             # Initial learning rate for AdaGrad
iterations = 30      # Number of steps
function = "1/10 * x^2 + y^2"  # Target function
```

## 📁 Directory Structure
```
20250205/
├── README.md
├── train_neuralnet.ipynb
├── gradient_descent_2d.ipynb
├── stochastic_gradient_descent_2d.ipynb
├── momentum_gradient_descent_2d.ipynb
├── adagrad_gradient_descent_2d.ipynb
├── two_layer_net.py
├── optimizer.py
```

## 🎨 Visualization Features
- Dark theme plots for better contrast
- Clear epoch vs accuracy visualization
- Training/test accuracy comparison
- Distinct line styles for different metrics
- Interactive 3D gradient descent visualization
- SGD vs standard gradient descent comparison
- Mini-batch gradient computation
- Stochastic exploration visualization
- Momentum-based optimization visualization
- Acceleration and deceleration effects
- Oscillatory behavior near convergence
- AdaGrad adaptive learning rate visualization
- Parameter-specific learning rate effects
- Automatic learning rate adjustment

## 📊 Results
- Final Training Accuracy: ~94.7%
- Final Test Accuracy: ~94.6%
- Convergence achieved within 17 epochs
- Gradient Descent converges to (0, 0) minimum
- Momentum GD shows smoother convergence
- Final position: (-0.53, 0.00)
- Minimum value: 0.002831
- AdaGrad shows efficient early-stage optimization
- Adaptive learning rates prevent overshooting
- Final position: (-0.01, 0.00)
- Minimum value: 0.000001

## 🔍 Key Learning Points
1. Implementation of backpropagation
2. Batch processing for efficient training
3. Comparison of training vs test accuracy
4. Visualization of learning progress
5. Understanding optimization landscapes
6. Gradient descent behavior in 2D/3D
7. Stochastic vs deterministic optimization
8. Mini-batch gradient computation
9. Exploration-exploitation trade-off
10. Momentum's role in optimization
11. Acceleration in gradient descent
12. Handling oscillation in optimization
13. Adaptive learning rate optimization
14. Parameter-specific learning rates
15. Handling different scale features

---
*Part of the MS AI School deep learning curriculum* 