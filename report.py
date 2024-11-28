import random


#%%
def is_convertible_to_int(input_str):
    #整数に変換できるかどうかを返す
    #入力：文字列　出力：真偽値
    try:
        int(input_str)
        return True
    except ValueError:
        return False


assert is_convertible_to_int("123")
assert not is_convertible_to_int("ac")


#%%
def input_bordsize():
    #ボードの大きさを決定
    #入力：なし　出力：ボードサイズ
    size = input(
        "ラッキーナンバーを始めます。まず、ボードの大きさを数字で入力してください。数字は4から6までの一桁とします。 \n 例：4×4のボードの場合、4を入力 \n ボードサイズ："
    )
    return size


#%%
def check_input_bordsize(bs):
    #ボードサイズの入力が正しいか確認
    #入力：ボードサイズ　出力：真偽値
    if is_convertible_to_int(bs):
        if 4 <= int(bs) <= 6:
            return True
    return False


assert not check_input_bordsize(7)
assert check_input_bordsize(4)
assert not check_input_bordsize("a")
assert not check_input_bordsize("あ")


#%%
def input_players():
    #プレイヤー数の入力
    #入力：なし　出力：プレイヤー数
    players = input(
        "プレイヤー数を入力してください。2人から4人までとします \n 例：2人でプレイする場合、2と入力 \n プレイヤー数：")
    return players


#%%
def check_input_players(p):
    #プレイヤー数入力の確認
    #入力：プレイヤー数　出力：真偽値
    if is_convertible_to_int(p):
        if 2 <= int(p) <= 4:
            return True
    return False


assert check_input_players(4)
assert not check_input_players(1)
assert not check_input_players("a")


#%%
def init_board(bs):
    #ボードの初期化
    #入力：ボードサイズ　出力：盤面のリスト

    board = []

    #チェスボードの行番号と列番号のラベル
    row_labels = [str(num) for num in range(1, bs + 1)]
    column_labels_name = ['a', 'b', 'c', 'd', 'e', 'f']
    column_labels = [" " + column_labels_name[i] for i in range(bs)]

    #列番号ラベルの作成
    column_board = [" "]  #ボードの目盛り位置の調整
    column_board += column_labels
    board += [column_board]  #リストの各要素は行を表す

    #行番号ラベルと升目の作成
    board += [["__" for i in range(bs + 2)]]
    for row in range(bs):
        row_board = []  #空マス
        row_board += [row_labels[row]]
        for col in range(bs + 1):  #空マスを列左一列目に追加
            row_board += ["__"]
        board += [row_board]  #リストの各要素は行を表す

    return board


assert init_board(4) == [[' ', ' a', ' b', ' c', ' d'],
                         ['__', '__', '__', '__', '__', '__'],
                         ['1', '__', '__', '__', '__', '__'],
                         ['2', '__', '__', '__', '__', '__'],
                         ['3', '__', '__', '__', '__', '__'],
                         ['4', '__', '__', '__', '__', '__']]
assert init_board(6) == [[' ', ' a', ' b', ' c', ' d', ' e', ' f'],
                         ['__', '__', '__', '__', '__', '__', '__', '__'],
                         ['1', '__', '__', '__', '__', '__', '__', '__'],
                         ['2', '__', '__', '__', '__', '__', '__', '__'],
                         ['3', '__', '__', '__', '__', '__', '__', '__'],
                         ['4', '__', '__', '__', '__', '__', '__', '__'],
                         ['5', '__', '__', '__', '__', '__', '__', '__'],
                         ['6', '__', '__', '__', '__', '__', '__', '__']]


#%%
def plyers_boards(p, bs):
    #人数分のボードを一つのリストに格納
    #入力：プレイヤー数・ボードサイズ　出力：ボードをまとめたリスト

    boards = []
    for i in range(p):
        boards.append(init_board(bs))
    return boards


assert plyers_boards(2, 4) == [[[' ', ' a', ' b', ' c', ' d'],
                                ['__', '__', '__', '__', '__', '__'],
                                ['1', '__', '__', '__', '__', '__'],
                                ['2', '__', '__', '__', '__', '__'],
                                ['3', '__', '__', '__', '__', '__'],
                                ['4', '__', '__', '__', '__', '__']],
                               [[' ', ' a', ' b', ' c', ' d'],
                                ['__', '__', '__', '__', '__', '__'],
                                ['1', '__', '__', '__', '__', '__'],
                                ['2', '__', '__', '__', '__', '__'],
                                ['3', '__', '__', '__', '__', '__'],
                                ['4', '__', '__', '__', '__', '__']]]


