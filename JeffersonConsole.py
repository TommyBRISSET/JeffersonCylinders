import random
import string


class JeffersonConsole:
    def __init__(self, filename: str):
        self.__filename = filename  # nom du fichier
        self.__permutationsDict = {}  # dictionnaire des permutations

    @staticmethod
    def alphabetRandom(length: int) -> str:  # mettre 26
        """Tirage aléatoire d'une chaîne de caractère constituée
         des 26 lettres de l'alphabet."""
        letters = string.ascii_uppercase
        listAlphabet = ''
        usedLetters = set()  # Ensemble pour stocker les lettres déjà générées
        for i in range(length):
            # Tant que la lettre générée n'est pas dans l'ensemble, on la rajoute à la liste et on l'ajoute à l'ensemble
            while True:
                letter = random.choice(letters)
                if letter not in usedLetters:
                    usedLetters.add(letter)
                    listAlphabet += letter
                    break
        return listAlphabet

    def writeInFile(self, nbr: int):
        """Écriture de n lignes dans un fichier texte, n étant un paramètre entier strictement
         positif, chacune d'elles étant générée selon le tirage précédent."""
        with open(self.__filename, 'w') as file:
            for i in range(nbr):
                line = self.alphabetRandom(26) + '\n'
                file.write(line)  # écriture de la ligne dans le fichier
        file.close()  # fermeture du fichier

    def readFile(self) -> dict[int, str]:
        """Lecture d'un fichier texte dont chaque ligne contient une permutation des 26 lettres de l’alphabet
         en majuscules et création d'un dictionnaire dont les clés sont les entiers compris entre un 1 et le
         nombre de lignes du fichier, la valeur correspondante à une clé i étant la i-ème ligne du fichier."""
        with open(self.__filename, 'r') as file:
            lines = file.readlines()
            self.__permutationsDict = {i + 1: lines[i].strip() for i in range(len(lines))}  # création du dictionnaire
        return self.__permutationsDict

    @staticmethod
    def verifyPermutation(lst: list) -> bool:
        """Vérification si une liste de n entiers est une permutation des entiers
         compris (au sens large) entre 1 et n."""
        n = len(lst)
        s = set(lst)
        return n == len(s) and min(s) == 1 and max(s) == n

    @staticmethod
    def generatePermutation(n: int) -> list:
        """Génération d'une permutation des entiers compris (au sens large) entre 1 et n."""
        lst = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            lst[i], lst[j] = lst[j], lst[i]  # permutation de deux éléments
        return lst

    @staticmethod
    def lettersChifrement(letter: str, permutation: list) -> str:
        """ Chiffrement d'une lettre relativement à une permutation des 26 lettres de
         l’alphabet en majuscules : on retourne la lettre située 6 positions après elle
          dans la permutation. On suppose bien sûr que l’alphabet en question est circulaire."""
        index = permutation.index(letter)
        chiffre = permutation[(index + 6) % 26]  # % 26 pour que l'index ne dépasse pas 26
        return chiffre

    @staticmethod
    def lettersDechiffrement(letter: str, permutation: list) -> str:
        """ Déchiffrement d'une lettre relativement à une permutation des 26 lettres de
         l’alphabet en majuscules : on retourne la lettre située 6 positions avant elle
          dans la permutation. On suppose bien sûr que l’alphabet en question est circulaire."""
        index = permutation.index(letter)
        chiffre = permutation[(index - 6) % 26]  # % 26 pour que l'index ne dépasse pas 26
        return chiffre

    def JeffersonChiffrement(self, key: list, text: str) -> str:
        """À partir d'un cylindre, i.e. un dictionnaire comme décrit précédemment, et d'une
         clé, i.e. l'ordre des cylindres, chiffrer un texte selon l'algorithme de Jefferson."""
        txt = text.upper()  # S'assurer que le texte est en majuscule
        txt = txt.replace(" ", "")  # Supprimer les espaces
        dicCylinders = self.readFile()
        TxtChiffred = ""
        if self.verifyPermutation(key):
            for i in range(len(txt)):
                TxtChiffred += self.lettersChifrement(txt[i], dicCylinders[key[i]])  # Chiffrement de chaque lettre
        return TxtChiffred

    def JeffersonDechiffrement(self, key: list, textChiffred: str) -> str:
        """À partir d'un cylindre, i.e. un dictionnaire comme décrit précédemment, et d'une
                 clé, i.e. l'ordre des cylindres, déchiffrer un texte selon l'algorithme de Jefferson."""
        dicCylinders = self.readFile()  # Dictionnaire des cylindres
        txtDechiffred = ""
        if self.verifyPermutation(key):
            for i in range(len(textChiffred)):
                txtDechiffred += self.lettersDechiffrement(textChiffred[i], dicCylinders[key[i]])  # Déchiffrement
        return txtDechiffred

