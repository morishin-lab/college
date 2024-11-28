import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import sys
import io

# 標準出力のエンコーディングを設定(出力文字化けのため)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

if __name__ == '__main__':
    # データを読み込む
    df = pd.read_csv(r"C:\Users\sd22028\Desktop\sd22028_report_1\sd22028_1_2\input_1_2.csv")

    #サンプルのラベルの作成
    labels_df = list(df.iloc[:, 0])

    # 不要な列をデータフレームから削除
    df = df.drop(columns=['Unnamed: 0'])
    np_df = df.values
    print('元のデータ行列:\n',np_df)

    #データフレームを標準化
    standardized_np_df=standardize_data(np_df)
    print('標準化されたデータ行列:\n',standardized_np_df)

    #特異値分解の実施
    U,w,Vt=perform_pca(standardized_np_df)

    #寄与率、累積寄与率、因子負荷量、主成分得点の計算
    contribution_raito, cumulative_contribution_raito, factor_loadings, principal_component_score = calculate_from_pca(U, w, Vt)

    # 結果を出力
    print("Obtained U:\n",U)
    print("Obtained w:\n",w)
    print("Obtained Vt:\n",Vt)
    print('UWV^T:\n', U@np.diag(w)@Vt)
    print('UWV^T / standardized_np_df:\n', U@np.diag(w)@Vt - standardized_np_df)    
    print('各主成分の寄与率:\n', contribution_raito)
    print('累積寄与率:\n', cumulative_contribution_raito)
    print('因子負荷量:\n', factor_loadings)
    print('主成分得点:\n', principal_component_score)

    #因子負荷量のプロット
    plt.figure(figsize=(8, 6))
    colors = ['red', 'orange', 'blue']#色の設定
    labels = ['ニュース', 'スポーツ', 'ビジネス']#ラベルの設定
    for i in range(factor_loadings.shape[1]):
        plt.scatter(factor_loadings[i, 0], factor_loadings[i, 1], color=colors[i],s=50, marker='s')
        plt.annotate(labels[i], (factor_loadings[i, 0], factor_loadings[i, 1]))  # データラベル追加
    # グラフの設定
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlabel('第一主成分')
    plt.ylabel('第二主成分')
    # x軸とy軸の範囲の調整
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.show()

    # 主成分得点のプロット
    plt.figure()
    for pc in range(w.shape[0]-2):
        for i, component in enumerate(principal_component_score):
            plt.scatter(component[pc], component[pc + 1],color='black', s=10)
            plt.annotate(labels_df[i], (component[pc], component[pc + 1]))  # データラベル追加
        # グラフの設定
        plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
        plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
        plt.xlabel('PC' + str(pc + 1))
        plt.ylabel('PC' + str(pc + 2))
        plt.show()