#%%
def init_cards(p, bs):
    #カードの初期化
    #入力：プレイヤ数　出力：カードの山札

    carddeck = []

    #人数分のカード束の準備
    cards = list(map(str, [card for card in range(1, 21 + (bs - 4) * 5)]))
    for players in range(p):
        carddeck += cards

    #カードをシャッフル
    random.shuffle(carddeck)

    return carddeck


assert init_cards(2, 4) == [
    '1', '8', '13', '2', '10', '16', '19', '15', '2', '1', '8', '6', '11',
    '14', '15', '18', '3', '20', '4', '18', '9', '16', '4', '14', '10', '5',
    '17', '7', '9', '19', '12', '11', '20', '6', '12', '13', '17', '3', '7',
    '5'
]
assert init_cards(2, 5) == [
    '19', '2', '4', '15', '12', '13', '1', '3', '23', '8', '9', '10', '21',
    '25', '6', '14', '12', '24', '16', '16', '11', '22', '22', '4', '10', '5',
    '17', '18', '15', '18', '5', '21', '7', '11', '19', '9', '20', '14', '13',
    '23', '6', '20', '1', '7', '8', '17', '3', '2', '24', '25'
]
assert init_cards(3, 4) == [
    '13', '14', '10', '17', '5', '3', '8', '6', '8', '11', '16', '19', '4',
    '8', '9', '20', '1', '2', '2', '19', '15', '16', '12', '7', '1', '16',
    '11', '6', '12', '4', '18', '18', '2', '5', '1', '10', '10', '15', '14',
    '20', '7', '4', '19', '9', '13', '14', '18', '3', '11', '20', '6', '12',
    '13', '17', '3', '7', '17', '9', '5', '15'
]


#%%
def board_ready(bl, c, bs):
    #ボードにカードを４枚並べ、初期準備をする。
    #入力：盤面・カード・ボードサイズ　出力：盤面・カード
    for i in range(len(bl)):
        init_cards = list(map(int, c[0:bs]))
        init_cards.sort()
        for j in range(bs):  #ボードサイズに対応する座標を指定
            if len(str(init_cards[j])) == 1:
                bl[i][j + 2][j + 2] = " " + str(init_cards[j])
            else:
                bl[i][j + 2][j + 2] = str(init_cards[j])
        c = c[bs:]

    return bl, c


assert board_ready([
    [[' ', 'a', 'b', 'c', 'd'], ['__', '__', '__', '__', '__', '__'],
     ['1', '__', '__', '__', '__', '__'], ['2', '__', '__', '__', '__', '__'],
     ['3', '__', '__', '__', '__', '__'], ['4', '__', '__', '__', '__', '__']],
    [[' ', 'a', 'b', 'c', 'd'], ['__', '__', '__', '__', '__', '__'],
     ['1', '__', '__', '__', '__', '__'], ['2', '__', '__', '__', '__', '__'],
     ['3', '__', '__', '__', '__', '__'], ['4', '__', '__', '__', '__', '__']]
], [
    '1', '8', '13', '2', '10', '16', '19', '15', '2', '1', '8', '6', '11',
    '14', '15', '18', '3', '20', '4', '18', '9', '16', '4', '14', '10', '5',
    '17', '7', '9', '19', '12', '11', '20', '6', '12', '13', '17', '3', '7',
    '5'
], 4) == ([[[' ', 'a', 'b', 'c', 'd'], ['__', '__', '__', '__', '__', '__'],
            ['1', '__', ' 1', '__', '__', '__'],
            ['2', '__', '__', ' 2', '__', '__'],
            ['3', '__', '__', '__', ' 8', '__'],
            ['4', '__', '__', '__', '__', '13']],
           [[' ', 'a', 'b', 'c', 'd'], ['__', '__', '__', '__', '__', '__'],
            ['1', '__', '10', '__', '__', '__'],
            ['2', '__', '__', '15', '__', '__'],
            ['3', '__', '__', '__', '16', '__'],
            ['4', '__', '__', '__', '__', '19']]], [
                '2', '1', '8', '6', '11', '14', '15', '18', '3', '20', '4',
                '18', '9', '16', '4', '14', '10', '5', '17', '7', '9', '19',
                '12', '11', '20', '6', '12', '13', '17', '3', '7', '5'
            ])


