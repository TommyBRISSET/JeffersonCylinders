from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk
from threading import Thread
from playsound import playsound
import blinking  # blinking.py
import copy
import os


class JeffersonDisplayPart2:

    def __init__(self, root, frame: Frame, cylinders: list, sizeElement: int, key: list):
        self.__cylindersArrange = cylinders  # liste des cylindres arrangés pour affichage
        self.__key = key  # clé
        # copie profonde de la liste des cylindres arrangés pour fonction reset
        self.__resetCylindersArrange = copy.deepcopy(self.__cylindersArrange)
        self.__selectedColumn = 0  # colonne sélectionnée
        self.__sizeElement = sizeElement  # taille des éléments
        self.__buttons = []  # liste des boutons pour nettoyage de l'affichage
        self.__total = 0  # total des lettres a crypter
        self.__songPlayed = True  # booléen qui permet de savoir si le son est autorisé ou non

        self.__root1 = root  # fenêtre principale

        self.__frame0 = frame  # frame principale
        self.__frame0.grid(row=0, column=0)

        self.__root1.bind('<Up>', self.upKey)  # bind des touches
        self.__root1.bind('<Down>', self.DownKey)
        self.__root1.bind('<Left>', self.leftKey)
        self.__root1.bind('<Right>', self.rightKey)
        self.__root1.bind('<Return>', self.CloseProgram)

        self.update()  # initialisation de l'affichage
        self.displayAllButtons()  # affichage des boutons UP (flèches vers le haut) et DOWN (flèches vers le bas)
        self.displayFinishButton()  # affichage du bouton FINISH
        self.displayInfoButton()  # affichage du bouton HOW IT WORKS
        self.displaySaveButton()  # affichage du bouton SAVE CYLINDERS
        self.displayLoadButton()  # affichage du bouton LOAD CYLINDERS
        self.displayAutoButton()  # affichage du bouton AUTO CLEAR
        self.displayEncryptButton()  # affichage du bouton AUTO CIPHER
        self.displayResetButton()  # affichage du bouton RESET CYLINDERS
        self.displaySoundButton()  # affichage du bouton SOUND CUT/PUT
        self.displayKey()  # affichage de la clé
        self.__root1.mainloop()

    def upKey(self, event: Event):
        """Méthode qui permet de déplacer la sélection (colonne) vers le haut (1 cran)"""
        self.updateColumnUp(self.__selectedColumn)

    def DownKey(self, event: Event):
        """Méthode qui permet de déplacer la sélection (colonne) vers le bas (1 cran)"""
        self.updateColumnDown(self.__selectedColumn)

    def leftKey(self, event: Event):
        """Méthode qui permet de déplacer la sélection vers la gauche"""
        if 1 <= self.__selectedColumn < self.__sizeElement:
            self.delPosition()
            self.__selectedColumn -= 1
            self.position()

    def rightKey(self, event: Event):
        """Méthode qui permet de déplacer la sélection vers la droite"""
        if 0 <= self.__selectedColumn < self.__sizeElement - 1:
            self.delPosition()
            self.__selectedColumn += 1
            self.position()

    def position(self):
        """Méthode qui permet de mettre d'avoir un indicateur de la colonne sélectionée"""
        if 0 <= self.__selectedColumn < self.__sizeElement:  # si la colonne sélectionnée est dans la grille
            self.__label = Label(self.__frame0, text="^", fg="red", bg="black", font=("Helvetica", 12))
            self.__label.grid(row=52, column=self.__selectedColumn)

    def delPosition(self):
        """Méthode qui permet de supprimer l'indicateur de la colonne sélectionée"""
        if 0 <= self.__selectedColumn < self.__sizeElement:  # si la colonne sélectionnée est dans la grille
            self.__label = Label(self.__frame0, text="", fg="red", bg="black", font=("Helvetica", 12))
            self.__label.grid(row=52, column=self.__selectedColumn)

    def update(self):
        """met a jour l'algorithme"""
        self.position()
        self.displayCylindersWithLines()

    def clearWindow(self):
        """Efface la fenêtre"""
        for widget in self.__frame0.winfo_children():  # on parcourt les widgets de la frame0
            # si le widget est un label ou un bouton et qu'il n'est pas dans la liste des boutons
            if isinstance(widget, (Label, Button)) and widget not in self.__buttons:
                widget.destroy()  # on le détruit

    def displayCylindersWithLines(self):
        """Affiche les cylindres et des lignes pour repérer la ligne de chiffrement et de déchiffrement du texte"""
        for i in range(len(self.__cylindersArrange)):
            for j, letter in enumerate(self.__cylindersArrange[i]):
                label = Label(self.__frame0, text=letter, fg="red", bg="black", font=("Helvetica", 12))
                label.grid(row=i * 2, column=j)

            # ligne pour séparer les ligne de chiffrement et de déchiffrement du texte
            if i == 8 or i == 9 or i == 14 or i == 15:
                total_width = self.__sizeElement * 28  # largeur totale de la 'ligne' (en pixels)
                line = Frame(self.__frame0, height=2, width=total_width, bg="red")  # création de la ligne
                line.grid(row=i * 2 + 1, column=0, columnspan=len(self.__cylindersArrange[i]))

            if i == 9:  # label pour afficher "CLEAR"
                clearLabel = Label(self.__frame0, text="CLEAR", fg="red", bg="black", font=("Helvetica", 12))
                clearLabel.grid(row=i * 2, column=len(self.__cylindersArrange[i]))

            if i == 15:  # label pour afficher "CIPHER"
                cipherLabel = Label(self.__frame0, text="CIPHER", fg="red", bg="black", font=("Helvetica", 12))
                cipherLabel.grid(row=i * 2, column=len(self.__cylindersArrange[i]))

    def displayAllButtons(self):
        """Affiche les boutons UP et DOWN (flèches vers le haut et vers le bas)"""
        upImage = Image.open("asset/UP.png")  # image pour le bouton UP
        upPhoto = ImageTk.PhotoImage(upImage)  

        for i in range(len(self.__cylindersArrange[0])):  # affiche les boutons UP
            button = Button(self.__frame0, image=upPhoto, fg="red", bg="black", border=0,
                            command=lambda column=i: self.buttonClicked("UP", column))
            button.image = upPhoto
            button.config(activebackground="black", activeforeground="red")
            button.grid(row=len(self.__cylindersArrange) * 2 + 3, column=i)
            self.__buttons.append(button)  # on ajoute le bouton à la liste des boutons

        downImage = Image.open("asset/DOWN.png")  # image pour le bouton DOWN
        downPhoto = ImageTk.PhotoImage(downImage)
        for i in range(len(self.__cylindersArrange[0])):  # affiche les boutons DOWN
            button = Button(self.__frame0, image=downPhoto, fg="red", bg="black", border=0,
                            command=lambda column=i: self.buttonClicked("DOWN", column))
            button.image = downPhoto
            button.config(activebackground="black", activeforeground="red")
            button.grid(row=len(self.__cylindersArrange) * 2 + 5, column=i)
            self.__buttons.append(button)  # on ajoute le bouton à la liste des boutons

    def updateColumnUp(self, column: int):
        """Met à jour la colonne selectionnée vers le haut"""
        t = Thread(target=self.playSound)  # on lance le son dans un thread
        t.start()  # on démarre le thread
        first_letter = self.__cylindersArrange[0][column]  # on récupère la première lettre
        for i in range(len(self.__cylindersArrange) - 1):  # on parcourt les lignes du cylindre
            self.__cylindersArrange[i][column] = self.__cylindersArrange[i + 1][column]  # on décale les lettres
        self.__cylindersArrange[-1][column] = first_letter  # on met la première lettre à la fin
        self.clearWindow()  # on efface certains widgets
        self.update()  # on met à jour certians widgets

    def updateColumnDown(self, column: int):
        """Met à jour la colonne selectionnée"""
        t = Thread(target=self.playSound)  # on lance le son dans un thread
        t.start()  # on démarre le thread
        last_letter = self.__cylindersArrange[-1][column]  # on récupère la dernière lettre
        for i in range(len(self.__cylindersArrange) - 1, 0, -1):  # on parcourt les lignes du cylindre
            self.__cylindersArrange[i][column] = self.__cylindersArrange[i - 1][column]  # on décale les lettres
        self.__cylindersArrange[0][column] = last_letter  # on met la dernière lettre au début
        self.clearWindow()  # on efface certains widgets
        self.update()  # on met à jour certians widgets

    def buttonClicked(self, direction: str, column: int):
        """Action lorsqu'un bouton est cliqué"""
        if direction == "UP":  # si le bouton cliqué est UP
            self.__selectedColumn = column  # on met à jour la colonne selectionnée
            self.updateColumnUp(column)  # on met à jour la colonne selectionnée vers le haut
        elif direction == "DOWN":  # si le bouton cliqué est DOWN
            self.__selectedColumn = column  # on met à jour la colonne selectionnée
            self.updateColumnDown(column)  # on met à jour la colonne selectionnée vers le bas

    def displayFinishButton(self):
        """affiche le bouton FINISH"""
        finishImage = Image.open("asset/finish.png")  # image pour le bouton FINISH
        finishPhoto = ImageTk.PhotoImage(finishImage)
        button = Button(self.__frame0, image=finishPhoto, fg="red", bg="black", border=0, command=self.CloseProgram)
        button.image = finishPhoto  # on met l'image dans le bouton
        button.config(activebackground="black", activeforeground="red")
        button.grid(row=len(self.__cylindersArrange) * 2 + 1, column=len(self.__cylindersArrange[0]) * 4)
        self.__buttons.append(button)  # on ajoute le bouton à la liste des boutons

    def displayInfoButton(self):
        """affiche le bouton HOW IT WORKS"""
        infoImage = Image.open("asset/howitwork.png")  # image pour le bouton HOW IT WORKS
        infoPhoto = ImageTk.PhotoImage(infoImage)
        button = Button(self.__frame0, image=infoPhoto, fg="red", bg="black", border=0, command=self.InfoButton)
        button.image = infoPhoto  # on met l'image dans le bouton
        button.config(activebackground="black", activeforeground="red")
        button.grid(row=0, column=len(self.__cylindersArrange[0]) * 4, rowspan=4)
        self.__buttons.append(button)  # on ajoute le bouton à la liste des boutons

    @staticmethod
    def InfoButton():
        """Affiche une fenetre avec les instructions d'utilisation"""
        messagebox.showinfo("How it works", "1. Enter your phrase in the line 'CLEAR', to do this, click on the UP "
                                            "or DOWN buttons. This will encrypt your phrase in the 'CIPHER' line.\n"
                                            "2. Click on the FINISH button to get your encrypted phrase and close "
                                            "the program.\n\nInformation on the different buttons:\n- 'SAVE CYLINDERS'" 
                                            "allows you to save the status of your current cylinders in a '.save' file."
                                            "\n- 'LOAD CYLINDERS' allows you to load the state of the cylinders from a " 
                                            "'.save' file.\n- 'AUTO CLEAR' allows you to enter text equal to or smaller"
                                            "than the size of a cylinder and automatically clears the cylinder.\n- "
                                            "'AUTO CIPHER' allows you to enter text equal to or smaller than the size"
                                            " of a cylinder and automatically decrypts it.\n- 'RESET CYLINDERS' allows"
                                            "you to reset cylinders to their original state, i.e. to the order created"
                                            "with the selected keys.\n- 'CUT/PUT SOUND' allows you to turn on or off"
                                            " the sound when using the program.\n\nNB : You can also use the keyboard "
                                            "to encrypt your phrase :\n"
                                            "Click the up keys to move up the letters\n"
                                            "Click the down keys to move down the letters\n"
                                            "Click the right keys to move to the right\n"
                                            "Click the left keys to move to the left\n"
                                            "Click the enter key to get your encrypted phrase and close the program")

    def displaySaveButton(self):
        """affiche le bouton SAVE CYLINDERS"""
        saveImage = Image.open("asset/save.png")  # image pour le bouton SAVE CYLINDERS
        savePhoto = ImageTk.PhotoImage(saveImage)
        button = Button(self.__frame0, image=savePhoto, fg="red", bg="black", border=0, command=self.saveButton)
        button.image = savePhoto  # on met l'image dans le bouton
        button.config(activebackground="black", activeforeground="red",)
        button.grid(row=4, column=len(self.__cylindersArrange[0]) * 4, rowspan=4)
        self.__buttons.append(button)  # on ajoute le bouton à la liste des boutons

    def saveButton(self):
        """Sauvegarde les cylindres dans un fichier save"""
        filename = simpledialog.askstring("Input", "Enter the name of the file in the dialog input\n with '.save' at "
                                                   "the end :")
        with open(filename, "w") as file:  # on ouvre le fichier en écriture
            file.write(str(self.__sizeElement))
            file.write("\n")
            for i in range(len(self.__cylindersArrange)):
                for j in range(len(self.__cylindersArrange[i])):
                    file.write(self.__cylindersArrange[i][j])  # on écrit les lettres des cylindres dans le fichier
                file.write("\n")
        file.close()  # on ferme le fichier
        filepath = os.path.join(os.getcwd(), filename)  # on récupère le chemin du fichier
        messagebox.showinfo("Save", f"The cylinders have been saved in the file 'cylinders.save'\n The file is located"
                                    f" in the folder {filepath}")

    def displayLoadButton(self):
        """affiche le bouton LOAD CYLINDERS"""
        loadImage = Image.open("asset/load.png")  # image pour le bouton LOAD CYLINDERS
        loadPhoto = ImageTk.PhotoImage(loadImage)
        button = Button(self.__frame0, image=loadPhoto, fg="red", bg="black", border=0, command=self.loadButton)
        button.image = loadPhoto  # on met l'image dans le bouton
        button.config(activebackground="black", activeforeground="red")
        button.grid(row=8, column=len(self.__cylindersArrange[0]) * 4, rowspan=4)
        self.__buttons.append(button)  # on ajoute le bouton à la liste des boutons

    def loadButton(self):
        """Charge les cylindres depuis un fichier save"""
        filename = filedialog.askopenfilename()  # on ouvre une fenêtre pour choisir le fichier
        if not filename.endswith(".save"):
            messagebox.showerror("Error", "Invalid file type. Select a '.save' file.")
            return
        with open(filename, "r") as file:  # on ouvre le fichier en lecture
            self.__sizeElement = int(file.readline())  # on récupère la taille des éléments
            self.__cylindersArrange = []
            for line in file:
                self.__cylindersArrange.append(list(line.replace("\n", "")))  # on récupère les lettres des cylindres
        file.close()  # on ferme le fichier
        self.clearWindow()
        self.update()

    def displayAutoButton(self):
        """affiche le bouton AUTO SEARCH"""
        autoClearImage = Image.open("asset/autoclear.png")  # image pour le bouton AUTO SEARCH
        autoClearPhoto = ImageTk.PhotoImage(autoClearImage)
        button = Button(self.__frame0, image=autoClearPhoto, fg="red", bg="black", border=0,
                        command=lambda column=0: self.autoButtonClicked("AUTO SEARCH"))
        button.image = autoClearPhoto  # on met l'image dans le bouton
        button.config(activebackground="black", activeforeground="red")
        button.grid(row=12, column=len(self.__cylindersArrange[0]) * 4, rowspan=4)
        self.__buttons.append(button)  # on ajoute le bouton à la liste des boutons

    def displayEncryptButton(self):
        """affiche le bouton AUTO ENCRYPT"""
        autoCipherImage = Image.open("asset/autocipher.png")  # image pour le bouton AUTO ENCRYPT
        autoCipherPhoto = ImageTk.PhotoImage(autoCipherImage)
        button = Button(self.__frame0, image=autoCipherPhoto, fg="red", bg="black", border=0,
                        command=lambda column=0: self.autoButtonClicked("AUTO ENCRYPT"))
        button.image = autoCipherPhoto  # on met l'image dans le bouton
        button.config(activebackground="black", activeforeground="red")
        button.grid(row=16, column=len(self.__cylindersArrange[0]) * 4, rowspan=4)
        self.__buttons.append(button)  # on ajoute le bouton à la liste des boutons

    def autoButtonClicked(self, todo: str):
        """Action lorsqu'un bouton est cliqué """
        if todo == "AUTO SEARCH":
            self.autoButton(10, 8, 9, 1)
        elif todo == "AUTO ENCRYPT":
            self.autoButton(16, 14, 15, 2)
        """Les deux premiers paramètres sont les lignes adjacentes à la ligne du texte à trouver, le troisième
            est la ligne dans laquelle se trouve le texte recherché, le quatrième est le numéro permettant d'afficher
            un message."""
    def autoButton(self, maxrow: int, minrow: int, line: int, choose: int):
        """Demande à l'utilisateur de rentrer une phrase et modifie les cylindres pour que la phrase soit cryptée"""
        text = simpledialog.askstring("Input", "Enter text in the dialog input:")
        if text is None:
            return
        text = text.upper().replace(" ", "")
        if not text.isalpha():
            messagebox.showerror("Invalid text", " Text must be only composed of letters !")
            return
        if len(text) > self.__sizeElement:
            messagebox.showerror(f"Invalid text length", " Text must be {self.__sizeElement} characters max long !")
            return
        self.encryptText(text, 0, maxrow, minrow, line, active=1, choose=choose)
        """Le premier paramètre est la phrase à crypter, le deuxième est le numéro de la 1er colonne , le troisième et 
        le quatrième sont les lignes pour rechercher la lettre, le cinquième est la ligne dans laquelle le texte est
         chiffrer/dechiffrer, le sixième est un paramètre permettant de savoir si on passe dans la fonction 
         pour la 1er fois et le dernier est le numéro permettant d'afficher un message."""

    def encryptText(self, text: str, column: int, maxrow: int, minrow: int, line: int, active: int, choose: int):
        """Modifie les cylindres pour que la phrase soit cryptée"""
        if active == 1:
            self.__total = len(text)  # on initialise le nombre de lettres à crypter
        if column >= len(text):
            return
        letter = text[column]
        row = next(i for i, c in enumerate(self.__cylindersArrange) if c[column] == letter)  # on récupère la ligne
        if row >= maxrow:
            for _ in range(row - line):  # on déplace la ligne vers le haut
                self.updateColumnUp(column)
            self.__total -= 1
            self.__root1.after(1500, lambda: self.encryptText(text, column + 1, maxrow, minrow, line, 0, choose))
        elif row <= minrow:
            for _ in range(line - row):  # on déplace la ligne vers le bas
                self.updateColumnDown(column)
            self.__total -= 1
            self.__root1.after(1500, lambda: self.encryptText(text, column + 1, maxrow, minrow, line, 0, choose))
        else:
            self.__total -= 1
            self.encryptText(text, column + 1, maxrow, minrow, line, 0, choose)  # on passe à la lettre suivante
        if self.__total == 0:
            self.windowsLoadingPart2(choose)  # on affiche la fenêtre de chargement

    def windowsLoadingPart2(self, choose: int):
        root2 = tk.Toplevel(self.__root1)  # on crée une nouvelle fenêtre
        largeur_principale = self.__root1.winfo_width()  # on récupère la largeur de la fenêtre principale
        hauteur_principale = self.__root1.winfo_height()  # on récupère la hauteur de la fenêtre principale

        x_principale = self.__root1.winfo_rootx()  # on récupère la position horizontale de la fenêtre principale
        y_principale = self.__root1.winfo_rooty()  # on récupère la position verticale de la fenêtre principale

        x_fenetre = x_principale  # Position horizontale
        y_fenetre = y_principale  # Position verticale

        root2.geometry(f"+{x_fenetre}+{y_fenetre}")  # on place la fenêtre à la même position que la fenêtre principale
        root2.geometry(f"{largeur_principale}x{hauteur_principale}")  # Donne la même taille que la fenêtre principale
        root2.configure(bg='black')
        root2.overrideredirect(True)
        if choose == 1:
            for i in range(6):
                label = blinking.BlinkingLabel(root2, text='TEXT CRYPTED', font=('Arial', 24), bg='black')
                label.pack(pady=50)
        elif choose == 2:
            for i in range(6):
                label = blinking.BlinkingLabel(root2, text='TEXT DECRYPTED', font=('Arial', 24), bg='black')
                label.pack(pady=50)
        root2.after(3000, root2.destroy)  # on ferme la fenêtre après 3 secondes

    def displayResetButton(self):
        """affiche le bouton RESET"""
        resetImage = Image.open("asset/reset.png")  # image pour le bouton RESET
        resetPhoto = ImageTk.PhotoImage(resetImage)
        button = Button(self.__frame0, image=resetPhoto, fg="red", bg="black", border=0, command=self.resetButton)
        button.image = resetPhoto  # on met l'image dans le bouton
        button.config(activebackground="black", activeforeground="red")
        button.grid(row=20, column=len(self.__cylindersArrange[0]) * 4, rowspan=4)
        self.__buttons.append(button)  # on ajoute le bouton à la liste des boutons

    def resetButton(self):
        """Remet les cylindres dans leur position initiale"""
        self.__cylindersArrange = copy.deepcopy(self.__resetCylindersArrange)
        self.clearWindow()
        self.update()

    def displaySoundButton(self):
        """affiche le bouton SOUND"""
        soundImage = Image.open("asset/cut.png" if self.__songPlayed else "asset/put.png")
        soundPhoto = ImageTk.PhotoImage(soundImage)
        if not hasattr(self, 'soundButton'):  # si le bouton n'existe pas
            self.soundButton = Button(self.__frame0, image=soundPhoto, fg="red", bg="black", border=0,
                                      command=self.soundButtonCallback)
            self.soundButton.image = soundPhoto  # on met l'image dans le bouton
            self.soundButton.config(activebackground="black", activeforeground="red")
            self.soundButton.grid(row=24, column=len(self.__cylindersArrange[0]) * 4, rowspan=4)
            self.__buttons.append(self.soundButton)  # on ajoute le bouton à la liste des boutons
        else:
            self.soundButton.config(image=soundPhoto)  # on change l'image du bouton
            self.soundButton.image = soundPhoto

    def soundButtonCallback(self):
        """Joue ou coupe le son"""
        if self.__songPlayed:
            self.__songPlayed = False
        else:
            self.__songPlayed = True
        self.displaySoundButton()

    def playSound(self):
        """Joue un son"""
        if self.__songPlayed:
            playsound("asset/roulement.mp3")

    def displayKey(self):
        """affiche la bouton GET KEY"""
        keyImage = Image.open("asset/key.png")
        keyPhoto = ImageTk.PhotoImage(keyImage)
        button = Button(self.__frame0, image=keyPhoto, fg="red", bg="black", border=0, command=self.keyButton)
        button.image = keyPhoto  # on met l'image dans le bouton
        button.config(activebackground="black", activeforeground="red")
        button.grid(row=28, column=len(self.__cylindersArrange[0]) * 4, rowspan=4)
        self.__buttons.append(button)  # on ajoute le bouton à la liste des boutons

    def keyButton(self):
        """Affiche la clé des cylindres"""
        messagebox.showinfo("Clé des cylindres", "Look at the console")
        print("La clé actuelle des cylindres est : ", self.__key)

    def CloseProgram(self, event=None):
        """termine l'algorithme et ferme la fenetre"""
        self.__root1.destroy()
        chiffred = [self.__cylindersArrange[15][i] for i in range(len(self.__cylindersArrange[15]))]
        print("Le chiffrement de votre phrase est : ", ''.join(chiffred))
