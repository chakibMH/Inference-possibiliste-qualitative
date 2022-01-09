# -*- coding: utf-8 -*-

import pandas as pd
from Res_absurde import infere

def get_st(BCPondere):
    
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
                print(nb)

        
    
    nb_var = max(variables)
    
    #ne pas compter le 0 le 0
    nb_var -= 1
    print("nb var = ",nb_var)
    
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
    
    l = 0
    u = len(st)
    
    while l < u:
        
        r = int((l+u)/2)
        
        #create a file for each st
        path = create_inter_file(st[r:u])
        
        if infere(path, var_interet):
            u = r -1 
        else:
            l = r
    
    
    
    