#%%
def print_table(bl, bc, bs):
    #テーブルの状況を表示
    #入力：盤面・ボード上のカード・ボードサイズ　出力：なし

    for i in range(len(bl)):
        #盤面のコピー
        bl_copied = []
        for j in bl[i]:
            row_copied = j[:]
            bl_copied.append(row_copied)

        print("[board_" + str(i + 1) + "]")  #ボード名の表記
        print(" ".join(bl[i][0]))  #行ラベルの描画

        bl_copied.pop(1)  #空マスの削除
        for j in range(bs):  #列ラベルと盤面の描画
            bl_copied[j + 1].pop(1)  # 空マスの削除
            print(" ".join(bl_copied[j + 1]))
        print("____________________")
        print(" ".join(bc))
        print()
        print()


#%%
def input_card(t):
    #入力：なし　出力：標準出力
    print("あなたはboard_" + str(t) + "です")
    cardtype = input("山札からカードを引く場合はDを、テーブル上のカードを引く場合はその番号を入力してください:")
    print("")
    return cardtype


#%%
def check_input_card(ct, bc):
    #カードタイプを指定
    #入力：ボード上のタイル　出力：判定
    if is_convertible_to_int(ct):
        if len(bc) == 1:
            return "n"
        elif not ct in bc:
            return "w"
        else:
            return ct
    elif ct != "D":
        return "w"
    else:
        return "d"


assert check_input_card("d", ["D", "3"]) == "w"
assert check_input_card("D", ["D", "3"]) == "d"
assert check_input_card("3", ["D", "3"]) == "3"
assert check_input_card("3", ["D"]) == "n"
assert check_input_card("4", ["D", "3"]) == "w"


#%%
def pick_cards(c, bc, ct):
    #カードを引く
    #入力：カード・カードタイプ・ボード上のカード　出力：引いたカード
    if ct == "D":
        card = c[0]
        c = c[1:]
    else:
        card = ct
        bc.remove(ct)
    return card, c


assert pick_cards(["3", "13", "18"], ["D", "2", "13"],
                  "D") == ("3", ["13", "18"])
assert pick_cards(["3", "13", "18"], ["D", "2", "13"],
                  "2") == ("2", ["3", "13", "18"])


#%%
def print_cards(c):
    #引いたカードを表示する
    #入力：カード　出力：なし
    print("引いたカードは" + str(c) + "です")
    print()


#%%
def input_cardplace():
    #カードの場所を受け取る
    #入力：なし　出力：座標
    coordnate = input(
        "カードを置きたい場所の、列番号、行番号を指定してください。\n 例：1行a列に置きたい場合、 a1 と入力 \n 座標：")
    return list(coordnate)


#%%
def check_input_cardplace(cp, b, bs, c, co):
    #カードの場所が正しいか判別
    #入力：ボード、座標　出力：座標
    #(エイリアシングで座標を更新)

    #2文字以上の入力を除外
    if len(cp) > 2:
        return False

    column_labels_name = ['a', 'b', 'c', 'd', 'e', 'f']
    row_labels = [str(i) for i in range(1, bs + 1)]

    #入力座標を変換
    for i in cp:
        if i in row_labels:
            co[0] = int(i) + 1
        elif i in column_labels_name:
            co[1] = column_labels_name.index(i) + 2
    #正しく座標に変換されているか確認
    for i in co:
        if not is_convertible_to_int(i):
            return False

    #縦の判定
    for i in range(co[0] - 1):  #ラベルの分を引く
        if is_convertible_to_int(b[i + 1][co[1]]):
            if int(b[i + 1][co[1]]) > int(c):  #上のマスの数字が大きくないか確認
                return False
    for j in range(bs - co[0] + 2):  #ラベル、空マスの分を足す
        if j == 0:
            continue
        elif is_convertible_to_int(b[j + co[0]][co[1]]):
            if int(b[j + co[0]][co[1]]) < int(c):  #下のマスの数字が小さくないか確認
                return False
    #横の判定
    for i in range(co[1] - 1):  #ラベルの分を引く
        if is_convertible_to_int(b[co[0]][i + 1]):
            if int(b[co[0]][i + 1]) > int(c):  #左のマスの数字が大きくないか確認
                return False
    for j in range(bs - co[1] + 2):  #ラベル、空マスの分を足す
        if j == 0:
            continue
        elif is_convertible_to_int(b[co[0]][j + co[1]]):
            if int(b[co[0]][j + co[1]]) < int(c):  #右のマスの数字が小さくないか確認
                return False
    return True


