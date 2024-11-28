import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#xの一階微分
def fx(x, y, vx, vy):
    return vx

#yの一階微分
def fy(x, y, vx, vy):
    return vy

#xの二階微分
def gx(x, y, vx, vy):
    return 0  #水平方向の加速度なし

#yの二階微分
def gy(x, y, vx, vy, m):
    return -9.8*m  #重力加速度

#ルンゲクッタ法を用いたパチンコのシミュレーション
def the_fourth_runge_kutta_pachinko(fx, fy, gx, gy, x0, y0, vx0, vy0, NDiv, hDiv, nails, targets, e_nail, e_end, m):
    x = np.zeros(NDiv + 1)
    y = np.zeros(NDiv + 1)
    vx = np.zeros(NDiv + 1)
    vy = np.zeros(NDiv + 1)
    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    
    win_flag = False  #パチンコの勝敗判定
    
    for n in range(1, NDiv + 1):
        k1x = fx(x[n-1], y[n-1], vx[n-1], vy[n-1])
        k1y = fy(x[n-1], y[n-1], vx[n-1], vy[n-1])
        k1vx = gx(x[n-1], y[n-1], vx[n-1], vy[n-1])
        k1vy = gy(x[n-1], y[n-1], vx[n-1], vy[n-1], m)
        
        k2x = fx(x[n-1] + hDiv*k1x/2, y[n-1] + hDiv*k1y/2, vx[n-1] + hDiv*k1vx/2, vy[n-1] + hDiv*k1vy/2)
        k2y = fy(x[n-1] + hDiv*k1x/2, y[n-1] + hDiv*k1y/2, vx[n-1] + hDiv*k1vx/2, vy[n-1] + hDiv*k1vy/2)
        k2vx = gx(x[n-1] + hDiv*k1x/2, y[n-1] + hDiv*k1y/2, vx[n-1] + hDiv*k1vx/2, vy[n-1] + hDiv*k1vy/2)
        k2vy = gy(x[n-1] + hDiv*k1x/2, y[n-1] + hDiv*k1y/2, vx[n-1] + hDiv*k1vx/2, vy[n-1] + hDiv*k1vy/2, m)
        
        k3x = fx(x[n-1] + hDiv*k2x/2, y[n-1] + hDiv*k2y/2, vx[n-1] + hDiv*k2vx/2, vy[n-1] + hDiv*k2vy/2)
        k3y = fy(x[n-1] + hDiv*k2x/2, y[n-1] + hDiv*k2y/2, vx[n-1] + hDiv*k2vx/2, vy[n-1] + hDiv*k2vy/2)
        k3vx = gx(x[n-1] + hDiv*k2x/2, y[n-1] + hDiv*k2y/2, vx[n-1] + hDiv*k2vx/2, vy[n-1] + hDiv*k2vy/2)
        k3vy = gy(x[n-1] + hDiv*k2x/2, y[n-1] + hDiv*k2y/2, vx[n-1] + hDiv*k2vx/2, vy[n-1] + hDiv*k2vy/2, m)
        
        k4x = fx(x[n-1] + hDiv*k3x, y[n-1] + hDiv*k3y, vx[n-1] + hDiv*k3vx, vy[n-1] + hDiv*k3vy)
        k4y = fy(x[n-1] + hDiv*k3x, y[n-1] + hDiv*k3y, vx[n-1] + hDiv*k3vx, vy[n-1] + hDiv*k3vy)
        k4vx = gx(x[n-1] + hDiv*k3x, y[n-1] + hDiv*k3y, vx[n-1] + hDiv*k3vx, vy[n-1] + hDiv*k3vy)
        k4vy = gy(x[n-1] + hDiv*k3x, y[n-1] + hDiv*k3y, vx[n-1] + hDiv*k3vx, vy[n-1] + hDiv*k3vy, m)
        
        x[n] = x[n-1] + hDiv * (k1x + 2*k2x + 2*k3x + k4x) / 6
        y[n] = y[n-1] + hDiv * (k1y + 2*k2y + 2*k3y + k4y) / 6
        vx[n] = vx[n-1] + hDiv * (k1vx + 2*k2vx + 2*k3vx + k4vx) / 6
        vy[n] = vy[n-1] + hDiv * (k1vy + 2*k2vy + 2*k3vy + k4vy) / 6
        
        #釘との衝突
        for nail in nails:
            dx = x[n] - nail[0]  #ボール-釘のx座標の差
            dy = y[n] - nail[1]  #ボール-釘のy座標の差
            distance = np.sqrt(dx**2 + dy**2)  #ボール-釘の距離
            if distance < 0.19:  #ボールの衝突判定
                normal_vec = np.array([dx, dy]) / distance  #釘とボールの接点の法線ベクトル
                velocity_vec = np.array([vx[n], vy[n]])  #ボールの速度ベクトル
                reflection_vec = velocity_vec - 2 * np.dot(velocity_vec, normal_vec) * normal_vec  #反射後のボールの速度ベクトル
                #衝突後の位置を調整
                x[n] = nail[0] + normal_vec[0] * 0.2
                y[n] = nail[1] + normal_vec[1] * 0.2
                vx[n], vy[n] = reflection_vec * e_nail  #反発係数の考慮

        #勝利判定
        if not win_flag:  #win_flagがFalseのときのみ
            for target in targets:
                #ボールがターゲットの範囲内にあり、y座標が0.2未満の場合
                if target[0] <= x[n] <= target[1] and y[n] < 0.2:
                    print(f"YOU WIN! Timestep: {n * hDiv:.2f} s")  #勝利メッセージと経過時間を出力
                    vx[n] = 0  #ボールのx方向の速度を0
                    vy[n] = 0  #ボールのy方向の速度を0
                    win_flag = True  #勝利判定
                    break 

        
        #地面との衝突
        if y[n] < 0.2:
            y[n] = 0.2  #衝突後の位置を調整
            vy[n] = 0
            vx[n] = 0

        #右端との衝突
        if x[n] > 9.8:
            x[n] = 9.8  #衝突後の位置を調整
            vx[n] = -vx[n] * e_end  #反発係数の考慮

        #左端との衝突
        if x[n] < 0.2:
            x[n] = 0.2  #衝突後の位置を調整
            vx[n] = -vx[n] * e_end  #反発係数の考慮
    
    return x, y, vx, vy

