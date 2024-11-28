import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import sys
import io

# 標準出力のエンコーディングを設定(出力文字化けのため)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# 平均の計算
def calculate_mean(data):
    return np.sum(data, axis=0) / data.shape[0]

# 標準偏差の計算
def calculate_std(data, mean):
    variance = np.sum((data - mean) ** 2, axis=0) / data.shape[0]
    return np.sqrt(variance)

# データの標準化
def standardize_data(data):
    mean = calculate_mean(data)
    std = calculate_std(data, mean)
    standardized_data = (data - mean) / std
    return standardized_data

# 主成分分析の実行
def perform_pca(data):
    u, w, vt = np.linalg.svd(data, full_matrices=False)
    return u, w, vt

# PCA結果から各値を計算
def calculate_from_pca(u, w, vt):
    n_samples = w.shape[0]
    total_variance = np.sum(w ** 2)/n_samples#分散の和
    contribution_raito = (w ** 2)/n_samples / total_variance#寄与率
    cumulative_contribution_raito = np.cumsum(contribution_raito)#累積寄与率
    factor_loadings = np.sqrt(contribution_raito)*vt.T#因子負荷量
    principal_component_score = u @ np.diag(w)#主成分得点
    
    return contribution_raito, cumulative_contribution_raito, factor_loadings, principal_component_score


if __name__ == "__main__":
    # データを読み込む
    df = pd.read_csv(r"C:\Users\sd22028\Desktop\sd22028_report_1\sd22028_1_3\input_1_3.csv")

    #サンプルのラベルの作成
    label = list(df.iloc[:, 0])

    # 不要な列をデータフレームから削除
    df = df.drop(columns=["Unnamed: 0"])
    np_df = df.values

    # データを標準化
    standardized_data = standardize_data(np_df)

    # PCAを実行
    u, w, vt = perform_pca(standardized_data)

    # PCAの結果を評価
    contribution_raito, cumulative_contribution_raito, factor_loadings, principal_component_score = calculate_from_pca(u, w, vt)
    print("各主成分の寄与率:\n", contribution_raito)
    print("累積寄与率:\n", cumulative_contribution_raito)
    print("因子負荷量:\n", factor_loadings)

    # 表を作成
    indicators = [
        "流動比率　　　",
        "自己資本比率　",
        "固定比率　　　",
        "売上高成長率　",
        "営業利益成長率",
        "営業利益率　　",
        "労働生産性　　",
    ]

    print(f"{"指標":<20} {"PC1":>6} {"PC2":>6} {"PC3":>6}")
    print("="*49)
    for i, indicator in enumerate(indicators):
        row = [f"{factor_loadings[i, j]:.3f}" for j in range(factor_loadings.shape[1])]
        print(f"{indicator:<15} {row[0]:>6} {row[1]:>6} {row[2]:>6}")

    #独自の指標
    self_indicators = [
        "財務健全性指標",
        "トレンド指標",
        "保守的経営指標"
    ]
        
    # 主成分得点のプロット
    for x_pc in range(2):
        #初期化
        sum_x_pc = 0
        sum_y_pc = 0
        for y_pc in range(2-x_pc):
            plt.figure()
            for i, component in enumerate(principal_component_score):
                plt.scatter(component[x_pc], component[x_pc + y_pc + 1], s=30)
                plt.annotate(label[i], (component[x_pc], component[x_pc + y_pc + 1]))#データラベル追加
                #平均を計算
                sum_x_pc += component[x_pc]
                sum_y_pc += component[x_pc + y_pc + 1]
            avg_x_pc = sum_x_pc / len(label)
            avg_y_pc = sum_y_pc / len(label)
            plt.scatter(avg_x_pc, avg_y_pc, s=30)#平均をプロット
            plt.annotate("平均", (avg_x_pc, avg_y_pc))#データラベル追加
            #グラフの設定
            plt.xlabel(self_indicators[x_pc])
            plt.ylabel(self_indicators[x_pc + y_pc + 1])
            plt.grid()
    plt.show()

