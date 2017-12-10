TP IA : Problème du voyageur de commerce
----------------------------------------

Structure du code:
------------------
Nous avons utilisé un named tuple pour représenter une ville et nou avons
créé 2 classe. Individual qui correspond à une solution et Population qui
regroupe tous les individus

Fonctions principales:
----------------------
individual.mutate() permet de faire muter un individu en change en échangeant
2 villes de place dans le chemin

individual.cross_breeding(individual) permet de crosser 2 individu entre eu
pour en créer un nouveau la méthode utilisée est celle décrite dans le pdf
arob98.pdf

individual.fitness() permet de calculer le score de l'individus

population.selection() permet de sélectionner les individus faisant partie de la
nouvelle population elle est 50% élitiste et 50% aléatoire

population.run(bool) permet de faire évoluer la population en faisant
mutation, cross et sélection et le parametre permet de définir si la gui
s'affiche ou non

Améliorations possibles:
------------------------
-ne pas créer l'individu totalement aléatoirement mais essayer de relier les
villes les plus proches
