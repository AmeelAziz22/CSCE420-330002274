Enter instructions and requirements for running your code here.

There are two python files which you can run: convCNF.py and DPLL.py

you can do: 

`python3 convCNF.py sammy.kb -DIMACS > sammy.cnf` 

which runs the convCNF.py file and converts the sammy.kb into a .cnf file written in the -DIMACS notation. `-DIMACS` argument is used to specify the file into DIMACS notation necessary to run the DPLL algorithm

to simply run the DPLL.py, you need atleast to specify the .cnf file 
`python3 DPLL.py mapcolor.cnf` will run the DPLL algorithm on mapcolor.cnf

you can also add in facts in the command line writing it after you specify the file:
`python3 DPLL.py -VG WAB`
this specifies the VG variable to be false and the WAB variable to be positive

I also added two hueristics: Unit Clause Heuristic (+UCH) and Pure Symbol Heuristic(+PSH). I know I wasn't supposed to do PSH but I didn't know till after I made it. 

to run these heuristics, use the argument +UCH or +PSH which will turn on the heuristic (and obviosly won't be added to the knowledge base)

`python3 DPLL.py 6queens.cnf +UCH`

After running your program, it should print out the path of the DPLL algorithm, printing what it tries or forces variables to be, when the algorithm backtracks, and the solution if satisfiable or if it is not satisfiable. You can see these in all the results textfiles in this repo. 

There are no constaints. Everything works as long as command line arguments are written correctly.