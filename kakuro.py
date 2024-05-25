from colorama import Fore, Style

class CSP:
    def __init__(self):
        self.vars = {}
        self.constraints = {'Dif': [], 'SameDomain2': [], 'SameDomain3': [], 'NotRepeated': []}
        self.board = []
        self.sum = {}

    def Vars_Doms(self):
        rows = set(range(1, 10))
        cols = 'ABCDEFGHI'
        self.vars = {f"{c}{r}": rows.copy() for c in cols for r in rows}
        self.sum = {f"{c}{r}": {'vertical': None, 'horizontal': None} for c in cols for r in rows}

    def assign(self, var, value, assignment):
        assignment[var] = value

    def initBoard(self, nameFile):
        with open(nameFile, 'r') as file:
            lines = file.readlines()

        self.board = []
        for line in lines:
            row = line.strip().split(' ')
            row_values = []
            for value in row:
                if '\\' in value:
                    sub_values = value.split('\\')
                    row_values.append(sub_values)
                elif value == "W" or value == "N":
                    row_values.append(value)
                else:
                    row_values.append(int(value))
            self.board.append(row_values)

        return self.board

    def getDomain(self, values):
        for row in range(9):
            for col in range(9):
                cell = values[row][col]
                if isinstance(cell, list):
                    # Vertical sum
                    if cell[0] != 'N':
                        sum_value = int(cell[0])
                        for i in range(row + 1, 9):
                            if values[i][col] == "W":
                                self.sum[f"{chr(65+col)}{i+1}"]['vertical'] = sum_value
                            else:
                                break
                    # Horizontal sum
                    if cell[1] != 'N':
                        sum_value = int(cell[1])
                        for i in range(col + 1, 9):
                            if values[row][i] == "W":
                                self.sum[f"{chr(65+i)}{row+1}"]['horizontal'] = sum_value
                            else:
                                break

    def printDomains(self):
        print("Domain:")
        for key, value in self.sum.items():
            vertical = value['vertical']
            horizontal = value['horizontal']
            print(f"{key}: Vertical = {vertical}, \t Horizontal = {horizontal}")

    def printBoard(self):
        colsIndex = "ABCDEFGHI"  # Columnas
        numbers_color = Fore.GREEN
        letters_color = Fore.BLUE
        region_color = Fore.RED
        separator = "\t" + region_color + ("+" + "-" * 15) * 10 + "+" + Style.RESET_ALL

        print("KAKURO SOLVER:")
        print(separator)
        print("\t|\t/\t|\t" + letters_color + "A" + Style.RESET_ALL + "\t|\t" + letters_color + "B" + Style.RESET_ALL + "\t|\t" + letters_color + "C" + Style.RESET_ALL + "\t|\t" + letters_color + "D" + Style.RESET_ALL + "\t|\t" + letters_color + "E" + Style.RESET_ALL + "\t|\t" + letters_color + "F" + Style.RESET_ALL + "\t|\t" + letters_color + "G" + Style.RESET_ALL + "\t|\t" + letters_color + "H" + Style.RESET_ALL + "\t|\t" + letters_color + "I" + Style.RESET_ALL + "\t|")
        print(separator)
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print(separator)
            row_values = []
            for j in range(9):
                cell_value = self.board[i][j]
                if isinstance(cell_value, list):
                    row_values.append(Fore.BLACK + "\\".join(map(str, cell_value)) + Style.RESET_ALL)
                elif cell_value == "W":
                    row_values.append(Fore.BLACK + str(cell_value) + Style.RESET_ALL)
                elif cell_value == "N":
                    row_values.append(Fore.BLACK + str(cell_value) + Style.RESET_ALL)
                else:
                    row_values.append(numbers_color + str(cell_value) + Style.RESET_ALL)
            print("\t|\t" + letters_color + str(i + 1) + Style.RESET_ALL + "\t|\t" + "\t|\t".join(row_values) + "\t|")
        print(separator)

    def solve(self):
        assignment = {var: None for var in self.vars}
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        if self.is_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                self.assign(var, value, assignment)
                self.apply_reductions(assignment)
                result = self.backtrack(assignment)
                if result:
                    return result
                assignment[var] = None  # Backtrack
        return None

    def is_complete(self, assignment):
        return all(value is not None for value in assignment.values())

    def select_unassigned_variable(self, assignment):
        for var, value in assignment.items():
            if value is None:
                return var
        return None

    def order_domain_values(self, var, assignment):
        return list(self.vars[var])

    def is_consistent(self, var, value, assignment):
        for constraint in self.constraints['Dif']:
            if var in constraint:
                other = constraint[0] if var == constraint[1] else constraint[1]
                if other in assignment and assignment[other] == value:
                    return False
        return True
    
    def apply_reductions(self, assignment):
        for var, value in assignment.items():
            if value is not None:
                self.reduce_domain(var, value)

    def reduce_domain(self, var, value):
        for constraint in self.constraints['SameDomain2']:
            if var in constraint:
                other = constraint[0] if var == constraint[1] else constraint[1]
                if value in self.vars[other]:
                    self.vars[other].remove(value)

        for constraint in self.constraints['SameDomain3']:
            if var in constraint:
                other1, other2 = constraint[0], constraint[1]
                if value in self.vars[other1] and value in self.vars[other2]:
                    self.vars[other1].remove(value)
                    self.vars[other2].remove(value)

        for constraint in self.constraints['NotRepeated']:
            if var in constraint:
                for other in constraint:
                    if other != var and value in self.vars[other]:
                        self.vars[other].remove(value)

# Run
csp = CSP()
csp.Vars_Doms()
csp.initBoard('solve.txt')
csp.getDomain(csp.board)
csp.printBoard()
solution = csp.solve()
if solution:
    print("Solution:")
    csp.printBoard()
else:
    print("No solution found.")
csp.printDomains()
