# 🧠 Neural Network Training Visualization

This directory contains implementations and visualizations of neural network training processes, focusing on a two-layer neural network trained on the MNIST dataset.

## 🖼️ Gallery

| Preview | Description |
|---------|-------------|
| <img src="https://github.com/user-attachments/assets/c0f5d3cf-fdcf-4271-9c35-3ada79e27cdb" width="200"/> | **Training vs Test Accuracy** <br> Visualization of the learning process showing: <br> • Training accuracy progression <br> • Test accuracy comparison <br> • Clear convergence pattern |
| <img src="https://github.com/user-attachments/assets/786d6398-b3b3-498a-94dc-59fe63233931" width="200"/> | **Two-Layer Network Architecture** <br> Visualization of the network structure: <br> • Input layer (784 neurons) <br> • Hidden layer (50 neurons) <br> • Output layer (10 neurons) |
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

## 📁 Directory Structure
```
20250205/
├── README.md
├── train_neuralnet.ipynb
├── two_layer_net.py
└── images/
    ├── training_accuracy.png
    └── network_architecture.png
```

## 🎨 Visualization Features
- Dark theme plots for better contrast
- Clear epoch vs accuracy visualization
- Training/test accuracy comparison
- Distinct line styles for different metrics

## 📊 Results
- Final Training Accuracy: ~94.7%
- Final Test Accuracy: ~94.6%
- Convergence achieved within 17 epochs

## 🔍 Key Learning Points
1. Implementation of backpropagation
2. Batch processing for efficient training
3. Comparison of training vs test accuracy
4. Visualization of learning progress

---
*Part of the MS AI School deep learning curriculum* 