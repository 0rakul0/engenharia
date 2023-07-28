from sklearn.feature_extraction.text import TfidfVectorizer
import locale
import logging
import random
import sys
from optparse import OptionParser
from time import time
import pickle
import matplotlib.pyplot as plt
import nltk
import numpy as np
from sklearn import metrics
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import NearestCentroid
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.utils.extmath import density

diretorio = "arquivos_ml//"

def testa(c, test_set,campo_treinamento,campo_classificacao,posicao_treinamento,posicao_classificacao):
    extensao =  str(c).split("(")[0]
    caminho_metodo = diretorio +  nome_arquivo_treinamento.split(".")[0] + "." + extensao

    with open(caminho_metodo, "wb") as file:
        print("Criando arquivo " + extensao)
        pickle.dump(c, file)

    previsoes = c.predict(test_set)

    if hasattr(c, 'decision_function'):
        hasDecision = True
        decision_function_matrix = c.decision_function(test_set)
    else:
        hasDecision = False

    for limite in range(0, 10):
        i = 0
        count_miss = 0
        count_correct = 0

        caminho_arquivo = diretorio + "piloto_ml{}.csv".format(limite)

        with open(caminho_arquivo , "w", encoding="latin-1", newline="\n") as arquivo:
            print(campo_treinamento, campo_classificacao+"_previsto", campo_classificacao+"_correto", "score", "resultado_previsao", file=arquivo,
                  sep=";")

            for value in values[int(tamanho * 0.7):]:
                # print(value[2], tree.predict(test_set[i]))
                previsao = previsoes[i]

                if limite == 0:

                    if value[posicao_classificacao].replace(".", "").replace("-", "").strip() == previsao:
                        count_correct += 1
                    else:
                        count_miss += 1

                    print(value[posicao_treinamento].strip(),
                          previsao,
                          value[posicao_classificacao].replace(".", "").replace("-", "").strip(),
                          str(get_higher_score(decision_function_matrix[i])).replace(".", ",") if hasDecision else 0,
                          str(value[posicao_classificacao].replace(".", "").replace("-", "").strip() == previsao),
                          file=arquivo, sep=";")

                else:
                    previsao = previsoes[i]
                    scr = decision_function_matrix[i] if hasDecision else 0
                    if get_higher_score(scr) > ((limite - 1) * 0.25):

                        if value[posicao_classificacao].replace(".", "").replace("-", "").strip() == previsao:
                            count_correct += 1
                        else:
                            count_miss += 1

                        print(value[posicao_treinamento].strip(),  # razao social
                              previsao,  # valor previsto
                              value[posicao_classificacao].replace(".", "").replace("-", "").strip(),  # valor correto
                              str(get_higher_score(decision_function_matrix[i])).replace(".", ",") if hasDecision else 0  ,
                              # score
                              str(value[posicao_classificacao].replace(".", "").replace("-", "").strip() ==
                                  previsao),  # previsão correta? v/f
                              file=arquivo, sep=";")

                i += 1

        global_score = count_correct / ((count_correct + count_miss) + 1)

        print((limite - 1) * 0.25, str(global_score).replace(".", ","),
              str((count_correct + count_miss) / (tamanho * 0.3)).replace(".", ","), count_correct, count_miss, sep=";")

def trim(s):
    """Trim string to fit on terminal (assuming 80-column display)"""
    return s if len(s) <= 80 else s[:77] + "..."

# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# parse commandline arguments
op = OptionParser()
op.add_option("--report",
              action="store_true", dest="print_report",
              help="Print a detailed classification report.")
op.add_option("--chi2_select",
              action="store", type="int", dest="select_chi2",
              help="Select some number of features using a chi-squared test")
op.add_option("--confusion_matrix",
              action="store_true", dest="print_cm",
              help="Print the confusion matrix.")
op.add_option("--top10",
              action="store_true", dest="print_top10",
              help="Print ten most discriminative terms per class"
                   " for every classifier.")
op.add_option("--all_categories",
              action="store_true", dest="all_categories",
              help="Whether to use all categories or not.")
op.add_option("--use_hashing",
              action="store_true",
              help="Use a hashing vectorizer.")
