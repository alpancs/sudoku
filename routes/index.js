var express = require('express')
var fsp = require('fs-promise')
var child_process = require('child-process-promise')

var router = express.Router()

/* GET home page. */
router.get('/', (req, res) => {
  res.render('index')
})

router.post('/solve', (req, res) => {
  let matrix = req.body
  let input_file = 'sudoku_solver_input'
  let input_raw = [matrix.length, ...matrix.map(line => line.join(' '))].join('\n')
  fsp.writeFile('bin/'+input_file, input_raw).catch(console.log)

  child_process.exec(`python SudokuSolver2.py < ${input_file}`, {cwd: 'bin'})
  .then(() => fsp.readFile('bin/result.txt'))
  .then(result_raw => {
    res.send(result_raw)
    for (file_name of ['bin/'+input_file, 'bin/minisat.in', 'bin/minisat.out', 'bin/result.txt'])
      fsp.unlink(file_name).catch(console.log)
  })
  .catch(console.log)
})

module.exports = router