#--------------------------------------------------- Test ---------------------------------------------------#

#test de chaque fonction de la classe JeffersonConsole


"""
test = JeffersonConsole("data.txt")

# test AlphabetRandom
test.alphabet = test.alphabetRandom(26)
print("Un alphabet désordonné : ", test.alphabet)
# test writeInFile
test.writeInFile(10)
# test readFile
print("dico avec clé de 1 à n et alphabet désordonné :  \n", test.readFile())
# test verifyPermutation
print("Vérification si une liste de n entiers est une permutation des entiers compris (au sens large) entre 1 et n\n"
      "exemple : [1, 2, 3, 4, 5] renvoie True \n ", test.verifyPermutation([1, 2, 3, 4, 5]))
# test generatePermutation
print("Génération d'une permutation des entiers compris (au sens large) entre 1 et n\n", test.generatePermutation(5))
# test lettersChifrement
print("Chiffrement d'une lettre relativement à une permutation des 26 lettres de l’alphabet en majuscules "
      "(B renvoie T) : ", test.lettersChifrement("B", "NOZUTWDCVRJLXKISEFAPMYGHBQ"))
"""
#test exemple énoncé de chiffrement
"""
test_1 = JeffersonConsole("cylinders/cylinderWiki.txt")
key_1 = [7, 9, 5, 10, 1, 6, 3, 8, 2, 4]
text_1 = "Retreat Now"
encrypted_text_1 = test_1.JeffersonChiffrement(key_1, text_1)
print("le texte chiffré : ", encrypted_text_1)  # print 'OMKEGWPDFN'
"""
#test exemple énoncé de déchiffrement
"""
test_2 = JeffersonConsole("cylinders/1ARIT-MP.txt")
key_2 = [12, 16, 29, 6, 33, 9, 22, 15, 20, 3, 1, 30, 32, 36, 19, 10, 35, 27, 25, 26, 2, 18, 31, 14, 34, 17, 23, 
7, 8, 21, 4, 13, 11, 24, 28, 5]
encrypted_text_2 = "GRMYSGBOAAMQGDPEYVWLDFDQQQZXXVMSZFS"
decrypted_text_2 = test_2.JeffersonDechiffrement(key_2, encrypted_text_2)
print("le texte déchiffré : ", decrypted_text_2)  # devrait print 'RETREATNOW'
"""

#--------------------------------------------------- Notre test ---------------------------------------------------#

"""
test_3 = JeffersonConsole("cylinders/OurCylinders.txt")
print(test_3.generatePermutation(44))
key_3 = [37, 23, 39, 43, 9, 7, 30, 2, 16, 28, 11, 22, 8, 44, 18, 15, 26, 40, 31, 4, 14, 24, 13, 21, 20, 36, 3, 17, 1, 
35, 25, 32, 34, 19, 33, 29, 5, 10, 6, 27, 12, 41, 38, 42]
text_3 = "SUPINFO ecole des experts metiers de linformatique"
encrypted_text_3 = test_3.JeffersonChiffrement(key_3, text_3)
print("le texte chiffré : ", encrypted_text_3)  # print 'GDELQLSGFIVISGDGGVUZBJWIQNLORJZUYCYRBQVDCVOL'
"""

"""
test_4 = JeffersonConsole("cylinders/OurCylinders.txt")
key_4 = [37, 23, 39, 43, 9, 7, 30, 2, 16, 28, 11, 22, 8, 44, 18, 15, 26, 40, 31, 4, 14, 24, 13, 21, 20, 36, 3, 17, 1, 
35, 25, 32, 34, 19, 33, 29, 5, 10, 6, 27, 12, 41, 38, 42]
encrypted_text_4 = "GDELQLSGFIVISGDGGVUZBJWIQNLORJZUYCYRBQVDCVOL"
decrypted_text_4 = test_4.JeffersonDechiffrement(key_4, encrypted_text_4)
print("le texte déchiffré : ", decrypted_text_4)  # print 'SUPINFOECOLEDSEXMETIERSDELINFORMATIQUE'
"""
