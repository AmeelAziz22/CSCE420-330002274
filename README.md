# Ameel Aziz - 330002274

# Course Setup 


- You will need a github account, and a basic understanding of git
- You will need python3 or C++
- You will also need the following python packages: 
- Make sure your python has future, heapq or queue.PriorityQueue

Once you have a github account
1. Go to https://github.com/EndlessDebugger/420_template
2. Click "Use Template -> Create a new repository" (use the name: CSCE420-`Your netid here`)
3. Make sure to make the repository private
4. Go to settings, Collaborators, Add people, and add `ioerger`, and `EndlessDebugger`

<img width="1186" alt="Screen Shot 2023-01-31 at 1 57 38 PM" src="https://user-images.githubusercontent.com/17692058/215868976-9207346a-973e-43d4-8b39-6c60b0be2611.png">


5. Then use git to clone your repository somewhere on your computer

## When submitting PAs, make sure to:
1. Create & push a git tag using the following command
git tag "pa1" && git push origin "pa1"

2. If you want to resubmit, simply delete the old git tag, and then recreate it on your latest
commit. `git push --delete origin "pa1" && git tag --delete "pa1"`

# PA1 Instructions
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

`python3 blocksworld.py probB19.bwp N`

# Limitations

The program is able to solve all the problems. However, probB10.bwp takes over 100,000 iterations to solve the entire problem so I would reccomend keeping at default 1,000,000. The program also make take more iterations to complete but will