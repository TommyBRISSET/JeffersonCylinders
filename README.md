# Cylindre de Jefferson


## Description

Le cylindre de Jefferson est un dispositif permettant de chiffrer des messages. Il a été inventé par Thomas Jefferson en 1795.
Cet appareil est constitué d’un certain nombre de disques, 36 pour l’original, pivotants autour d’un axe et sur lesquels sont inscrits des alphabets désordonnés. Les deux correspondants disposent des mêmes disques.

Chaque disque est identifiable par un numéro. La clé est l’ordre dans lequel les disques sont insérés sur l’axe, il s’agit donc d’une suite de numéros.

Pour chiffrer un message, l’expéditeur arrange les disques selon la clé, puis les fait pivoter de telle sorte que le message apparaisse sur une même ligne du cylindre. Le message chiffré sera alors le contenu de la sixième ligne suivante (ce dernier choix n’est que conventionnel, on aurait pu en effectuer un autre).

Pour déchiffrer un message, le destinataire arrange bien sûr lui aussi les disques selon la clé, puis les fait pivoter de telle sorte que le message chiffré apparaisse sur une même ligne du cylindre. Le message d’origine sera alors le contenu de la sixième ligne précédente.

## Fonctionnement

Version console :

Lancer le fichier 'JeffersonConsole.py' avec python3.
Vous pouvez tester les différentes fonctions unes à unes en décommettant les lignes correspondantes à la fin du fichier
ou tester les exemples de chiffrement et déchiffrement se situant aussi à la fin dans la partie Test.

Version graphique :

Pour lancer la version graphique :
- Veillez à ouvrir le fichier start.py et modifier le fichier txt contenant les cylindres dans le lancement de la fonction.
- ```python3 start.py```

Cela ouvre la premiere fenêtre de l'application permettant de choisir l'ordre des clés puis vous enmène
vers la fenêtre principale du programme.

## Attention :
 Programme réalisé sous python3 et plus precisemment, veillez à utiliser la version 3.10.11 de python.
Les modules 'Playsound' version 1.2.2 et 'Pillow' version 9.5.0 sont requis pour le bon fonctionnement du programme.
 