assert check_input_cardplace(
    ["c", "2"],
    [[' ', 'a', 'b', 'c', 'd'], ['__', '__', '__', '__', '__', '__'],
     ['1', '__', '1', '__', '__', '__'], ['2', '__', '__', '2', '__', '__'],
     ['3', '__', '__', '__', '8', '__'], ['4', '__', '__', '__', '__', '13']],
    4, "2", ["", ""])

assert not check_input_cardplace(["c", "2"], [
    [' ', 'a', 'b', 'c', 'd'], ['__', '__', '__', '__', '__', '__'],
    ['1', '__', '1', '__', '__', '__'], ['2', '__', '__', '2', '__', '__'],
    ['3', '__', '__', '__', '8', '__'], ['4', '__', '__', '__', '__', '13']
], 4, "1", ["", ""])

assert not check_input_cardplace(["d", "2"], [
    [' ', 'a', 'b', 'c', 'd'], ['__', '__', '__', '__', '__', '__'],
    ['1', '__', '1', '__', '__', '__'], ['2', '__', '__', '2', '__', '__'],
    ['3', '__', '__', '__', '8', '__'], ['4', '__', '__', '__', '__', '13']
], 4, "20", ["", ""])


#%%
def place_cards(b, co, c, bc):
    #カードを置く
    #入力：盤面、座標、カード、テーブル上のカード　出力：盤面

    if b[co[0]][co[1]] != "__":
        bc.append(b[co[0]][co[1]])
    if len(c) == 1:
        b[co[0]][co[1]] = " " + c
    else:
        b[co[0]][co[1]] = c

    return b


assert place_cards(
    [[' ', 'a', 'b', 'c', 'd'], ['__', '__', '__', '__', '__', '__'],
     ['1', '__', '1', '__', '__', '__'], ['2', '__', '__', '2', '__', '__'],
     ['3', '__', '__', '__', '8', '__'], ['4', '__', '__', '__', '__', '13']],
    [3, 4], "2", ["D"]) == [[' ', 'a', 'b', 'c', 'd'],
                            ['__', '__', '__', '__', '__', '__'],
                            ['1', '__', '1', '__', '__', '__'],
                            ['2', '__', '__', '2', ' 2', '__'],
                            ['3', '__', '__', '__', '8', '__'],
                            ['4', '__', '__', '__', '__', '13']]
assert place_cards(
    [[' ', 'a', 'b', 'c', 'd'], ['__', '__', '__', '__', '__', '__'],
     ['1', '__', '1', '__', '__', '__'], ['2', '__', '__', '2', '__', '__'],
     ['3', '__', '__', '__', '8', '__'], ['4', '__', '__', '__', '__', '13']],
    [3, 3], "2", ["D"]) == [[' ', 'a', 'b', 'c', 'd'],
                            ['__', '__', '__', '__', '__', '__'],
                            ['1', '__', '1', '__', '__', '__'],
                            ['2', '__', '__', ' 2', '__', '__'],
                            ['3', '__', '__', '__', '8', '__'],
                            ['4', '__', '__', '__', '__', '13']]


#%%
def game_finished(board, bs):
    #ゲームの終了を判定
    #入力：盤面、ボードサイズ　出力：真偽値
    board_for_judge = board[2:]
    b_copied = []
    for j in board_for_judge:
        row_copied = j[:]
        b_copied.append(row_copied)
    for i in range(bs):
        b_copied[i].pop(1)
        if "__" in "".join(b_copied[i]):
            return False

    return True


assert not game_finished(
    [[' ', 'a', 'b', 'c', 'd'], ['__', '__', '__', '__', '__', '__'],
     ['1', '__', '1', '__', '__', '__'], ['2', '__', '__', '2', '__', '__'],
     ['3', '__', '__', '__', '8', '__'], ['4', '__', '__', '__', '__', '13']],
    4)