op.add_option("--n_features",
              action="store", type=int, default=2 ** 16,
              help="n_features when using the hashing vectorizer.")
op.add_option("--filtered",
              action="store_true",
              help="Remove newsgroup information that is easily overfit: "
                   "headers, signatures, and quoting.")

(opts, args) = op.parse_args(sys.argv[1:])

nome_arquivo_treinamento = input("Qual o nome do arquivo de treinamento?\n")
if not "." in nome_arquivo_treinamento:
    print("O arquivo não tem extensão, será setado como .csv")
    nome_arquivo_treinamento = nome_arquivo_treinamento + ".csv"

campo_treinamento = input("Qual o nome do campo de treinamento?\n")

campo_classificacao = input("Qual o nome do campo de classificacao?\n")

vetor_treinamento = nome_arquivo_treinamento.split(".")[0] + ".vetor"

posicao_treinamento = int(input("Qual a posicao do campo de treinamento?\n"))

posicao_classificacao = int(input("Qual a posicao do campo de classificacao?\n"))

# Benchmark classifiers
def benchmark(clf, X_train, y_train, X_test, y_test,campo_treinamento,campo_classificacao,posicao_treinamento,posicao_classificacao):
    print('_' * 80)
    print("Training: ")
    print(clf)
    t0 = time()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)

    t0 = time()
    pred = clf.predict(X_test)
    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)

    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)

    if hasattr(clf, 'coef_'):
        print("dimensionality: %d" % clf.coef_.shape[1])
        print("density: %f" % density(clf.coef_))

        if opts.print_top10:
            print("top 10 keywords:")
            top10 = np.argsort(clf.coef_[0])[-10:]
            print(top10)
        print()

    # if opts.print_report:
    #     print("classification report:")
    #     print(metrics.classification_report(y_test, pred,
    #                                         target_names=target_names))

    testa(clf, X_test,campo_treinamento,campo_classificacao,posicao_treinamento,posicao_classificacao)

    if opts.print_cm:
        print("confusion matrix:")
        print(metrics.confusion_matrix(y_test, pred))

    print()
    clf_descr = str(clf).split('(')[0]
    return clf_descr, score, train_time, test_time

def clean_values(values):
    for line in values:
        for v in line:
            v.replace(".", "").replace("-", "").strip()

    return values

def get_higher_score(values):
    max = float('-inf')
    for v in np.nditer(values):
        if v > max:
            max = v

    return max

locale.setlocale(locale.LC_ALL, "pt-BR")

caminho_arquivo = diretorio +  nome_arquivo_treinamento

# load train and test data
with open(caminho_arquivo, "r", encoding="utf-8") as csv_file:
    values = [x.strip().split(";") for x in csv_file]

tamanho = len(values)

values = clean_values(values)

# razoes_sociais = [x[1].replace(".", " ").replace("-", " ").strip() for x in values]

random.shuffle(values)

train_data = values[:int(tamanho*0.7)]
test_data = values[int(tamanho*0.7):]

print('data loaded')

y_train = [x[posicao_classificacao].replace(".", " ").replace("-", " ").strip() for x in train_data]
y_test = [x[posicao_classificacao].replace(".", " ").replace("-", " ").strip() for x in test_data]

print("Extracting features from the training data using a sparse vectorizer")

if opts.use_hashing:
    vectorizer = HashingVectorizer(stop_words=nltk.corpus.stopwords.words('portuguese'), alternate_sign=False,
                                       n_features=opts.n_features)
    X_train = vectorizer.transform([x[1].replace(".", " ").replace("-", " ").strip() for x in train_data])

else:
    vectorizer = TfidfVectorizer(max_df=0.5, use_idf=True, sublinear_tf=True,
                                     stop_words=nltk.corpus.stopwords.words('portuguese'))

    X_train = vectorizer.fit_transform([x[1].replace(".", " ").replace("-", " ").strip() for x in train_data])


print("Extracting features from the test data using the same vectorizer")

X_test = vectorizer.transform([x[1].replace(".", " ").replace("-", " ").strip() for x in test_data])


