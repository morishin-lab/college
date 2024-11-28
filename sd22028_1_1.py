import numpy as np
import pandas as pd

# 主成分分析の実行
def perform_pca(data):
    u, w, vt = np.linalg.svd(data, full_matrices=False)
    return u, w, vt

if __name__ == '__main__':
    # データを読み込む
    df = pd.read_csv(r"C:\Users\sd22028\Desktop\sd22028_report_1\sd22028_1_1\report_1_1.csv")
    np_df = df.values

    #特異値分解を実施
    U,w,Vt=perform_pca(df)

    #結果を出力
    print("U=",U)
    print()
    print("w=",np.diag(w))
    print()
    print("Vt=",Vt)