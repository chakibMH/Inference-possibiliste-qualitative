# -*- coding: utf-8 -*-
import re
import os


def clean_data(text):
    """retourne une liste de str sans les commentaires"""
    liste_elem = text.split("\n")
    
    liste_cld = [elt for elt in liste_elem if 
                 type(re.search(r"^[^c]+",elt)) != type(None)
                 and elt != ""]
    

    return liste_cld


def new_file(texte,provlit):
    
    """cette fct permet de creer un fichier temp 
        pour le solveur """
    
    liste_file = clean_data(texte)
    
    #inserer le nouveau literal
    
    liste_file.append(provlit)
    
    
    #modifier le nombre total de literaux
    
    first = liste_file[0]
    
    
    first_liste = re.compile(r"[\s]+").split(first)
    
    first_liste =list(filter(lambda x:x!='' , first_liste))
    

    
    nbactu = int(first_liste[-1])
    
    print("nbactu : ")
    print(nbactu)
    
    nbactu += 1
    
    nbactu = str(nbactu)
    
    first_liste[-1] = nbactu
    
    first = " ".join(first_liste)
    
    liste_file[0] = first
    
    new_text = "\n".join(liste_file)
    
    path = "temp_infere.cnf"
    
    with open(path,'w') as f:
        f.write(new_text)
        
    
    
    return path


    
def infere(file_BC,provlit):
    
    """cette fct permet d'utiliser le solveur SAT """
    
    with open(file_BC,'r') as f:
        texte = f.read()
        
     
    path = new_file(texte,provlit)
    
    os.system("ubcsat -alg saps -i "+path+" -solve > res_temp") 
    
    
    with open("res_temp","r") as f:
        result = f.read()
    
    os.remove(path)
    
    os.remove("res_temp")
    
    
    if 'No Solution found' in result:
        print("la base de connaisance est incoherante le litteral ne peut etre deduit")
        consist = False

    else:
        print("le litteral est une consequence logique de la BC")
        consist = True
        
        
    return consist
        
    
        
# if __name__ == "__main__":
#     infere("classic_BC\\BC-Zoo2.cnf","2 0")