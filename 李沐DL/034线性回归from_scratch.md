## 3.4 Linear Regression Implementation from Scratch
In this section, we will implement the entire method from scratch, including 
1. the model; 
2. the loss function; 
3. a minibatch stochastic gradient descent optimizer;
4. the training function that stitches all of these pieces together. 
5. we will run our synthetic data generator from Section 3.3 and apply our model on the resulting dataset
```python
%matplotlib inline
import torch
from d2l import torch as d2l
```


### 3.4.1 Defining the Model
In the following we initialize weights by drawing random numbers from a normal distribution with mean 0 and a standard deviation of 0.01. The magic number 0.01 often works well in practice, but you can specify a different value through the argument sigma. Moreover we set the bias to 0. 
```python
class LinearRegressionScratch(d2l.Module):  #@save
    """The linear regression model implemented from scratch.
    Args:
        num_inputs: 这是输入特征的数量。对于线性回归模型，输入特征的数量等于模型权重（w）的行数。

        lr: 这是学习率（learning rate），用于控制模型在训练过程中权重更新的步长。它影响着模型在每次参数更新时的幅度
        
        sigma=0.01: 这是用于初始化权重（w）的标准差。在这里，通过 torch.normal(0, sigma, (num_inputs, 1), requires_grad=True) 来随机生成服从均值为0、标准差为 sigma 的正态分布的张量作为初始权重 w，其中 num_inputs 是输入特征的数量，(num_inputs, 1) 表示创建一个形状为 (num_inputs, 1) 的张量作为权重矩阵。设置 requires_grad=True 表示这个张量需要梯度，因此可以在训练过程中进行优化。
        
        self.b: 这是偏置（bias）项，初始化为零。在线性回归模型中，除了权重 w 外，还有一个偏置项 b，表示模型预测中的偏移量。它也是一个需要梯度的张量，用于模型训练过程中更新

    """

    def __init__(self, num_inputs, lr, sigma=0.01):
        super().__init__()
        self.save_hyperparameters()
        self.w = torch.normal(0, sigma, (num_inputs, 1), requires_grad=True)
        self.b = torch.zeros(1, requires_grad=True)
```
Next we must define our model, relating its input and parameters to its output. Using the same notation as (3.1.4) for our linear model we simply take the matrix–vector product of the input features X and the model weights w, and add the offset b to each example. The product Xw is a vector and b is a scalar. Because of the broadcasting mechanism (see Section 2.1.4), when we add a vector and a scalar, the scalar is added to each component of the vector. The resulting forward method is registered in the LinearRegressionScratch class via add_to_class (introduced in Section 3.2.1).
```python
@d2l.add_to_class(LinearRegressionScratch)  #@save
def forward(self, X):
    '''forward 函数定义了线性回归模型的前向传播（forward propagation）过程。在深度学习中，前向传播是指输入数据通过模型，经过一系列的线性和非线性运算后得到模型的输出结果。
    Args:
        X: 这是输入数据，通常是一个张量（Tensor），其中包含了一个批次的样本数据。这里假设输入的数据形状为 (batch_size, num_features)，其中 batch_size 是批次大小，num_features 是特征数量。

        torch.matmul(X, self.w) + self.b: 这是前向传播的主要计算过程。它对输入数据 X 和模型的权重 self.w 进行矩阵乘法操作（torch.matmul），然后加上模型的偏置 self.b，得到线性回归模型的预测结果。这个过程可以表示为 X⋅w+b，其中 X⋅w 表示矩阵乘法运算

        在深度学习中，forward 方法通常是必须的，它定义了模型的计算流程。在训练模型时，数据会通过这个前向传播过程得到模型的预测结果，然后计算预测结果与实际标签之间的误差，并通过反向传播（backward propagation）来更新模型的参数，以减小误差，提高模型的性能。
    '''
    return torch.matmul(X, self.w) + self.b
```
### 3.4.2 Defining the Loss Function
```python
@d2l.add_to_class(LinearRegressionScratch)  #@save
def loss(self, y_hat, y):
    '''
    方差平均数
    '''
    l = (y_hat - y) ** 2 / 2
    return l.mean()
```

### 3.4.3 Defining the Optimization Algorithm
Our goal here is to illustrate how to train more general neural networks, and that requires that we teach you how to use minibatch SGD. Hence we will take this opportunity to introduce your first working example of SGD. At each step, using a minibatch randomly drawn from our dataset, we estimate the gradient of the loss with respect to the parameters. Next, we update the parameters in the direction that may reduce the loss.

The following code applies the update, given a set of parameters, a learning rate lr. Since our loss is computed as an average over the minibatch, we do not need to adjust the learning rate against the batch size. In later chapters we will investigate how learning rates should be adjusted for very large minibatches as they arise in distributed large-scale learning. For now, we can ignore this dependency.

