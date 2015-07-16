Bernstein's Algorithm
========================================
This code implements **Bernsteins Synthesis Algorithm** in Python, 
the dependency is *tabulate*(https://bitbucket.org/astanin/python-tabulate) 
for printing table in beautiful format.

To run this program, simply import the algorithm :
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    from Algorithm.Bernstein import *
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*Step 1* : Create the algorithm :
~~~~~~~~~~~~~~~~~~~~
    algo = Bernstein()
~~~~~~~~~~~~~~~~~~~~
*Step 2* : Create a fuctional dependency list :
~~~~{.python}
    fds = FDList()
    # X1, X2 -> A, D
    fds.add_fd(FD(frozenset(['X1', 'X2']), frozenset(['A', 'D'])))
    # C, D -> X1, X2
    fds.add_fd(FD(frozenset(['C', 'D']), frozenset(['X1', 'X2'])))
    # A, X1 -> B
    fds.add_fd(FD(frozenset(['A', 'X1']), frozenset(['B'])))
    # B, X2 -> C
    fds.add_fd(FD(frozenset(['B', 'X2']), frozenset(['C'])))
    # C -> A
    fds.add_fd(FD(frozenset(['C']), frozenset(['A'])))
~~~~
*Step 3* : Compute the algorithm :
~~~~~~~~~~~~~~~~~~~~
    algo.compute(fds)
~~~~~~~~~~~~~~~~~~~~
*Step 4* : Print the relational schemas generated :
~~~~{.python}
    relations = algo.get_relations()
    print Bernstein.get_print_relations_info(relations)
~~~~
We will get 4 relations for the above functional dependencies :

    Relation    Keys                                              Attributes
    ----------  ------------------------------------------------  ------------
    R0          [frozenset(['X2', 'X1']), frozenset(['C', 'D'])]  set([])
    R1          [frozenset(['A', 'X1'])]                          set(['B'])
    R2          [frozenset(['X2', 'B'])]                          set(['C'])
    R3          [frozenset(['C'])]                                set(['A'])

- For detecting superfluous attribute in a specific relation, please check the method :
~~~~~~~~~~~~~~~~~~~~~~~~
    Bernstein.superfluous_attribute_detection_algorithm
~~~~~~~~~~~~~~~~~~~~~~~~
The detection algorithm is described in the paper : (https://www.comp.nus.edu.sg/~lingtw/ltk.pdf)

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/hugle/bernstein/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

