from config import settings
from MusicReco.Manager import Manager
from MusicReco.models.db import Audio, Plugin
import MusicReco.models.db
from utils import load_collection

from sklearn.learning_curve import validation_curve
from sklearn.svm import SVC
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import SGDClassifier
from sklearn.learning_curve import learning_curve
from sklearn.linear_model import LogisticRegression
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and traning learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : integer, cross-validation generator, optional
        If an integer is passed, it is the number of folds (defaults to 3).
        Specific cross-validation objects can be passed, see
        sklearn.cross_validation module for the list of possible objects
    """

    plt.figure()
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=5, n_jobs=1, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.xlabel("Training examples")
    plt.ylabel("Score")
    plt.legend(loc="best")
    plt.grid("on")
    if ylim:
        plt.ylim(ylim)
    plt.title(title)
    #plt.show()

def plot_validation_curve(estimator, title, X , y , ylim = None, cv= None, param_name=None, param_range=None):

    plt.figure()
    train_scores, test_scores = validation_curve(estimator, X, y, param_name=param_name, param_range=param_range, cv=cv, scoring="accuracy", n_jobs=2)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.semilogx(param_range, train_scores_mean, label="Training score", color="r")
    plt.fill_between(param_range, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.2, color="r")
    plt.semilogx(param_range, test_scores_mean, label="Cross-validation score", color="g")
    plt.fill_between(param_range, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.2, color="g")

    plt.title(title)
    plt.xlabel("C")
    plt.ylabel("Score")
    plt.ylim(ylim)
    plt.legend(loc="best")
    plt.grid("on")


def plots(manager):
    from sklearn.neural_network import MLPClassifier
    df = manager.mllib.getAllDataFrame()

    manager.mllib.train(df,plugin='AF')
    X = manager.mllib.X_train.iloc[:,:-1]
    y = manager.mllib.X_train.iloc[:,-1]

    clf = SVC(gamma=0.001, C= 100, kernel='rbf')
    #clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-9,activation='tanh', tol = 1e-6,
    #    hidden_layer_sizes=(10, 3), random_state=1)
    p = Pipeline([("Scaler", StandardScaler()), ("svm", clf)])
    plot_learning_curve(p, "Learning Curve SVC", X, y, ylim=(0.0, 1.01), train_sizes=np.linspace(0.1, 1.0, 5))
    #print(p.get_params().keys())

    #param_range = np.linspace(10,500,10)
    #param_range=[(3,3),(5,3),(10,3),(15,3),(25,3), (40,3)]
    #plot_validation_curve(p, "Validation Curve Logistic", X, y, ylim=(0.0, 1.01), cv=10, param_name="svm__hidden_layer_sizes", param_range=param_range)
    plt.savefig("learning.png")
    #plt.show()


def main():
    # import settings
    tags = settings['tags']
    plugins = settings['plugins']
    train_dir = settings['training_dataset']
    test_size = float(settings['test_size'])

    model = MusicReco.models.db
    manager = Manager(model)


    # initialize_storage
    manager.initialize_storage()

    # load collection

    #NOTE: Make sure you load collection only one time.
#     manager.load_collection(tags, train_dir, test_size)
#     manager.load_plugins(plugins)

    # Create feature vector of songs
    manager.use_plugin(plugin='AF')

    manager.use_ml(ml = "LINEAR")

    #manager.init_vectors(limit = 1000)

    # learning algorithms
    manager.train()

    predict, test =  manager.test()

    manager.accuracy_score(predict, test)

    #manager.plot()
    #plots(manager)



if __name__ == '__main__':
    main();
