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
    

def inf_qualitative(st, var_interet):
    """
    

    Parameters
    ----------
    st : list of DataFrame
        liste des st.
    var_interet : str
        variable d'interet .
        
        
        Fct pour l'inference qualitative 

    Returns
    -------
    val : float
        seuil min de possibilite de la variable d interet.

    """
    
    #verifier si ca infere
    
    path = create_inter_file(st)
    
    if infere(path, var_interet):
    
        l = 0
        u = len(st)
        
        while l < u:
            
            r = int((l+u)/2)
            
            #create a temporary file for each st
            path = create_inter_file(st[r:u])
            
            #appel a SAT avec la straight et la negation de la var d interet
            if infere(path, var_interet):
                #si c'est consistanct
                u = r -1 
            else:
                #si ce n'est pas consistant
                l = r
        val = st[r].seuil.iloc[0]
    else:
        print("la base n infere pas "+var_interet)
        val = 0
    
    return val
    
def main(BCPondere, var_interet):
    
    #strate
    st = get_st(BCPondere)
    print(st)
    
    # inference
    #val = inf_qualitative(st, var_interet)
    
    