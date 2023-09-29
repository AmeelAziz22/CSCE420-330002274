# Instruction
The blocksworld program made with python. 

You can run it with:

`python3 blocksworld.py [filename]`

In compute.cs.tamu.edu, running with python uses version 2.7 when python uses version 3.6. If you are on regular system or have anaconda prompt, etc. , you can run it with 

`python blocksworld.py [filename]`

There are optional Flags

`python3 blocksworld.py [filename] [print_each_iter] [max_iterations] [use_BFS]`

`filename` is the name of the file inside the probs folder
`print_each_iter` is if you want to print through iterations. Values is "Y" or "N". Default is Y. If you choose
N, it will still print every 50,000 in case it is a long program 


`max_iterations` is the number of the max iterations. Default is 1,000,000
`use_BFS` is if you want to use Breadth first traversal instead of Best First Search or A*. Values are Y or N Default is N

Some example command line

`python3 blocksworld.py probB05.bwp N 100000 Y`

`python3 blocksworld.py probB10.bwp`

`python blocksworld.py probB19.bwp N`

# Limitations

The program is able to solve all the problems. However, probB10.bwp takes over 100,000 iterations to solve the entire problem so I would reccomend keeping at default 1,000,000. The program also make take more iterations to complete but will find a shorter solution then the results in teh instruction. For B19, I got a planlen of 15 instead of 19. 