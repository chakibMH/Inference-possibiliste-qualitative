# -*- coding: utf-8 -*-

import pandas as pd
from Res_absurde import infere

def get_st(BCPondere="RCR_BASE.txt"):
    """
    

    Parameters
    ----------
    BCPondere : str
        chemin vers BC ponderee.

        Fct qui permet la lecture d'une base de connaissance ponderee, et retourne les 
        
        differente strates
        
    Returns
    -------
    st : list
        liste de strates.

    """
    
    #lire la base ponderee
    df = pd.read_csv(BCPondere, header=None, names=["formule","seuil"])
    #transformer la base en shema accpte par UBICAST
    c1 = df.apply(lambda x:to_cnf_form(x.formule),axis=1)
    
    df_new = pd.DataFrame(data = [c1.values, df.seuil.values])
    df_new = df_new.T
    df_new.columns=['formule','seuil' ]
    
    #trier les vals du plus grand au plus petit selon le poids
    df_new.sort_values(by='seuil',  inplace=True)
    
    les_seuils = df_new.seuil.unique()
    
    #construire straite
    
    st = []
    
    for s in les_seuils:
        st.append(df_new.loc[df_new.seuil == s])
        
        
    df.sort_values(by='seuil',  inplace=True)
    les_seuils = df_new.seuil.unique()
    st_affich = []
    for s in les_seuils:
        st_affich.append(df.loc[df.seuil == s])
        
    return st,st_affich

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
    
    print("elt "+els[0])
    
    o = els[0].replace("-","")
    
    o = ord(o)
    
    o = o-64
    
    prem = int(o)
    
    if "-" in els[0]:
        prem = - prem
    
    print("prem ",prem)
    
    prem = -prem
    
    print("-prem ",prem)
    
    els[0] = str(prem)
    
    return " ".join(els)
    

def to_cnf_form(exp_log):
    """
    

    Parameters
    ----------
    exp_log : str
        chaine representant la formule disjonctive.

        cette fct permet de faire une chaine de caracteres sous format cnf, acceptee par le solveur SAT,
        apartie d une chaine en lagage naturel

    Returns
    -------
    new_exp : str
        chaine sous format cnf avec des chiffres au lieu de noms de vars.

    """
    #enlever les espaces
    
    exp_log =exp_log.replace(" ","")
    
    #transformer au format cnf
    
    exp_log =exp_log.replace("or"," ")
    
    # tranformer les lettres en num
    
    new_exp = ""
    for c in exp_log:
        o = ord(c)
        if o >= 65 and o <= 90:
            #c un cractere
            o = o-64
            new_exp += str(o)
        else:
            new_exp+=c
            
    
    #rajouter le 0 a la fin
    new_exp += " 0"
    return new_exp
    
    

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

        val = st[l].seuil.iloc[0]
        print("le seuil minimum de certitude de la variable d interet est : ",val)
    else:
        print("la base n infere pas "+var_interet)
        val = 0
    
    return val
    

def first_step(BaseText):
    with open("RCR_BASE.txt","w") as f:
        f.write(BaseText)


def main(BCPondere, var_interet):
    
    #strate
    st,st_affich = get_st(BCPondere)
    print(st)
    print(st_affich)
    
    # inference
    val = inf_qualitative(st, var_interet)
    
    