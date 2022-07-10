def win_rsp(v1, v2):
    win_table = dict(가위=['바위', '가위', '보'], 
                     바위=['보', '바위', '가위'], 
                     보=['가위', '보', '바위'])
    status = win_table[v1].index(v2)
    if status == 0:
        return "Player1 lose"
    elif status == 1:
        return "Draw"
    else:
        return "Player1 win"