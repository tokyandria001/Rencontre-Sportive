import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

def affichage_graphique_matchs_simple(matchs,byes):
    # Création de la fenêtre principale
    root:tk.Tk = tk.Tk()
    root.title(f"Arbre des matchs de l'algoritme de selection simple")
    root.geometry(f"530x235")
    root.resizable(False, False)

    # Permet de mettre la fenêtre au premier plan 
    root.lift()
    root.attributes('-topmost', True)

    # Enlève le fait d'avoir la fenêtre au premier plan
    root.after(1,lambda: root.attributes('-topmost', False))

    # Configuration du style de la fenêtre principale
    style:ThemedStyle = ThemedStyle(root)
    style.set_theme("scidpink")
    
    # Création des onglets
    notebook_principal:ttk.Notebook = ttk.Notebook(root)
    
    # Reformatage des matchs par catégorie pour qu'ils ressemblent à ceux de l'algorithme d'Edmond
    matchs_par_categorie:list = matchs
    for i in range (0,len(matchs_par_categorie)):
        temp_dict = {}
        temp_list = list(matchs_par_categorie[i])
        temp_key = (matchs_par_categorie[i][0],matchs_par_categorie[i][1])
        temp_dict["matches"] = matchs_par_categorie[i][2]
        if temp_key in byes.keys():
            temp_dict["byes"] = byes[temp_key]
        temp_list.pop(2)
        temp_list.append(temp_dict)
        matchs_par_categorie[i] = tuple(temp_list)

    # Séparation de la catégorie d'âge et du poids pour permettre de faire un rangement par onglet d'âge puis par poids
    categorie_age_dict:dict = {}
    for cat_age, cat_poids, data in matchs_par_categorie:
        if cat_age not in categorie_age_dict:
            categorie_age_dict[cat_age] = []
        categorie_age_dict[cat_age].append((cat_poids, data))

    # Parcours des catégories d'âge        
    for cat_age, sous_cat  in categorie_age_dict.items() :
        # Création des onglets (catégorie d'âge)
        onglet_age:tk.Frame = tk.Frame(notebook_principal)
        notebook_principal.add(onglet_age, text=f"{cat_age}")

        #Création de du notebook secondaire (stocke les onglets catégorie de poids)
        notebook_secondaire:ttk.Notebook = ttk.Notebook(onglet_age)
        notebook_secondaire.pack(side="left",expand=True, fill="both")

        # Parcours des catégories de poids
        for cat_poids, data in sous_cat:
            # Création des onglets (catégorie de poids)
            onglet_poids:tk.Frame = tk.Frame(notebook_secondaire)
            onglet_poids.pack(padx=20, pady=20, fill="both", expand=True)   
            notebook_secondaire.add(onglet_poids, text=f"{cat_poids}")
            
            # Création d'un canvas pour la scrollbar
            canvas:tk.Canvas = tk.Canvas(onglet_poids)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Création d'une scrollbar
            scrollbar:ttk.Scrollbar = ttk.Scrollbar(onglet_poids, orient=tk.VERTICAL, command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Associer la scrollbar au canvas
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            
            # Création d'un frame dans le Canvas pour stocker les matchs
            frame_match:tk.Frame = tk.Frame(canvas)
            
            # Ajout de la frame dans le canvas
            canvas.create_window((0, 0), window=frame_match, anchor='nw')

            tk.Label(frame_match,text=" ",font=('Century Gothic','5')).pack()

            # Affichage des matchs
            if 'byes' in data.keys():
                tk.Label(frame_match, text="Bye : "+", ".join(data['byes']), font=('Century Gothic','10'), justify="center").pack()
            if data['matches'] != []:
                count:int = 0
                for match in data['matches']:
                    count += 1
                    j1:str = f"{match[0][0]} {match[0][1]} ({match[0][2]})"
                    j2:str = f"{match[1][0]} {match[1][1]} ({match[1][2]})"
                    tk.Label(frame_match, text=f"Match n°{count} : {j1} vs {j2}",font=('Century Gothic','10'), justify="center").pack()
            else:
                tk.Label(frame_match, text="Aucun match.",font=('Century Gothic','10'), justify="center").pack()

            # Obligation d'un espace à la fin de chaque regroupement de match car bug empêchant la scrollbar d'apparaître si trop peu de données
            if count < 7 :
                tk.Label(frame_match,text=" ",font=('Century Gothic','85')).pack()
            else :
                tk.Label(frame_match,text=" ",font=('Century Gothic','5')).pack()

            # Rafraichissement de la frame contenant les matchs
            frame_match.update_idletasks()

            # Rafraichissement de la scrollbar après l'ajout des matchs
            canvas.configure(scrollregion=canvas.bbox("all"))    

    notebook_principal.pack(expand=True, fill="both")
    
    # Affichage de la fenêtre principale
    root.mainloop()

        

        




