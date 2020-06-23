import time

def solve(board,update_fun,inteval):
    col = []
    row = []
    sqa = []
    board2 = []

    for y in range(len(board)):
        row.append({})

        for x in range(len(board[y])):
            n = board[y][x]
            si = y//3*3 + x//3
            
            if(n != 0):
                row[y][n] = True

            if(y == 0):
                col.append({})

            if(n != 0):
                col[x][n] = True
            

            if(len(sqa)<=si):
                sqa.append({})

            
            if(n != 0):
                sqa[si][n] = True
    
    
    index = 0
    k = 1

    while(index<81):
        i = index//9
        j = index % 9
        si = j//3 + i//3 * 3

        if(board[i][j] != 0):
            index+=1
        else:
            while(k<=10):
                if(k == 10):
                    o = board2.pop()
                    _i = o["i"]
                    _j = o["j"]
                    _k = o["k"]
                    _si = o["si"]

                    k = _k +1
                    board[_i][_j] = 0
                    row[_i][_k] = False
                    col[_j][_k] = False
                    sqa[_si][_k] = False
                    index = o["index"]

                    update_fun(index)
                    # time.sleep(inteval)
                    break

                elif(((not k in row[i]) or row[i][k] == False) and ((not k in col[j]) or col[j][k] == False) and ((not k in sqa[si]) or sqa[si][k] == False)):
                    row[i][k] = True
                    col[j][k] = True
                    sqa[si][k] = True
                    board[i][j] = k
                    record = {}
                    record["index"] = index
                    record["si"] = si
                    record["i"] = i
                    record["j"] = j
                    record["k"] = k
                    board2.append(record)
                    index+=1
                    k = 1

                    update_fun(index)
                    # time.sleep(inteval)

                    break

                k+=1
    
    return board


            


