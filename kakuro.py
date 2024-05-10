
import copy
import itertools
from colorama import Fore, Style

class CSP:
    def __init__(self):
        self.vars = {}
        self.constraints ={'Dif':[], 'SameDomain2': [], 'SameDomain3': [], 'NotRepeated': []}

    def Vars_Doms(self):
        rows = set(range(1, 10))
        cols = 'ABCDEFGHI'
        self.Vars = {f"{c}{r}": rows.copy() for c in cols for r in rows}

    def assign(self, var, value, assignment):
        assignment[var] = value

    def initBoard(self, nameFile):
      with open(nameFile, 'r') as file:
        lines = file.readlines()
      
      board = []
      for line in lines:
        row = line.strip().split(' ')
        # Se separan los objetos internos que tengan \ como separador
        for i in range(len(row)):
          if '\\' in row[i]:
            row[i] = row[i].split('\\')
        board.append(row)
      
      return board
    
    # Restricciones de las filas.

    def printBoard(self, board):
      colsIndex = "ABCDEFGHI" # Columnas
      numbers_color = Fore.GREEN
      letters_color = Fore.BLUE
      region_color = Fore.RED
      separator = "\t" + region_color + ("+" + "-" * 15 ) * 10 + "+" + Style.RESET_ALL

      print("KAKURO SOLVER:")
      print(separator)
      print("\t|\t/\t|\t" + letters_color + "A" + Style.RESET_ALL + "\t|\t" + letters_color + "B" + Style.RESET_ALL + "\t|\t" + letters_color + "C" + Style.RESET_ALL + "\t|\t" + letters_color + "D" + Style.RESET_ALL + "\t|\t" + letters_color + "E" + Style.RESET_ALL + "\t|\t" + letters_color + "F" + Style.RESET_ALL + "\t|\t" + letters_color + "G" + Style.RESET_ALL + "\t|\t" + letters_color + "H" + Style.RESET_ALL + "\t|\t" + letters_color + "I" + Style.RESET_ALL + "\t|")
      print(separator)
      for i in range(9):
        if i % 3 == 0 and i != 0:
          print(separator)
        row_values = []
        for j in range(9):
          cell_value = board[i][j]
          if isinstance(cell_value, list):
            row_values.append(Fore.BLACK + "\\".join(map(str, cell_value)) + Style.RESET_ALL)
          elif 'N' in str(cell_value):
            row_values.append(Fore.BLACK + str(cell_value) + Style.RESET_ALL)
          else:
            row_values.append(numbers_color + str(cell_value) + Style.RESET_ALL)
        print("\t|\t" + letters_color + str(i+1) + Style.RESET_ALL + "\t|\t" + "\t|\t".join(row_values) + "\t|")
      print(separator)



#run
csp = CSP()
csp.Vars_Doms()
board = csp.initBoard('solve.txt')
csp.printBoard(board)
