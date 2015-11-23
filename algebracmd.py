import cmd
import copy
import re

class AlgebraCmd(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.matrix = []
        self.path = []
        self.ops = []
        self.vars = []
        self.pr = True

    def do_matrix(self, matrix):
        """
        Input a new matrix using a syntax similar to the content of a tabular
        block in LaTeX.
        """
        num = "[[-]?\d+(\.?\d+)?|[-]?\d+/\d+]"
        pattern = "((" + num + "{1}[&]{1})*(" + num + "\\\\){1})*((" + num + "{1}[&]{1})*(" + num + "[\\\\]?){1}){1}"
        if re.match(pattern, matrix.strip()):
            self.matrix = self.strip_matrix([y for y in [x.strip().split('&') for x in matrix.split('\\\\')]])
            self.path = []
            self.ops = []
            if self.pr:
                self.print_matrix()
        else:
            print "***Error: Bad matrix format. Format should match: 'r1c1&r1c2...&r1cn\\r2c1&...&r2cn\\...rmc1&...&rmcn', meaning column values are separated with '&' and new rows are prefixed with '\\\\'***"

    def do_solve(self, op):
        """
        Apply one or more operation(s) on the working matrix.

        Valid operations are:
        - LX(C): Multiply row X by coefficient C.
        - LXY: Swap row X with row Y.
        - LXY(C): Add row X multiplied by coefficient C to line Y.
        """
        ops = [x.strip() for x in op.split(",")]
        for x in ops:
            if re.match("L[0-9]{2}\([[-]?\d+(\.?\d+)?|[-]?\d+/\d+]\)", x):
                self.path.append(copy.deepcopy(self.matrix))
                lines = [int(x[1])-1, int(x[2])-1]
                raw_coeff = x[x.index("(")+1:x.index(")")]
                self.ops.append("L_{" + str(lines[0]+1) + "," + str(lines[1]+1) + "}(" + raw_coeff + ")")
                if "." in raw_coeff:
                    coeff = float(raw_coeff)
                elif "/" in raw_coeff:
                    div = raw_coeff.split("/")
                    coeff = float(div[0].strip())/float(div[1].strip())
                else:
                    coeff = int(raw_coeff)
                self.matrix[lines[0]] = [(a + coeff * b) for a,b in zip(self.matrix[lines[0]], self.matrix[lines[1]])]
            elif re.match("L[0-9]{1}\([[-]?\d+(\.?\d+)?|[-]?\d+/\d+]\)", x):
                self.path.append(copy.deepcopy(self.matrix))
                line = int(x[1])-1
                raw_coeff = x[x.index("(")+1:x.index(")")]
                self.ops.append("L_" + str(line+1) + "(" + raw_coeff + ")")
                if "." in raw_coeff:
                    coeff = float(raw_coeff)
                elif "/" in raw_coeff:
                    div = raw_coeff.split("/")
                    coeff = float(div[0].strip())/float(div[1].strip())
                else:
                    coeff = int(raw_coeff)
                self.matrix[line] = [coeff * a for a in self.matrix[line]]
            elif re.match("L[0-9]{2}", x):
                self.path.append(copy.deepcopy(self.matrix))
                lines = [int(x[1])-1, int(x[2])-1]
                self.ops.append("L_{" + str(lines[0]+1) + "," + str(lines[1]+1) + "}")

                temp = self.matrix[lines[0]]
                self.matrix[lines[0]] = self.matrix[lines[1]]
                self.matrix[lines[1]] = temp
            else:
                print "***Argument format error. 'solve' argument must be of form: '[L[0-9]{2}[([[-]?\d+(\.?\d+)?|[-]?\d+/\d+])]?|L[0-9]{1}([[-]?\d+(\.?\d+)?|[-]?\d+/\d+])]'***"
                print "***Examples: L31(1), L23, L31(1/2), L41(-2), L4(3), L25(-1/50)***"
                print "***Halting operation execution.***"
                break
        if self.pr:
            self.print_matrix()

    def do_determinant(self):
        """
        Return the determinant of the working matrix.
        """
        print self.determinant(copy.deepcopy(self.matrix))

    def do_undo(self, *args):
        """
        Undo the last action performed on the working matrix.
        """
        if len(self.path) > 0:
            self.matrix = self.path.pop()
            del self.ops[-1]
            if self.pr:
                print "Previous action undone."
                self.print_matrix()
        else:
            print "***Error: There is nothing to undo.***"

    def do_latex(self, dest):
        """
        Output the working matrix and all operations applied to it as
        LaTeX "bmatrix".

        This allows easily writing the steps used to solve a matrix.
        """
        output = ""
        for op,matrix in zip(self.ops, self.path):
            output += "$\\begin{bmatrix}\n"
            for row in matrix:
                treated = map(self.treat, row)
                string = map(str, treated)
                output += " & ".join(string) + "\\\\\n"
            output += "\\end{bmatrix}$\n"
            output += "$" + op + " \\sim$\n"

        output += "$\\begin{bmatrix}\n"
        for row in self.matrix:
            treated = map(self.treat, row)
            string = map(str, treated)
            output += " & ".join(string) + "\\\\\n"
        output += "\\end{bmatrix}$"
        if len(dest) > 0:
            poutput
        print output

    def do_let(self, args):
        if re.match("[a-zA-Z]+=[[[-]?\d+(\.?\d+)?|[-]?\d+/\d+]|[a-zA-Z]", args):
            vals = args.split("=")
            self.substitute(vals[0], vals[1])

    def do_man(self, *args):
        self.do_help(args)

    def do_help(self, *args):
        print "Valid functions:\n"
        print "'matrix <args>' initiates the working matrix. Use the latex format, with elements in a row separated by '&' and new rows delimited by '\\\\' Example: '1&2&3\\4&5&6\\7&8&9'. Note that variables are NOT supported.\n"
        print "'solve <args>' applies the given operations to the working matrix. Use the same format seen in class: 'L<row><row2>(<coeff>)', 'L<row1><row2>' or 'L<row>((<coeff>)'. To chain many operations, separate them with commas.\n"
        print "'latex' prints the transformations as a 'latex' formatted document. This allows you to create pdf files documenting the steps to the solution.\n"
        print "'exit' closes the program.\n"

    def do_exit(self, *args):
        print "Exiting program."
        return True

    def treat(self, val):
        if val % 1 == 0:
            return int(val)
        else:
            return val

    def determinant(self, matrix):
        """
        Utility method to calculate the determinant of the working matrix.
        """
        j = 0
        determinant = 0
        if len(matrix) != len(matrix[0]):
            return -1
        if len(matrix) == 2 and len(matrix[0]) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        else:
            for i in len(matrix):
                determinant += matrix[i][j] * self.determinant(self.sub_matrix(copy.deepcopy(matrix), i, j))
            return determinant

    def sub_matrix(self, matrix, line, col):
        matrix.pop(line)
        for r in matrix:
            r.pop(col)
        return matrix

    def print_matrix(self):
        print 'Working matrix is now:'
        for row in self.matrix:
            print row

    def strip_matrix(self, matrix):
        stripped = []
        for row in matrix:
            if row[0] != '':
                current = []
                for x in row:
                    if re.match("[[-]?\d+(\.?\d+)?|[-]?\d+/\d+]", x):
                        if "." in x:
                            current.append(float(x.strip()))
                        elif "/" in x:
                            div = x.split("/")
                            current.append(float(div[0].strip())/float(div[1].strip()))
                        else:
                            current.append(int(x.strip()))
                if len(current) > 0:
                    stripped.append(current)
        return stripped

if __name__ == '__main__':
    AlgebraCmd().cmdloop()
