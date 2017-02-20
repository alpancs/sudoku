from os import system
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello():
  return render_template("sudoku.html", lokal = request.remote_addr.startswith("127.0"))

@app.route("/solve", methods = ["POST"])
def solve():
  m = request.json
  with open("input_for_SudokuSolver", "w") as f:
    f.write(str(len(m)) + '\n')
    f.write('\n'.join( [' '.join([str(sel) for sel in baris]) for baris in m] ))
  system("python SudokuSolver2.py < input_for_SudokuSolver")
  with open("result.txt") as f:
    ret = f.read()
  system("rm input_for_SudokuSolver minisat.in minisat.out result.txt")
  return ret

if __name__ == "__main__":
  app.run(debug = True, host = "0.0.0.0")