A simple Python cmd that allows solving matrix with basic operations.

I made this to use during my Linear Algebra class, allowing me to easily
write my assignments and notes in LaTeX without manually writing every
step of the solution.

All matrixes are entered using a syntax similar to LaTeX's format:
* Each column is delimited by an ampersand ("&").
* A new row is delimited by a double backslash ("\\\\").

#Commands

##matrix
Input a new matrix using a syntax similar to the content of a tabular
block in LaTeX. Sets this matrix as the working matrix.

##solve
Apply one or more operation(s) on the working matrix.

Valid operations are:
* LX(C): Multiply row X by coefficient C.
* LXY: Swap row X with row Y.
* LXY(C): Add row X multiplied by coefficient C to line Y.

##determinant
Return the determinant of the working matrix.

##undo
Undo the last action performed on the working matrix.

##latex
Output the working matrix and all operations applied to it as
LaTeX "bmatrix".

This allows easily writing the steps used to solve a matrix.

##help or man
Prints a short help message.
