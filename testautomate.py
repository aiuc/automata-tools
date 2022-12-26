from automate import *
from transition import *
from state import *
import os
import copy
from itertools import product
from automateBase import AutomateBase

s1 = State(0, True, False)
s2 = State(1, False, True)

# t1 : Transition
t1 = Transition(s1,"a",s1)

# t2 : Transition
t2 = Transition(s1,"a",s2)

# t3 : Transition
t3 = Transition(s1,"b",s2)

# t4 : Transition
t4 = Transition(s2,"a",s2)

# t5 : Transition
t5 = Transition(s2,"b",s2)

# liste : List[Transition]
liste = [t1,t2,t3,t4,t5]

## cr ́eation de l’automate
# aut : Automate

s3 = State(0, True, False)
aut = Automate(liste, [s1,s2])
#aut.show("")
#aut=Automate.creationAutomate("auto.txt")
#aut.show("fichier")

t = Transition(s1,"a",s2)
#print(aut)
aut.removeTransition(t)
aut.removeTransition(t1)
#print(aut)
aut.addTransition(t1)
aut.addTransition(t)
#print(aut)
#aut.removeState(s1)
#print(aut)
#aut.addState(s1)
print(aut.getListTransitionsFrom(s1))

#print(aut)
#aut.show("fishiersanst")