#初期化関数
def init():
    #各ボール位置とその軌跡を初期化
    for ball, traj in zip(balls, trajectories):
        ball.set_data([], [])  #ボール位置初期化
        traj.set_data([], [])  #軌跡初期化
    return balls + trajectories 

#更新関数
def update(frame):
    #各フレームでのボールと軌跡のデータを更新
    for i, (ball, traj) in enumerate(zip(balls, trajectories)):
        ball.set_data([x_list[i][frame]], [y_list[i][frame]])  #ボールの現在の位置を設定
        traj.set_data(x_list[i][:frame+1], y_list[i][:frame+1])  #ボールの軌跡を設定
    ax.set_title(f"Timestep: {frame * hDiv:.2f}")  #タイトルに現在の経過時間を表示
    return balls + trajectories  

#パラメータを読み込み
def read_params(file_name):
    df = pd.read_table(file_name, sep="\s+", header=None)
    params = {row[0]: float(row[1]) for index, row in df.iterrows()}
    return params

if __name__ == "__main__":
    #datファイルからパラメータを読み込み
    params = read_params(r"input_3.dat")
    
    x0 = params["x0"]  #xの初期値
    y0 = params["y0"]  #yの初期値
    vx0 = params["vx0"]  #xvの初期値
    vy0 = params["vy0"]  #yvの初期値
    NDiv = int(params["NDiv"])
    EndTime = params["EndTime"]
    hDiv = EndTime / NDiv
    num_balls = int(params["num_balls"])#ボールの数
    m = params["m"]  #質量
    e_nail = params["e_nail"]  #釘との反発係数
    e_end = params["e_end"]  #端との反発係数

    #釘の配置
    nails = [] #リストの初期化
    x_center = params["x_center"]  #スパイラルの中心のx座標
    y_center = params["y_center"]  #スパイラルの中心のy座標
    r_max = params["r_max"]  #スパイラルの最大半径
    num_spirals = int(params["num_spirals"])  #スパイラルの数
    num_points_per_spiral = int(params["num_points_per_spiral"])  #各スパイラルに配置する点の数

    nail_1_x = params["nail_1_x"]
    nail_1_y = params["nail_1_y"]
    nail_2_x = params["nail_2_x"]
    nail_2_y = params["nail_2_y"]
    nail_3_x = params["nail_3_x"]
    nail_3_y = params["nail_3_y"]
    target_x = params["target_x"]
    target_y = params["target_y"]

    #スパイラルを生成するループ
    for i in range(num_spirals):
        if i == 0 or i == 2:  #ボールの挟まり防止のため最初のスパイラルと3番目のスパイラルをスキップ
            continue
        r = r_max * (i / num_spirals)  #スパイラルの半径を計算
        theta_offset = (i % 2) * np.pi / num_points_per_spiral  #スパイラルが交互にずれるように設定

        for j in range(num_points_per_spiral):
            theta = 2 * np.pi * j / num_points_per_spiral + theta_offset  #点の角度の計算
            x_pos = x_center + r * np.cos(theta)  #点のx座標の計算
            y_pos = y_center + r * np.sin(theta)  #点のy座標の計算
            #点が画面内に収まる場合のみ追加
            if 0 <= x_pos <= 12 and 0 <= y_pos <= 10:
                nails.append([x_pos, y_pos])  

    #追加の釘を手動で配置
    nails.append([nail_1_x, nail_1_y])  #追加の釘1を配置
    nails.append([nail_2_x, nail_2_y])  #追加の釘2を配置
    nails.append([nail_3_x, nail_3_y])  #追加の釘3を配置


    # ターゲットの配置
    targets = [[target_x, target_y]]  # あたりの判定を指定

    # 初期条件をボールごとに微小に変化させた複数のボールのシミュレーション
    initial_conditions = [(vx0 + 0.01 * i, vy0 - 0.01 * i) for i in range(num_balls)]
    x_list, y_list = [], []  # 座標の空リスト

    # 初期条件ごとのルンゲクッタ法の計算
    for vx0, vy0 in initial_conditions:
        x, y, vx, vy = the_fourth_runge_kutta_pachinko(fx, fy, gx, gy, x0, y0, vx0, vy0, NDiv, hDiv, nails, targets, e_nail, e_end, m)
        x_list.append(x)
        y_list.append(y)

    # アニメーション用のグラフの設定
    fig, ax = plt.subplots(figsize=(6.5, 7.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # 釘をプロット
    nail_patches = [ax.plot(nail[0], nail[1], "o", color="red", markersize=7)[0] for nail in nails]

    # 当たり判定エリアをプロット
    for target in targets:
        ax.plot([target[0], target[1]], [0.2, 0.2], "g-", linewidth=5)

    # ボールの色および軌跡を作成
    colors = plt.get_cmap("tab20", num_balls).colors
    balls = [ax.plot([], [], "o", color=colors[i], markersize=7)[0] for i in range(num_balls)]
    trajectories = [ax.plot([], [], color=colors[i])[0] for i in range(num_balls)]

    # アニメーションの描画
    ani = FuncAnimation(fig, update, frames=NDiv, init_func=init, blit=True, interval=0.001)

    # アニメーションを表示
    plt.show()
