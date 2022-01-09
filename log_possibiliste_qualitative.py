# -*- coding: utf-8 -*-

import pandas as pd
from Res_absurde import infere

def get_st(BCPondere):
    """
    

    Parameters
    ----------
    BCPondere : str
        chemin vers BC ponderee.

        Fct qui permet la lecture d'une base de connaissance ponderee
        
    Returns
    -------
    st : list
        liste de st.

    """
    
    #lire la base ponderee
    df = pd.read_csv(BCPondere, header=None, names=["formule","seuil"])
    
    #trier les vals du plus grand au plus petit
    df.sort_values(by='seuil',  inplace=True)
    
    les_seuils = df.seuil.unique()
    
    #construire st
    
    st = []
    
    for s in les_seuils:
        st.append(df.loc[df.seuil == s])
        
    return st

def create_inter_file(list_st):
    """
    

    Parameters
    ----------
    list_st : list
        liste de st.


    fct qui cree un fichier intermediare qui concerne cette strate, pour l'utiliser avec SAT    

    Returns
    -------
    path : str
        chemin vers un fichier intermediare pour cette st.

    """
    
    
    
    liste_formules = []
    for df in list_st:
        #pour chaque df dans cette st
        # ajouter chaque formules dans la liste des formules
        liste_formules += df.formule.values.tolist()
    
    
    
    #determiner le nb de formules dans cette st
    nb_formules =len(liste_formules)
    
    
    
    #determiner le nb de var dans cette st
    variables = []
    
    for f in liste_formules:
        inter = f.split(" ")
        #changer le signe
        inter = [int(nb) if int(nb) > 0 else -int(nb) for nb in inter]
        
        for nb in inter:
            if nb not in variables:
                variables.append(nb)
                

        

    # prendre le max pour ne pas avoir de probleme
    
    nb_var = max(variables)
        
    print("nb var = ",nb_var)
    
    #creation di fiher
    ##
    ####
    ##
    first_line = "p cnf "+str(nb_var)+" "+str(nb_formules)
    
    #creer le contenue du fichier intermediaire
    contenu_fichier = first_line
    
    for f in liste_formules:
        contenu_fichier += "\n"+f
    
    contenu_fichier += "\n"
    
    #enregistrer le fichier
    
    path = "inter_st.cnf"
    
    with open(path, 'w') as f:
        f.write(contenu_fichier)
        
        
    return path

def get_negation(var_interet):
    """
    

    Parameters
    ----------
    var_interet : str
        le but sous format cnf.
        
        
        calcul la negation du but

    Returns
    -------
    str
        la negation du but sous format snf.

    """
    
    els = var_interet.split(" ")
    
    prem = int(els[0])
    
    prem = -prem
    
    els[0] = str(prem)
    
    return " ".join(els)
    
    
    
    

def inf_qualitative(st, var_interet):
    """
    

    Parameters
    ----------
    st : list of DataFrame
        liste des st.
    var_interet : str
        variable d'interet .
        
        
        Fct pour  l'inference possibiliste qualitative 

    Returns
    -------
    val : float
        seuil min de possibilite de la variable d interet.

    """
    
    #verifier si ca infere
    

    #si ce n'est pas le cas on retourne 0
    path = create_inter_file(st)
    if infere(path, var_interet):
        #calcul de la negation
        neg_var_interet = get_negation(var_interet)
        print("la base infere la variable d'intret...calcul du seuil minimum en cours...")
    
        l = 0
        u = len(st)
        
        while u-l > 1:

            r = int((l+u)/2)
            
            
            #create a temporary file for each st
            path = create_inter_file(st[r:u])

            
            #appel a SAT avec la strate et la negation de la var d interet
            if infere(path, neg_var_interet) == True:
                #si c'est consistenct
                u = r -1 
            else:
                #si ce n'est pas consistent
                l = r
            print("u == ",u)
            print("l == ",l)
        val = st[l].seuil.iloc[0]
        print("le seuil minimum de certitude de la variable d interet est : ",val)
    else:
        print("la base n infere pas "+var_interet)
        val = 0
    
    return val
    


def main(BCPondere, var_interet):
    
    #strate
    st = get_st(BCPondere)
    print(st)
    
    # inference
    val = inf_qualitative(st, var_interet)
    
    