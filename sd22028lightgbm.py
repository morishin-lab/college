#%%
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_recall_fscore_support,
    roc_auc_score,
)
import lightgbm as lgb


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
def calculate_cell_features(x):
    cell_features = []
    # 縦・横・斜のパターンの数え上げ
    CELL_FEATURE = {
        "B": (1, 0, 0, 0, 0),
        "W": (0, 1, 0, 0, 0),
        "b": (0, 0, 1, 0, 0),
        "w": (0, 0, 0, 1, 0),
        "s": (0, 0, 0, 0, 1)
    }
    for cell in x[1]:
        cell_features += CELL_FEATURE[cell]
    assert len(cell_features) == 125
    assert sum(cell_features) == 25
    return cell_features


def calculate_main_direction_fetures(x):
    B_direction_features = [0] * 4
    W_direction_features = [0] * 4
    for idx in range(25):
        if x[1][idx] == "B":
            if idx >= 5:  #上
                if x[1][idx - 5] == "s":
                    B_direction_features[0] = 1
            if idx % 5 != 4:  #右
                if x[1][idx + 1] == "s":
                    B_direction_features[1] = 1
            if idx <= 19:  #下
                if x[1][idx + 5] == "s":
                    B_direction_features[2] = 1
            if idx % 5 != 0:  #左
                if x[1][idx - 1] == "s":
                    B_direction_features[3] = 1
        if x[1][idx] == "W":
            if idx >= 5:  #上
                if x[1][idx - 5] == "s":
                    W_direction_features[0] = 1
            if idx % 5 != 4:  #右
                if x[1][idx + 1] == "s":
                    W_direction_features[1] = 1
            if idx <= 19:  #下
                if x[1][idx + 5] == "s":
                    W_direction_features[2] = 1
            if idx % 5 != 0:  #左
                if x[1][idx - 1] == "s":
                    W_direction_features[3] = 1
    main_direction_features = []
    main_direction_features += B_direction_features
    main_direction_features += W_direction_features
    assert len(main_direction_features) == 8
    assert sum(main_direction_features) <= 8
    return main_direction_features


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
    features = calculate_cell_features(x)
    features += calculate_main_direction_fetures(x)
    features += calculate_turn_features(x)
    assert len(features) == 125 + 2 + 8
    assert sum(features) <= 25 + 1 + 8
    return features


#%%
# データの特徴ベクトルへの変換
def convert_to_feature_vector(X_org):
    X = []
    for x in X_org:
        X.append(calculate_features(x))
    return X


#%%
def convert_to_0_1(y_org):
    Y = []
    for y in y_org:
        if y == "B":
            Y.append(1)
        else:
            Y.append(0)
    return Y


#%%
# データの学習
def train(X_train, y_train):
    assert len(X_train) == len(y_train)
    model = lgb.LGBMClassifier()
    model.fit(X_train, y_train)
    return model


# 様々な評価指標
def evaluate_scores(model, X, y, pos_label=1, labels=[1, 0]):
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
    X_org_train, y_org_train = read_slipe_data("slipe.train.csv")
    X_org_devel, y_org_devel = read_slipe_data("slipe.devel.csv")

    # 学習
    X_train = convert_to_feature_vector(X_org_train)
    y_train = convert_to_0_1(y_org_train)
    X_devel = convert_to_feature_vector(X_org_devel)
    y_devel = convert_to_0_1(y_org_devel)

    model = train(X_train, y_train)

    # validationでの評価
    cmatrix, accuracy, p, r, f, auc = evaluate_scores(model, X_devel, y_devel)
    print(f"confusion matrix = \n{cmatrix}")
    print(f"accuracy = {accuracy}")
    print(f"(precision, recall, f-score) = ({p:.3f}, {r:.3f}, {f:.3f})")
    print(f"AUC-ROC = {auc:.3f}")
    output_test_predictions(model)