caminho_vetor = diretorio + vetor_treinamento
with open(caminho_vetor, "wb") as file:
    print("Criando arquivo Vectorizer")
    pickle.dump(vectorizer, file)

if opts.select_chi2:
    print("Extracting %d best features by a chi-squared test" % opts.select_chi2)
    ch2 = SelectKBest(chi2, k=opts.select_chi2)
    X_train1 = ch2.fit_transform(X_train, y_train)
    X_test1 = ch2.transform(X_test)

results = []
for clf, name in (
        (RidgeClassifier(tol=1e-2, solver="sag"), "Ridge Classifier"),
        (Perceptron(max_iter=50), "Perceptron"),
        (PassiveAggressiveClassifier(max_iter=50), "Passive-Aggressive"),
        # (KNeighborsClassifier(n_neighbors=10), "kNN"),
        # (RandomForestClassifier(n_estimators=100), "Random forest")
):
    print('=' * 80)
    print(name)
    results.append(benchmark(clf, X_train, y_train, X_test, y_test,campo_treinamento,campo_classificacao,posicao_treinamento,posicao_classificacao))

for penalty in ["l2", "l1"]:
    print('=' * 80)
    print("%s penalty" % penalty.upper())
    # Train Liblinear model
    results.append(benchmark(LinearSVC(penalty=penalty, dual=False,
                                       tol=1e-3), X_train, y_train, X_test, y_test,campo_treinamento,campo_classificacao,posicao_treinamento,posicao_classificacao))

    # Train SGD model
    results.append(benchmark(SGDClassifier(alpha=.0001, n_iter=50,
                                           penalty=penalty), X_train, y_train, X_test, y_test,campo_treinamento,campo_classificacao,posicao_treinamento,posicao_classificacao))


# Train SGD with Elastic Net penalty
print('=' * 80)
print("Elastic-Net penalty")
results.append(benchmark(SGDClassifier(alpha=.0001, n_iter=50,
                                       penalty="elasticnet"), X_train, y_train, X_test, y_test,campo_treinamento,campo_classificacao,posicao_treinamento,posicao_classificacao))


# Train NearestCentroid without threshold
print('=' * 80)
print("NearestCentroid (aka Rocchio classifier)")
results.append(benchmark(NearestCentroid(), X_train, y_train, X_test, y_test,campo_treinamento,campo_classificacao,posicao_treinamento,posicao_classificacao))

# Train sparse Naive Bayes classifiers
print('=' * 80)
print("Naive Bayes")
results.append(benchmark(MultinomialNB(alpha=.01), X_train, y_train, X_test, y_test,campo_treinamento,campo_classificacao,posicao_treinamento,posicao_classificacao))
results.append(benchmark(BernoulliNB(alpha=.01), X_train, y_train, X_test, y_test,campo_treinamento,campo_classificacao,posicao_treinamento,posicao_classificacao))

print('=' * 80)
print("LinearSVC with L1-based feature selection")
# The smaller C, the stronger the regularization.
# The more regularization, the more sparsity.
results.append(benchmark(Pipeline([
  ('feature_selection', SelectFromModel(LinearSVC(penalty="l1", dual=False,
                                                  tol=1e-3))),
  ('classification', LinearSVC(penalty="l2"))]), X_train, y_train, X_test, y_test,campo_treinamento,campo_classificacao,posicao_treinamento,posicao_classificacao))

# make some plots

indices = np.arange(len(results))

results = [[x[i] for x in results] for i in range(4)]

clf_names, score, training_time, test_time = results
training_time = np.array(training_time) / np.max(training_time)
test_time = np.array(test_time) / np.max(test_time)

plt.figure(figsize=(12, 8))
plt.title("Score")
plt.barh(indices, score, .2, label="score", color='navy')
plt.barh(indices + .3, training_time, .2, label="training time",
         color='c')
plt.barh(indices + .6, test_time, .2, label="test time", color='darkorange')
plt.yticks(())
plt.legend(loc='best')
plt.subplots_adjust(left=.25)
plt.subplots_adjust(top=.95)
plt.subplots_adjust(bottom=.05)

for i, c in zip(indices, clf_names):
    plt.text(-.3, i, c)

plt.show()



