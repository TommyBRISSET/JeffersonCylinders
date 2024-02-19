from tkinter import *
import tkinter as tk
from JeffersonTkinterPartie2 import JeffersonDisplayPart2
import time
import blinking


class JeffersonDisplay:
    """Classe qui gère la première fenêtre d'affichage des cylindres de Jefferson
    avec la sélection de la clé et l'affichage des valeurs"""
    def __init__(self, filename: str):

        self.__filename = filename  # nom du fichier
        self.__root = tk.Tk()  # fenêtre principale
        self.__root.title("Cylindres de Jefferson")
        self.__root.configure(bg='black')
        self.__root.resizable(False, False)

        self.__frame0 = Frame(self.__root, bg="black")  # frame principale
        self.__frame0.grid(row=0, column=0)

        self.__cylindersArrange = []  # liste des cylindres arrangés pour affichage
        self.__valuesLabel = []  # liste des labels des valeurs
        self.__sizeElement = 0  # taille des éléments
        self.__cylinders = []  # liste des cylindres
        self.__orderValue = 0  # ordre de la valeur
        self.__keys = []  # liste des boutons clés
        self.__usedValues = []  # liste des valeurs utilisées (clés)
        self.__valuesLabels = []  # liste des labels des valeurs

        self.initializeCylinders(self.__filename)  # initialisation des cylindres
        self.update()  # initialisation de l'affichage
        self.__root.mainloop()

    def update(self):
        """Méthode qui initialise et met à jour l'affichage"""
        self.positionFrames()
        self.createKeyButtons()
        self.createLabel()
        self.createValuesLabel()

    def initializeCylinders(self, filename: str):
        """Méthode qui initialise la matrice des cylindres, la matrice
         des cylindres arrangés et la taille d'un cylindre"""
        with open(filename, 'r') as file:  # ouverture du fichier
            content = file.read()

        lines = content.split('\n')
        self.__cylinders = [line.split() for line in lines if line]  # liste des cylindres du fichier
        file.close()

        self.__cylindersArrange = self.transformMatrix(self.__cylinders)  # liste des cylindres arrangés pour affichage

        self.__sizeElement = len(self.__cylindersArrange[0])  # taille d'un cylindre

    @staticmethod
    def transformMatrix(matrix: list) -> list:
        """Méthode qui transforme une matrice pour un bon affichage"""
        newMatrix = []
        for i in range(len(matrix[0][0])):  # parcours de la matrice
            new_row = []
            for row in matrix:
                new_row.append(row[0][i])
            newMatrix.append(new_row)
        return newMatrix

    def positionFrames(self):
        """Méthode qui positionne les valeurs des cylindres dans des labels pour l'affichage"""
        for i in range(len(self.__cylindersArrange)):
            for j, letter in enumerate(self.__cylindersArrange[i]):
                label = Label(self.__frame0, text=letter, fg="red", bg="black", font=("Helvetica", 12))
                label.grid(row=i * 2, column=j)  # positionnement des labels

    def createLabel(self):
        """Méthode qui crée le label "'Enter the key'"""
        label = tk.Label(self.__frame0, text="Enter the key", font=('Helvetica', 12, 'bold'), bg='black', fg='red')
        label.grid(row=57, column=self.__sizeElement + 1, padx=2)

    def createKeyButtons(self):
        """Méthode qui crée les boutons pour les clés"""
        for index in range(self.__sizeElement):
            button = tk.Button(self.__frame0, text=f"{index + 1}",
                               font=('Helvetica', 12, 'bold'), bg='black', fg='red', border=0)  # création des boutons
            button.config(activebackground="black", activeforeground="red")
            button.bind("<Button-1>", self.clickButton)  # bind du bouton à la méthode clickButton
            button.grid(row=57, column=index, padx=2)
            self.__keys.append(button)

    def createValuesLabel(self):
        """Méthode qui crée les labels pour l'affichage des clés sélectionnées"""
        for index in range(self.__sizeElement):
            label = tk.Label(self.__frame0, text="", bg='black', fg='red', font=('Helvetica', 12, 'bold'))
            label.grid(row=58, column=index)
            self.__valuesLabels.append(label)

    def clickButton(self, event: Event):
        """Méthode qui gère le clic sur un bouton (clés)"""
        button = event.widget  # récupération du bouton
        value = button["text"]
        if value not in self.__usedValues:  # si la valeur n'est pas déjà utilisée
            self.__usedValues.append(value)
            index = len(self.__usedValues) - 1
            self.__valuesLabels[index].config(text=value)
            button.config(fg='grey')
            self.__root.update()  # apelle la fonction update
        self.checkKeysSelection()  # vérifie si toutes les clés ont été sélectionnées

    def checkKeysSelection(self):
        """Méthode qui vérifie si toutes les clés ont été sélectionnées"""
        if len(self.__usedValues) == self.__sizeElement:  # si toutes les clés ont été sélectionnées
            self.__usedValues = list(map(int, self.__usedValues))  # conversion des valeurs en int
            self.__orderValue = sorted(self.__usedValues)  # tri des valeurs
            self.windowsLoading()  # ouverture de la fenêtre de chargement
            self.reorderMatrix()  # réorganisation de la matrice

    def windowsLoading(self):
        """Méthode qui ouvre la fenêtre de chargement"""
        loading_window = tk.Toplevel(self.__root)
        largeur_principale = self.__root.winfo_width()  # Largeur de la fenêtre principale
        hauteur_principale = self.__root.winfo_height()  # Hauteur de la fenêtre principale

        x_principale = self.__root.winfo_rootx()  # Position horizontale de la fenêtre principale
        y_principale = self.__root.winfo_rooty()  # Position verticale de la fenêtre principale

        x_fenetre = x_principale  # Position horizontale de la fenêtre de chargement
        y_fenetre = y_principale  # Position verticale de la fenêtre de chargement

        loading_window.geometry(f"+{x_fenetre}+{y_fenetre}")  # Positionnement de la fenêtre de chargement
        loading_window.geometry(f"{largeur_principale}x{hauteur_principale}")  # Taille de la fenêtre de chargement
        loading_window.configure(bg='black')
        loading_window.overrideredirect(True)
        for i in range(8):
            loading_label = blinking.BlinkingLabel(loading_window, text="Loading", font=('Helvetica', 35, 'bold'),
                                                   fg='green', bg='black')
            loading_label.pack(pady=10)
        self.__root.update()
        time.sleep(1)  # pause de 1 seconde
        loading_window.destroy()  # fermeture de la fenêtre de chargement

    def clearWindow(self):
        """Efface le contenu de la fenêtre"""
        for widget in self.__frame0.winfo_children():  # parcours des widgets contenu dans le frame0
            widget.destroy()

    def reorderMatrix(self):
        """Méthode qui réordonne la matrice selon les clés sélectionnées"""
        newMatrix = [[0 for x in range(len(self.__cylindersArrange[0]))]
                     for y in range(len(self.__cylindersArrange))]  # création d'une nouvelle matrice

        for i, row in enumerate(self.__cylindersArrange):  # réordonne la matrice selon les clés sélectionnées
            for j, val in enumerate(row):
                newCol = self.__usedValues.index(self.__orderValue[j])
                newMatrix[i][newCol] = val
        self.clearWindow()
        # envoie la fenêtre, la frame, la matrice, la taille des éléments et l'ordre des clés à la classe
        # JeffersonDisplayPart2
        JeffersonDisplayPart2(self.__root, self.__frame0, newMatrix, self.__sizeElement, self.__usedValues)
