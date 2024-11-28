import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#yの1階微分である関数fの定義
def f(y, z):
    return z
#yの2階微分である関数gの定義
def g(y, z, a, b):
    return -b/a*y

#パラメータを読み込み
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
    params = read_params(r"input_2.dat")
    t_init = params["t_init"]
    y0 = params["y0"]
    z0 = params["z0"]
    NDiv_start = int(params["NDiv_start"])
    NDiv_end = int(params["NDiv_end"]) 
    NDiv_step = int(params["NDiv_step"])
    EndTime = params["EndTime"]
    a = params["a"]
    b = params["b"]
    E = int(params["E"])
    

    #時間軸の設定
    t_ideal = np.linspace(t_init, EndTime, 100000)#十分な精度を持つ理論解のNDivとして100000を採用

    #理論解の計算
    y_theoretical = np.cos(np.sqrt(b/a)*t_ideal)

    # 誤差の保存用リスト
    errors = []
    NDiv_values = []

    #結果のプロット
    plt.figure(figsize=(10,5))

    #理論解と数値解の比較
    for NDiv in range(NDiv_start,NDiv_end + 1,NDiv_step):
        hDiv = EndTime/NDiv
        t = np.linspace(t_init, EndTime, NDiv + 1)
        y_numerical = the_fourth_runge_kutta(f, g, y0, z0, NDiv, hDiv, a, b)
        plt.plot(t, y_numerical, "-", label="Numerical Solution_"+ str(NDiv))
        

    #分割数と平均誤差の関係
    for mul in range(E):
        NDiv = 10**mul
        hDiv = EndTime/NDiv
        t = np.linspace(0, EndTime, NDiv + 1)
        y_numerical = the_fourth_runge_kutta(f, g, y0, z0, NDiv, hDiv, a, b)
        y_theoretical_subset = np.cos(np.sqrt(b/a) * t)
        error = np.abs(y_numerical - y_theoretical_subset)#誤差の計算
        mean_error = np.mean(error)#平均誤差の計算
        errors.append(mean_error)
        NDiv_values.append(NDiv)

    plt.plot(t_ideal, y_theoretical, "b--", label="Theoretical Solution")
    plt.axhline(0, color='gray', linewidth=0.5)  
    plt.axvline(0, color='gray', linewidth=0.5)  
    plt.xlabel("t")
    plt.ylabel("y")
    plt.ylim(-2,2)
    plt.legend()
    plt.show()

    #NDivと平均誤差の関係をプロット
    plt.figure()
    plt.plot(NDiv_values, errors, "o-")
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel("Mean Error")
    plt.grid(True, which="both", ls="--")
    plt.show()