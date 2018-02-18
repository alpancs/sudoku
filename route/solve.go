package route

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"os/exec"
	"strings"

	"github.com/go-chi/chi/middleware"
)

var Solve = newSolveHandler()

func newSolveHandler() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		workDir := "bin/" + strings.Replace(middleware.GetReqID(r.Context()), "/", "_", -1)
		err := prepareWorkDir(workDir)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		defer os.RemoveAll(workDir)

		input, err := getInput(r)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		output, err := solve(workDir, input)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.Write(output)
	}
}

func prepareWorkDir(workDir string) error {
	err := os.MkdirAll(workDir, 0777)
	if err != nil {
		return err
	}
	err = os.Link("bin/SudokuSolver2.py", workDir+"/SudokuSolver2.py")
	if err != nil {
		return err
	}
	err = os.Link("bin/minisat", workDir+"/minisat")
	return err
}

func getInput(r *http.Request) (*bytes.Buffer, error) {
	matrixRaw, err := ioutil.ReadAll(r.Body)
	if err != nil {
		return nil, err
	}

	var matrix [][]int
	err = json.Unmarshal(matrixRaw, &matrix)
	if err != nil {
		return nil, err
	}

	buffer := bytes.NewBuffer(nil)
	fmt.Fprintf(buffer, "%d\n", len(matrix))
	for i := 0; i < len(matrix); i++ {
		for j := 0; j < len(matrix); j++ {
			c := ' '
			if j == len(matrix)-1 {
				c = '\n'
			}
			fmt.Fprintf(buffer, "%d%c", matrix[i][j], c)
		}
	}
	return buffer, nil
}

func solve(workDir string, input io.Reader) ([]byte, error) {
	cmd := exec.Command("python2", "SudokuSolver2.py")
	cmd.Dir = workDir
	cmd.Stdin = input
	err := cmd.Run()
	if err != nil {
		return nil, err
	}
	return ioutil.ReadFile(workDir + "/result.txt")
}