assert game_finished(
    [[' ', 'a', 'b', 'c', 'd'], ['__', '__', '__', '__', '__', '__'],
     ['1', '__', '1', '1', '1', '1'], ['2', '__', '2', '2', '2', '2'],
     ['3', '__', '8', '8', '8', '8'], ['4', '__', '1', '1', '1', '13']], 4)


#%%
def print_winner(b, bc, bs, t):
    #勝者を表示
    #入力：盤面、テーブル上のカード、ボードサイズ、ターン　出力：なし
    print("ゲームは終了しました")
    print()
    print_board(b, bc, bs)
    print("勝者は")
    print()
    print("board_" + str(t))
    print()
    print("です。")


#%%
def count_turn(t, p):
    #ターンをカウント
    #入力：盤面、座標、カード、テーブル上のカード　出力：ターン
    t += 1
    if t > p:
        t = 1
    return t


assert count_turn(1, 2) == 2
assert count_turn(4, 4) == 1


#%%
def swap_board(bl, t):
    #ボードを入れ替える
    #入力：ボードリスト、ターン　出力：盤面
    board = bl[t - 1]
    return board


assert swap_board([[[1]], [[2]]], 2) == [[2]]
assert swap_board([[[1]], [[2]]], 1) == [[1]]


#%%
def print_board(b, t, bs, bc):
    #盤面を表示
    #入力：盤面、ターン、ボードサイズ、テーブル上のカード　出力：なし
    b_copied = []
    for j in b:
        row_copied = j[:]
        b_copied.append(row_copied)
    print("[board_" + str(t) + "]")  #ボード名の表記
    print(" ".join(b[0]))  #行ラベルの描画
    b_copied.pop(1)  #空マスの削除
    for j in range(bs):  #列ラベルと盤面の描画
        b_copied[j + 1].pop(1)  # 空マスの削除
        print(" ".join(b_copied[j + 1]))
    print("_____________________")
    print(" ".join(bc))


#%%
if __name__ == '__main__':
    TURN = 0
    while True:  #ボードサイズの決定
        bordsize = input_bordsize()
        if check_input_bordsize(bordsize):
            bordsize = int(bordsize)
            break
        print("入力が正しくありません")
    while True:  #プレイヤ数の決定
        players = input_players()
        if check_input_players(players):
            players = int(players)
            break
        print("入力が正しくありません")
    #ボードの初期化
    board_list = plyers_boards(players, bordsize)
    cards_on_table = ["D"]
    turn = TURN
    #カードの初期化
    deck = init_cards(players, bordsize)
    #ボードにカードを４枚並べ、初期準備をする。
    (board_list, deck) = board_ready(board_list, deck, bordsize)
    while True:
        #ターンをカウント
        turn = count_turn(turn, players)
        #ボードを入れ変える
        board = swap_board(board_list, turn)
        #テーブルの状況を表示
        print_table(board_list, cards_on_table, bordsize)
        #テーブル上のカードを指定
        while True:
            print_board(board, turn, bordsize, cards_on_table)
            deck_or_table = input_card(turn)
            state = check_input_card(deck_or_table, cards_on_table)
            if state == "n":  #表向きのカードが無かった場合
                print("テーブルに表向きのカードがありません。山札からカードを引きます。")
                deck_or_table = "D"
                break
            elif state == "w":  #指定したカードが無かった場合
                print("指定したカードはテーブルにありません。")
                continue
            else:  #デッキまたはカードを指定した場合
                break
        #カードを引く
        (card, deck) = pick_cards(
            deck,
            cards_on_table,
            deck_or_table,
        )
        print_cards(card)  #引いたカードの出力
        while True:  #カードを引いておく
            coordinate = ["", ""]  #座標の初期化
            #カードを置く座標を指定
            place = input_cardplace()
            if check_input_cardplace(place, board, bordsize, card,
                                     coordinate):  #カード座標が正しいか確認
                #カードを置く
                board = place_cards(board, coordinate, card, cards_on_table)
                break
            print("入力座標が正しくありません")
        if game_finished(board, bordsize):  #ゲーム終了の確認
            break
    print_winner(board, cards_on_table, bordsize, turn)  #勝者の表示
