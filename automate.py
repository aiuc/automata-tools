
from transition import *
from state import *
import os
import copy
from itertools import product
from automateBase import AutomateBase

# gr8 etudiants : Maimouna Abdelrahman et Ossama Elliethy 

class Automate(AutomateBase):
        
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs


    def succ (self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """

        successeurs = []
        # s: States
        
        for state in listStates:
            tmp = self.succElem(state, lettre)
            for state in tmp:
                if state not in successeurs :
                    successeurs.append(state)
        return successeurs



    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """

    @staticmethod
    def accepte(auto,mot) :
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """
        
        
        init = auto.getListInitialStates()
        
        for l in mot:
            init = auto.succ(init, l)
        for s in init:
            if s.fin:
                return True
            
        return False

""""
        final = auto.getListFinalStates()
        init = auto.getListInitialStates()
        
        for l in mot:
            init = auto.succ(init, l)
        for s in init:
            if s in final:
                return True
            else:
                return False
""""
""""
        final = auto.getListFinalStates()
        init = auto.getListInitialStates()
        
        for l in mot:
            init = auto.succ(init, l)
        for s in init:
            return s in final:
                
""""
    @staticmethod
    def estComplet(auto,alphabet) :
        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """
          
        for state in auto.listStates:
        	for a in alphabet:
        		if (auto.succElem(state,a)==[]):
        			return False
        return True

        
    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """


        initialState=auto.getListInitialStates()
        if (len(initialState) != 1):
            return False
        
        for etat in auto.listStates:
            listeTransitions = auto.getListTransitionsFrom(etat)
            label = []
            for t in listeTransitions:
                if t.etiquette in label:
                    return False
                else:
                    label.append(t.etiquette)
        return True
        

       
    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """
        
        autoComplet = copy.deepcopy(auto)
        if(auto.estComplet(auto, alphabet)):
            return autoComplet
        else:
            etatPuit = State (len(auto.listStates)+1, False, False, "rejected")

            for etat in autoComplet.listStates:
                for lettre in alphabet:
                    if(autoComplet.succElem(etat, lettre)== []):
                        autoComplet.addTransition(Transition(etat, lettre, etatPuit))
        return autoComplet

       

    @staticmethod
    def determinisation(auto) :
        """ Automate -> Automate
        rend l'automate déterminisé d'auto
        """
        if ( Automate.estDeterministe(auto) ) :
            return auto
        alphabet = auto.getAlphabetFromTransitions()
        worklist : List[ set[ State ] ] = [ set( auto.getListInitialStates() ) ]
        newlist : List[ set[ State ] ] = [ set( auto.getListInitialStates() ) ]
        newTrans : List[Transition] = []

        while (worklist) : 
            stateSet = worklist[0]
            worklist.remove(stateSet)

            for c in alphabet :
                succ = set(auto.succ(stateSet,c))

                if succ not in newlist :
                    newlist.append(succ)
                    worklist.append(succ)

                #si tout est initial donc b true
                b = False
                s = "{ "
                for e in stateSet :
                    s += e.label+" "
                    b = b and e.init
                s+= "}"
                state1 = State(newlist.index(stateSet),b,State.isFinalIn(stateSet),s)

                s = "{ "
                for e in succ :
                    s += e.label+" "
                s+= "}"
                state2 = State(newlist.index(succ),False,State.isFinalIn(succ),s)

                newTrans.append( Transition(state1,c,state2) )

        return Automate(newTrans)
        
    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        at = Automate.determinisation(auto)
        at = Automate.completeAutomate(at, alphabet)
        retAt = Automate([])

        for transition in at.listTransitions:
            tr = Transition(
                        State(transition.stateSrc.id,
                              transition.stateSrc.init,
                              not transition.stateSrc.fin),
                        transition.etiquette,
                        State(transition.stateDest.id,
                              transition.stateDest.init,
                              not transition.stateDest.fin)
                )
            retAt.addTransition(tr)

        return retAt

        """    
         def complementaire(auto,alphabet):
        
        autoComplementaire = Automate.completeAutomate(auto, alphabet) 
        autoComplementaire = Automate.determinisation(auto)
        for etat in autoComplementaire.listStates:
            if (etat.fin):
                etat.fin = False
            else:
                etat.fin = True
        return autoComplementaire 
   """

    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        T = []
        done = []
        # Concatenons les etats initiaux de auto1 et auto2
        to_do = list(product(auto0.getListInitialStates(), auto1.getListInitialStates()))

        Dico = dict()

        i = 0

        alphabet = auto0.getAlphabetFromTransitions()

        while to_do != []:
            for l in alphabet:
                # Est ce qu'un des deux etats du couple a-t-il une transition vers un autre etat avec la lettre l
                if auto0.succElem(to_do[0][0], l) != [] and auto1.succElem(to_do[0][1], l) != []:
                    # Si oui on nomme ce couple todo
                    todo = to_do[0]
                    # On concatene les listes d'etats vers lesquels le couple peut se diriger
                    succ = list(product(auto0.succElem(
                        to_do[0][0], l), auto1.succElem(to_do[0][1], l)))
                    # On parcours cette liste via couple
                    for couple in succ:
                        # Est-ce que ce couple est dans le dico ?
                        if str(todo) in Dico:
                            # Est-ce que la liste des etats vers lesquels le couple peut se diriger est dans le dico ?
                            if str(couple) in Dico:
                                # Si oui on ajoute alors les transitions du couple vers les etats de l'autre couple
                                T.append(Transition(
                                    Dico[str(todo)], l, Dico[str(couple)]))
                            else:
                                # Si non, on cree l'etat et on ajoute ses transitions
                                s = State(
                                    i, couple[0].init and couple[1].init, couple[0].fin and couple[1].fin)
                                T.append(Transition(Dico[str(todo)], l, s))
                                # Puis on ajoute finalement le couple vers lequel le couple todo pouvait se diriger
                                Dico[str(couple)] = s
                                i += 1
                        else:
                            # Si non, on cree l'etat todo et on l'ajoute au dico
                            s = State(
                                i, todo[0].init and todo[1].init, todo[0].fin and todo[1].fin)
                            Dico[str(todo)] = s
                            i += 1
                            # Ici on recommence pour verifier si le couple vers lequel vont todo est deja dans Dico puis on ajoute les transitions.
                            if str(couple) in Dico:
                                T.append(Transition(
                                    Dico[str(todo)], l, Dico[str(couple)]))
                            else:
                                s = State(
                                    i, couple[0].init and couple[1].init, couple[0].fin and couple[1].fin)
                                T.append(Transition(Dico[str(todo)], l, s))
                                Dico[str(couple)] = s
                                i += 1
                        # Si le couple vers lequel va todo n'est pas dans la liste to_do et n'est pas fini, alors on l'ajoute a to_do puis on va la traiter.
                        if couple not in to_do and couple not in done:
                            to_do.append(couple)
            done.append(to_do[0])
            to_do.remove(to_do[0])

        return Automate(T)

    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        T = []
        done = []
        # On concatene les états initiaux de auto1 et auto2
        to_do = list(product(auto0.getListInitialStates(), auto1.getListInitialStates()))

        Dico = dict()

        i = 0

        alphabet = auto0.getAlphabetFromTransitions()

        while to_do != []:
            for l in alphabet:
                # Est ce qu'un des deux états du couple à-t-il une transition vers un autre état avec la lettre l
                if auto0.succElem(to_do[0][0], l) != [] and auto1.succElem(to_do[0][1], l) != []:
                    # Si oui on nomme ce couple todo
                    todo = to_do[0]
                    # On concatène les listes d'états vers lesquels le couple peut se diriger
                    succ = list(product(auto0.succElem(
                        to_do[0][0], l), auto1.succElem(to_do[0][1], l)))
                    # On parcours cette liste via couple
                    for couple in succ:
                        # Est-ce que ce couple est dans le dico ?
                        if str(todo) in Dico:
                            # Est-ce que la liste des états vers lesquels le couple peut se diriger est dans le dico ?
                            if str(couple) in Dico:
                                # Si oui on ajoute alors les transitions du couple vers les états de l'autre couple
                                T.append(Transition(
                                    Dico[str(todo)], l, Dico[str(couple)]))
                            else:
                                # Si non, on crée l'état et on ajoute ses transitions
                                s = State(
                                    i, couple[0].init or couple[1].init, couple[0].fin or couple[1].fin)
                                T.append(Transition(Dico[str(todo)], l, s))
                                # Puis on ajoute finalement le couple vers lequel le couple todo pouvait se diriger
                                Dico[str(couple)] = s
                                i += 1
                        else:
                            # Si non, on crée l'état todo et on l'ajoute au dico
                            s = State(
                                i, todo[0].init or todo[1].init, todo[0].fin or todo[1].fin)
                            Dico[str(todo)] = s
                            i += 1
                            # Ici on recommence pour verifier si le couple vers lequel vont todo est déjà dans Dico puis on ajoute les transitions.
                            if str(couple) in Dico:
                                T.append(Transition(
                                    Dico[str(todo)], l, Dico[str(couple)]))
                            else:
                                s = State(
                                    i, couple[0].init and couple[1].init, couple[0].fin and couple[1].fin)
                                T.append(Transition(Dico[str(todo)], l, s))
                                Dico[str(couple)] = s
                                i += 1
                        # Si le couple vers lequel va todo n'est pas dans la liste to_do et n'est pas fini, alors on l'ajoute à to_do puis on va la traiter.
                        if couple not in to_do and couple not in done:
                            to_do.append(couple)
            done.append(to_do[0])
            to_do.remove(to_do[0])

        return Automate(T)

   

 
        
       
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        alphabet = auto.getAlphabetFromTransitions()
        newAuto = copy.deepcopy(auto)
        listFinal = newAuto.getListFinalStates()
        listInit = newAuto.getListInitialStates()

        for final in listFinal :
            for init in listInit :
                for c in alphabet :
                    init.fin = True
                    newAuto.addTransition( Transition(final,c,init) )

        return newAuto