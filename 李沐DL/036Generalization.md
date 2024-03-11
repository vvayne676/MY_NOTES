## 3.6 Generalization
As machine learning scientists, our goal is to discover patterns. But how can we be sure that we have truly discovered a general pattern and not simply memorized our data. This problem—how to discover patterns that generalize—is the fundamental problem of machine learning, and arguably of all of statistics.

The phenomenon of fitting closer to our training data than to the underlying distribution is called overfitting, and techniques for combatting overfitting are often called regularization methods.

### 3.6.1 Generalization Error
In the standard supervised learning setting, we assume that the training data and the test data are drawn independently from identical distributions. This is commonly called the IID assumption
IID assumption (独立同分布-Independent and Identically Distributed)

#### 3.6.1.1 Model Complexity
In classical theory, when we have simple models and abundant data, the training and generalization errors tend to be close. Deep neural networks turn out to be just such models: while they generalize well in practice, they are too powerful to allow us to conclude much on the basis of training error alone. In these cases we must rely more heavily on our holdout data to certify generalization after the fact. Error on the holdout data, i.e., validation set, is called the validation error.
这个section 主要就是聊了 Generalization, model error, generalization error, validation error. 

### 3.6.2 Underfitting or Overfitting
. If the model is unable to reduce the training error, that could mean that our model is too simple (i.e., insufficiently expressive) to capture the pattern that we are trying to model. Moreover, since the generalization gap ($R_{emp}-R$) between our training and generalization errors is small, we have reason to believe that we could get away with a more complex model. This phenomenon is known as underfitting. We want to watch out for the cases when our training error is significantly lower than our validation error, indicating severe overfitting. Fixing our model, the fewer samples we have in the training dataset, the more likely (and more severely) we are to encounter overfitting.

### 3.6.3 Model Selection
原始数据:
1. training set:
    1. training set
    2. validation set
2. test set

model selection可以用 cross-validation: k-fold cross-validation 首先将数据集随机分成k个大小相等（或几乎相等）的子集（称为“折”）。然后，模型进行k次训练和验证，每次选择不同的折作为验证集，其余的k-1个折作为训练集。最后，模型性能的估计是这k次验证结果的平均值