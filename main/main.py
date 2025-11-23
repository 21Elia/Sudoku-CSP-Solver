from sudoku import Sudoku

def printResult(result):
    for r in range(9):
        for c in range(9):
            cell = (r, c)
            print(str(result[cell]) + " ", end="")
        print("")
    
    pass

if __name__ == "__main__":
    # world's hardest Sudoku according to Arto Inkala
    hardest_sudoku = "800000000003600000070090200050007000000045700000100030001000068008500010090000400"
    
    # random Sudoku
    test_sudoku = "906870340051040706400006000068007003302010687100000000000002409700508162209004038"

    game = Sudoku(hardest_sudoku)
    board:str = game.board
    for i in range(len(board)):
        if(i % 9 == 0):
            print("")
        print(board[i] + " ", end="")


    print("\n\nSolving...\n")

    result = game.solve()

    if result: 
        print("Sudoku solved!\n")
        printResult(result)
    else:
        print("No solutionf found.")
