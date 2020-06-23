def check_valid(board,boardinfo):
    rows = []
    cols = []
    cells = []

    for y in  range(len(boardinfo)):
        for x in range(len(boardinfo[y])):
            boardinfo[y][x] = True

    for i in range(len(board)):
       rows.append({}) 
       cols.append({}) 
       cells.append({}) 

    
    for y in range(len(board)):
        for x in range(len(board[i])):
            if(board[y][x]==0):
                continue

            cellIndex = y//3 * 3 + x//3

            row = rows[y]
            col = cols[x]
            cell = cells[cellIndex]

            number = str(board[y][x])
            if(number in row or number in col or number in cell):
                boardinfo[y][x] = False
                if(number in row):
                    pile = row[number][0]
                    boardinfo[pile[1]][pile[0]] = False
                if(number in col):
                    pile = col[number][0]
                    boardinfo[pile[1]][pile[0]] = False
                if(number in cell):
                    pile = cell[number][0]
                    boardinfo[pile[1]][pile[0]] = False
            else:
                row[number] = [[x,y]]
                col[number] = [[x,y]]
                cell[number] = [[x,y]]


    
