#%%
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_recall_fscore_support,
    roc_auc_score,
)

LogisticRegression(max_iter=1000)


#%%
# データの読み込み
def read_slipe_data(file_name):
    X, y = [], []
    with open(file_name) as data:
        for line in data:
            attrs = line.strip().split(",")
            y1, x1 = attrs[0], attrs[1:]
            X.append(x1)
            y.append(y1)
    return X, y


#%%
# ここにそれぞれの特徴を計算する関数を追加する
def add_pattern_feature(pattern_features, dic, pattern):
    pattern_features[dic[pattern]] += 1
    pattern_features[dic[pattern[::-1]]] += 1


def calculate_pattern_features(x):
    pattern_features = [0] * 3125
    d = {}
    IDX = {"B": 4, "W": 3, "b": 2, "w": 1, "s": 0}
    for i in "BWbws":
        for j in "BWbws":
            for k in "BWbws":
                for l in "BWbws":
                    for m in "BWbws":
                        d[i + j + k + l + m] = IDX[i] * 625 + IDX[
                            j] * 125 + IDX[k] * 25 + IDX[l] * 5 + IDX[m]
    for i in range(5):
        add_pattern_feature(pattern_features, d, x[1][i] + x[1][i + 5] +
                            x[1][i + 10] + x[1][i + 15] + x[1][i + 20])  # 列
        add_pattern_feature(pattern_features, d,
                            x[1][i * 5] + x[1][i * 5 + 1] + x[1][i * 5 + 2] +
                            x[1][i * 5 + 3] + x[1][i * 5 + 4])  # 行
    assert len(pattern_features) == 3125
    assert sum(pattern_features) == 20
    return pattern_features


def calculate_turn_features(x):
    turn_features = [0, 0]
    if x[0] == "B":
        turn_features[0] = 1
    elif x[0] == "W":
        turn_features[1] = 1
    assert len(turn_features) == 2
    assert sum(turn_features) == 1
    return turn_features


# 特徴ベクトルの計算
def calculate_features(x):
    features = calculate_pattern_features(x)
    features += calculate_turn_features(x)
    assert len(features) == 3125 + 2
    assert sum(features) <= 20 + 1
    return features


#%%
# データの特徴ベクトルへの変換
def convert_to_feature_vector(X_org):
    X = []
    for x in X_org:
        X.append(calculate_features(x))
    return X


#%%
# データの学習
def train(X_train, y_train):
    assert len(X_train) == len(y_train)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model


# 様々な評価指標
def evaluate_scores(model, X, y, pos_label="B", labels=["B", "W"]):
    y_hat = model.predict(X)
    cmatrix = confusion_matrix(y_true=y, y_pred=y_hat, labels=labels)
    accuracy = accuracy_score(y_true=y, y_pred=y_hat)
    p, r, f, _ = precision_recall_fscore_support(y_true=y,
                                                 y_pred=y_hat,
                                                 pos_label=pos_label,
                                                 average="binary")
    y_hat_proba = model.predict_proba(X)
    roc = roc_auc_score(y, y_hat_proba[:, 1])
    return cmatrix, accuracy, p, r, f, roc


#%%
def output_test_predictions(model):
    X_org_test, y_test = read_slipe_data("slipe.test.csv")
    X_test = convert_to_feature_vector(X_org_test)
    y_predictions = model.predict(X_test)
    W_B_dictionary = {0: "W", 1: "B"}
    name_handle = open("sd22028.txt", "w")
    for i in y_predictions:
        name_handle.write(f'{W_B_dictionary[i]}\n')
    name_handle.close()


#%%
if __name__ == '__main__':
    # データの読み込み
    X_org_train, y_train = read_slipe_data("slipe.train.csv")
    X_org_devel, y_devel = read_slipe_data("slipe.devel.csv")

    # 学習
    X_train = convert_to_feature_vector(X_org_train)
    X_devel = convert_to_feature_vector(X_org_devel)

    model = train(X_train, y_train)

    # validationでの評価
    cmatrix, accuracy, p, r, f, auc = evaluate_scores(model, X_devel, y_devel)
    print(f"confusion matrix = \n{cmatrix}")
    print(f"accuracy = {accuracy}")
    print(f"(precision, recall, f-score) = ({p:.3f}, {r:.3f}, {f:.3f})")
    print(f"AUC-ROC = {auc:.3f}")
    output_test_predictions(model)