We define our SGD class, a subclass of d2l.HyperParameters (introduced in Section 3.2.1), to have a similar API as the built-in SGD optimizer. We update the parameters in the step method. The zero_grad method sets all gradients to 0, which must be run before a backpropagation step.
```python
# Stochastic Gradient Descent
class SGD(d2l.HyperParameters):  #@save
    """Minibatch stochastic gradient descent."""
    def __init__(self, params, lr):
        self.save_hyperparameters()

    def step(self):
    """这个方法执行了一次优化步骤，应用了梯度下降算法。对于每个模型参数 param，通过 param -= self.lr * param.grad 对参数进行更新

    param.grad 表示参数 param 的梯度，self.lr 是学习率。这里的更新方式是简化版的梯度下降，即按照梯度的反方向更新参数值，乘以学习率控制步长
    """
        for param in self.params:
            param = param - self.lr * param.grad

    def zero_grad(self):
    '''
    zero_grad(self): 这个方法用于将模型参数的梯度清零。对于每个模型参数 param，如果它的梯度不为 None，则通过 param.grad.zero_() 将其梯度置零。这个操作通常在每次计算完梯度后调用，以准备开始下一轮的梯度计算。

    在许多优化算法中，比如随机梯度下降（SGD）或其变种，梯度是根据当前的损失函数计算得到的。由于通常是通过迭代的方式计算梯度并进行参数更新，如果不在每次迭代后将梯度清零，梯度会不断累积，导致错误的梯度信息被保留。这可能会使模型的优化过程变得不稳定，甚至影响到模型的收敛性。

    在深度学习中，通常会进行多次迭代优化模型参数。梯度清零可以确保每次迭代开始时，都从零开始累积新的梯度信息，而不会受到上一次迭代梯度的影响。这有助于确保每次梯度更新都是基于当前批次数据的计算结果，而不受之前迭代的影响。

    在某些深度学习框架中（比如PyTorch、TensorFlow等），计算梯度是通过构建计算图来实现的。如果不清零梯度，梯度信息将保留在计算图中，并随着后续的计算而持续存在，占用内存资源。清零操作有助于释放这些内存空间。
    '''
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()

```

We next define the configure_optimizers method, which returns an instance of the SGD class.
```python
@d2l.add_to_class(LinearRegressionScratch)  #@save
def configure_optimizers(self):
    return SGD([self.w, self.b], self.lr)
```

### 3.4.4 Training
Now that we have all of the parts in place (parameters, loss function, model, and optimizer), we are ready to implement the main training loop. It is crucial that you understand this code fully since you will employ similar training loops for every other deep learning model covered in this book. In each epoch, we iterate through the entire training dataset, passing once through every example (assuming that the number of examples is divisible by the batch size). In each iteration, we grab a minibatch of training examples, and compute its loss through the model’s training_step method. Then we compute the gradients with respect to each parameter. Finally, we will call the optimization algorithm to update the model parameters. 
1. Initialize parameters (w,b)
2. Repeat until done
    1. Compute gradient
    2. Update parameters
```python 
@d2l.add_to_class(d2l.Trainer)  #@save
def prepare_batch(self, batch):
    '''这个方法对训练数据的批次进行预处理或准备工作。在这个示例中，prepare_batch 方法接收一个数据批次 batch 作为输入，并直接返回这个批次，即不做任何额外的处理或转换。通常可以在这个方法中进行数据标准化、扩增、格式转换等操作，以准备好输入模型的数据。
    '''
    return batch

@d2l.add_to_class(d2l.Trainer)  #@save
def fit_epoch(self):
    '''这个方法执行了模型的一个训练 epoch。在训练过程中，它通过迭代训练数据集来更新模型的参数
    
    self.model.train()：将模型设置为训练模式，以便启用训练中需要的功能，比如梯度计算。

    '''
    # Puts the model in training mode.
    self.model.train()
    for batch in self.train_dataloader:
        loss = self.model.training_step(self.prepare_batch(batch))
        # 清空优化器中保存的梯度信息
        self.optim.zero_grad()
        # comment out below because below context manager will disable gradient computation temporarily 
        # with torch.no_grad():
        # 根据损失计算梯度
        loss.backward()
        if self.gradient_clip_val > 0:  # To be discussed later
            # If gradient clipping is enabled, clips gradients to prevent their value from exceeding a threshold.
            self.clip_gradients(self.gradient_clip_val, self.model)
        # 根据计算出的梯度更新模型参数
        self.optim.step()
        self.train_batch_idx = self.train_batch_idx + 1
    if self.val_dataloader is None:
        return
    # Puts the model in evaluation mode.
    self.model.eval()
    # 对验证数据集进行验证，并执行相应的验证步骤
    for batch in self.val_dataloader:
        # Context manager to disable gradient calculation
        with torch.no_grad():
            self.model.validation_step(self.prepare_batch(batch))
        self.val_batch_idx = self.val_batch_idx + 1
```
1. set model to training mode `self.model.train()`
2. for loop on minibatch training data to 
    1. calculate loss
    2. zero gradient
    3. loss backward
    4. step update parameter
    5. batch idx +1
3. set model to eval mode
4. for loop on minibatch validation data 
    1. validation stage do not need calculate gradient so we have torch.no_grad()
    2. validation_step
    3. validation batch idx + 1
### 3.4.5
Start to whole process
```python
# model is model like w1x1 + w2x2 = y, w1 and w2 are the fields belong to model
model = LinearRegressionScratch(2, lr=0.03)
# data is the value of x like x1 x2
data = d2l.SyntheticRegressionData(w=torch.tensor([2, -3.4]), b=4.2)
trainer = d2l.Trainer(max_epochs=3)
trainer.fit(model, data)
```


RuntimeError: a leaf Variable that requires grad is being used in an in-place operation.???

在 PyTorch 中，叶子变量是直接创建的张量，它们不是任何操作的结果，比如通过 torch.tensor 或者 Variable 创建的张量，并且设置了 requires_grad=True。原地操作是指直接修改这个变量而不是创建一个新的变量，比如使用 += 或者 *= 这样的操作。

当你在一个需要梯度的变量上执行原地操作时，PyTorch 无法正确地追踪梯度，因为原地修改意味着变量的值被覆盖了，这会破坏计算图并导致无法回溯。

为了解决这个问题，你需要避免在需要梯度的变量上执行原地操作。如果你需要修改一个变量，你应该创建一个新的变量来存储修改后的值。例如，如果你有一个原地操作 x += y，你应该替换为 x = x + y。

Check forward/backward/SGD make sure you have no in-place operation.