import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#yの1階微分である関数fの定義
def f(y, z):
    return z
#yの2階微分である関数gの定義
def g(y, z, a, b):
    return -b/a*y

#パラメータの読み込み
def read_params(file_name):
    df = pd.read_table(file_name, sep=" ", header=None)
    params = {row[0]: float(row[1]) for index, row in df.iterrows()}
    return params

#ルンゲクッタ法の計算
def the_fourth_runge_kutta(f, g, y0, z0, NDiv, hDiv, a, b):
    y = np.zeros(NDiv + 1)
    z = np.zeros(NDiv + 1)
    y[0], z[0] = y0, z0
    
    for i in range(1, NDiv + 1):
        s1 = f(y[i-1], z[i-1])
        l1 = g(y[i-1], z[i-1], a, b)
        
        s2 = f(y[i-1] + hDiv * s1/2, z[i-1] + hDiv * l1/2)
        l2 = g(y[i-1] + hDiv * s1/2, z[i-1] + hDiv * l1/2, a, b)
        
        s3 = f(y[i-1] + hDiv * s2/2, z[i-1] + hDiv * l2/2)
        l3 = g(y[i-1] + hDiv * s2/2, z[i-1] + hDiv * l2/2, a, b)
        
        s4 = f(y[i-1] + hDiv * s3, z[i-1] + hDiv * l3)
        l4 = g(y[i-1] + hDiv * s3, z[i-1] + hDiv * l3, a, b)
        
        y[i] = y[i-1] + hDiv * (s1 + 2*s2 + 2*s3 + s4) / 6
        z[i] = z[i-1] + hDiv * (l1 + 2*l2 + 2*l3 + l4) / 6
    
    return y

if __name__ =="__main__":
    #初期条件をdatファイルから読み込み
    params = read_params(r"input_1.dat")
    t_init = params["t_init"]
    y0 = params["y0"]
    z0 = params["z0"]
    NDiv = int(params["NDiv"])
    EndTime = params["EndTime"]
    a = params["a"]
    b = params["b"]
    hDiv = EndTime / NDiv

    #時間軸の設定
    t = np.linspace(t_init, EndTime, NDiv + 1)#数値解のt
    t_ideal = np.linspace(t_init, EndTime, 100000)#十分な精度を持つ理論解のNDivとして100000を採用

    #数値解の計算
    y_numerical = the_fourth_runge_kutta(f, g, y0, z0, NDiv, hDiv, a, b)

    #理論解の計算
    y_theoretical = np.cos(np.sqrt(b/a)*t_ideal)

    #結果のプロット
    plt.figure()
    plt.plot(t_ideal, y_theoretical, "r-", label="Numerical Solution")
    plt.plot(t, y_numerical, "b--", label="Theoretical Solution")
    plt.axhline(0, color="gray", linewidth=0.5)  
    plt.axvline(0, color="gray", linewidth=0.5)  
    plt.xlabel("t")
    plt.ylabel("y")
    plt.legend()
    plt.show()
