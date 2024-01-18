### 4.1.1 Classification
One-Hot encoding is a vector with as many components as we have categories. The component corresponding to a particular instance’s category is set to 1 and all other components are set to 0. In our case, a label $y$ would be a three-dimensional vector, with (1,0,0) corresponding to “cat”, (0,1,0) to “chicken”, and (0,0,1) to “dog”: \
$y \in{\{(1,0,0),(0,1,0),(0,0,1)\}}$

#### 4.1.1.1 Linear Model
为了估计所有可能类别的条件概率，我们需要一个有多个输出的模型，每个类别对应一个输出。 为了解决线性模型的分类问题，我们需要和输出一样多的仿射函数（affine function）。 每个输出对应于它自己的仿射函数。我们的例子中，我们有 4 个特征 和 3 个可能的输出类别，则一共需要15个标量：12个表示权重，3个表示偏移量：\
$o_1 = x_1w_{11} + x_2w_{12} + x_3w_{13}+x_4w_{14} + b_1$\
$o_2 = x_2w_{21} + x_2w_{22} + x_3w_{23}+x_4w_{14} + b_1$\
$o_3 = x_3w_{31} + x_2w_{32} + x_3w_{33}+x_4w_{14} + b_1$\
其向量形式为
$o=Wx+b$


#### 4.1.1.2 The Softmax 
Assuming a suitable loss function, we could try, directly, to minimize the difference between o and the labels y . While it turns out that treating classification as a vector-valued regression problem works surprisingly well, it is nonetheless unsatisfactory in the following ways:
* There is no guarantee that the outputs $o_i$ sum up to  in the way we expect probabilities to behave.
* There is no guarantee that the outputs $o_i$ are even nonnegative, even if their outputs sum up to 1, or that they do not exceed 1.

There are many ways we might accomplish this goal. For instance, we could assume that the outputs  are corrupted versions of $y$, where corruption occurs by means of adding noise $\epsilon$ drawn from a normal distribution. 

In other words, $y=o+\epsilon$, where $\epsilon_i$ ~ $N(0,\sigma^2 )$. This is the so-called probit model, first introduced by Fechner (1860). While appealing, it does not work quite as well nor lead to a particularly nice optimization problem, when compared to the softmax.

Another way to accomplish this goal (and to ensure nonnegativity) is to use an exponential function. This does indeed satisfy the requirement that the conditional class probability increases with increasing $o_i$, it is monotonic, and all probabilities are nonnegative. We can then transform these values so that they add up to 1 by dividing each by their sum. This process is called normalization. Putting these two pieces together gives us the softmax function: \
$y=softmax(o)$ where $y_j=\frac{e^{O_j}}{\sum_{e^{o_k}}}$

#### 4.1.1.3 Vectorization
$O=XW + b$\
$\hat{Y} = softmax(O)$



softmax回归(softmax regression)是一种用于分类问题的线性回归模型。它在分类问题上的效果比普通线性回归好,但模型结构较为简单。是分类问题的基础算法之一。
* 采用线性模型输出多个类别的原始分数。
* 使用softmax函数将原始分数转换为每个类别的概率。
* 损失函数采用交叉熵直接优化最终类别概率。


### 4.1.2 Loss Function
在深度学习中，全连接层无处不在。 然而，顾名思义，全连接层是“完全”连接的，可能有很多可学习的参数。具体来说，对于任何具有 d 个输入和 q 个输出的全连接层，参数开销为 $O(dq)$，这个数字在实践中可能高得令人望而却步。 幸运的是，将 q 个输入转换为个输出的成本可以减少到 $O(\frac{dq}{n})$，其方法是将 q 个输出分成 n 组，然后每组进行连接。这样可以将参数开销降低到 $O(\frac{dq}{n})$ 其中超参数可以由我们灵活指定，以在实际应用中平衡参数节约和模型有效性 



