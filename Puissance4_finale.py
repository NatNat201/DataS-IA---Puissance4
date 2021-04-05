##Puissance 4


##grille
import math
from copy import deepcopy

#création de la grille
def creationGrille():
    grille = []
    for i in range(GRILLE_HAUTEUR):
        grille.append([])
        for j in range(GRILLE_LONGUEUR):
            grille[i].append(' ')
    return grille

#On regarde si la colonne est pleine ou non
def colonneValide(grille, Col):
    if grille[0][Col] == ' ':
        return True
    return False

#renvoie tous les coups possibles, c'est-à-dire les colonnes vides
def coupsValides(grille):
    Columns = []
    for Col in range(GRILLE_LONGUEUR):
        if colonneValide(grille, Col):
            Columns.append(Col)
    return Columns

#places the current move's joueur ['x'|'o'] in the referenced column in the grille
def actionJoueur(grille, col, joueur):
    #on utilise deepcopy pour faire une copie de la grille et ne pas toucher à la grille d’origine
    grille_bis = deepcopy(grille)
    for row in range(5,-1,-1):
        if grille_bis[row][col] == ' ':
            grille_bis[row][col] = joueur
            return grille_bis, row, col

#vérifie si la colonne jouée est vide ou non
def colonneVide(col, grille):
    for row in range(GRILLE_HAUTEUR):
        if grille[row][col] == ' ':
            return True
    return False


##Affichage

def printGrille(grille):
    print('')
    print("\t      1   2   3   4   5   6   7   8   9  10  11  12")

    print('         --- --- --- --- --- --- --- --- --- --- --- ---  ')
    for i in range(0, GRILLE_HAUTEUR, 1):
        print("\t",i+1,' ',end="")
        #
        for j in range(GRILLE_LONGUEUR):
            if str(grille[i][j]) == 'x':
                print("| " + "\033[1;36;48m" + str(grille[i][j]) + "\033[0m", end=" ")   #couleur du jeton
            elif str(grille[i][j]) == 'o':
                print("| " + "\033[1;31;48m" + str(grille[i][j]) + "\033[0m", end=" ")   #couleur du jeton
            elif str(grille[i][j]) == 'X':
                print("| " + "\033[1;36;48m" + str(grille[i][j]) + "\033[0m", end=" ")   #couleur du jeton
            elif str(grille[i][j]) == 'O':
                print("| " + "\033[1;31;48m" + str(grille[i][j]) + "\033[0m", end=" ")   #couleur du jeton
            else:
                print("| " + str(grille[i][j]), end=" ")

        print("|")
        print("\t     --- --- --- --- --- --- --- --- --- --- --- ---  ")
    print('')


##Comptage des séquences alignées

GRILLE_LONGUEUR  = 12
GRILLE_HAUTEUR = 6
IA    = 'O'
JOUEUR = 'X'

def countSequence(grille, joueur, length):
    """ La fonction parcourt la grille et compte le nombre de fois où 'length' pions alignés par le 'joueur', c'est-à-dire que si length=4, la fonction compte le nombre de fois où 4 pions sont alignés pour le joueur
    """
    total = 0
    # On regarde chaque case de la grille
    for row in range(GRILLE_HAUTEUR):
        for col in range(GRILLE_LONGUEUR):
            # On vérifie si elle correspond au joueur que l'on a en paramètre
            if grille[row][col] == joueur:
                # Regarde si une séquence de length pions verticalement alignés commence en (row, col)
                total += verticalSeq(grille,row, col,length)
                # Regarde si une séquence de length pions horizontalement alignés commence en (row, col)
                total += horizontalSeq(grille,row, col,length)
                # Regarde si l'une des deux, voire les deux, diagonales a un alignement de length pions qui commence en (row, col)
                total += (posDia(grille,row, col,length) + negDia(grille,row, col,length))
    # return la somme de séquences alignées pour length pions alignés
    return total



def verticalSeq(grille,row, col,length):
    """La fonction retourne 1 si elle a trouvé un alignement vertical de length pions
    """
    count = 0
    for rowIndex in range(row, GRILLE_HAUTEUR):
        if grille[rowIndex][col] == grille[row][col]:
            count += 1
        else:
            break
    if count >= length:
        return 1
    else:
        return 0

def horizontalSeq(grille,row, col,length):
    """La fonction retourne 1 si elle a trouvé un alignement horizontal de length pions
    """
    count = 0
    for colIndex in range(col, GRILLE_LONGUEUR):
        if grille[row][colIndex] == grille[row][col]:
            count += 1
        else:
            break
    if count >= length:
        return 1
    else:
        return 0


def negDia(grille,row,col,length):
    count = 0
    colIndex = col
    for rowIndex in range(row, -1, -1):
        if colIndex > 10:
            break
        elif grille[rowIndex][colIndex] == grille[row][col]:
            count += 1
        else:
            break
        # On incrémente la colonne de 1 quand la rangée diminue
        colIndex = colIndex-1
    if count >= length:
        return 1
    else:
        return 0



def posDia(grille, row, col, length):
    count = 0
    colIndex = col
    for rowIndex in range(row, -1, -1):
        if colIndex > 10:
            break
        elif grille[rowIndex][colIndex] == grille[row][col]:
            count += 1
        else:
            break
        # On incrémente la colonne de 1 quand la rangée diminue
        colIndex = colIndex+1
    if count >= length:
        return 1
    else:
        return 0


##Heuristique

def Heuristique(grille, joueur):
    """ On évalue l'état de la grille de jeu
    La valeur calculée résulte de la différence entre le score du joueur qui appelle la fonction et le score de l'adversaire
        Le score total d'un joueur correspond à la somme de toutes les séquences qu'il a réussi à aligner (2,3 ou 4 pions) que l'on va pondérer proportionnellement au nombre de pions alignés afin que le score 'récompense' les longues séquences puisque c'est le but du jeu.
    """
    if joueur == JOUEUR: adversaire = IA
    else: adversaire = JOUEUR

    joueur_4    = countSequence(grille, joueur, 4)
    joueur_3   = countSequence(grille, joueur, 3)
    joueur_2     = countSequence(grille, joueur, 2)
    joueurScore    = joueur_4*10000000 + joueur_3*10000 + joueur_2*100

    adversaire_4  = countSequence(grille, adversaire, 4)
    adversaire_3 = countSequence(grille, adversaire, 3)
    adversaire_2   = countSequence(grille, adversaire, 2)
    adversaireScore  = adversaire_4*10000000 + adversaire_3*10000 + adversaire_2*100

    if adversaire_4 > 0:
        #Dans ce cas, le joueur pour lequel on évalue la grille a perdu
        #On return la plus petite valeur possible => -infinity
        return -1000000000000000000
    else:
        #Return le score du joueur-le score de l'adversaire
        return joueurScore - adversaireScore


def gameIsOver(grille):
    """On regarde s'il y a un gagnant
    """
    if countSequence(grille, JOUEUR, 4) >= 1:
        return 1
    elif countSequence(grille, IA, 4) >= 1:
        return -1
    else:
        return 0



##minimax


from random import shuffle

def MiniMaxAlphaBeta(grille, depth, joueur):
    # on fait la liste des mouvements possibles
    validMoves = coupsValides(grille)
    shuffle(validMoves) #on mélange les coups, pour qu’il choisisse de manière aléatoire dans le cas où deux coups sont possibles et tout aussi efficace
    bestMove  = validMoves[0]
    bestScore = float("-inf")

    # on initialise alpha et beta
    alpha = -1000000000000000000
    beta = 1000000000000000000

    if joueur == IA: adversaire = JOUEUR
    else: adversaire = IA

    # on va tester chacun des movements possibles
    for move in validMoves:
        # on créé une grille secondaire pour tester
        grille_bis = actionJoueur(grille, move, joueur)[0]
        # on exécute la fonction minimizeBeta sur cette grille
        grilleScore = minimizeBeta(grille_bis, depth - 1, alpha, beta, joueur, adversaire )
        if grilleScore > bestScore:
            bestScore = grilleScore
            bestMove = move
    return bestMove

def minimizeBeta(grille, depth, a, b, joueur, adversaire):
    validMoves = []
    for col in range(12):
        # si la colonne fait partie des mouvements possibles
        if colonneVide(col, grille):
            # on joue alors dans cette colonne
            temp = actionJoueur(grille, col, joueur)[2]
            validMoves.append(temp)

    # on regarde si la partie est finie
    if depth == 0 or len(validMoves) == 0 or gameIsOver(grille):
        return Heuristique(grille, joueur)

    validMoves = coupsValides(grille)
    beta = b

    # on évalue les scores
    for move in validMoves:
        grilleScore = 1000000000000000000
        if a < beta:
            grille_bis = actionJoueur(grille, move, adversaire )[0]
            grilleScore = maximizeAlpha(grille_bis, depth - 1, a, beta, joueur, adversaire )

        if grilleScore < beta:
            beta = grilleScore
    return beta

def maximizeAlpha(grille, depth, a, b, joueur, adversaire ):
    validMoves = []
    for col in range(12):
        # si la colonne fait partie des mouvements possibles
        if colonneVide(col, grille):
            # on joue alors dans cette colonne
            temp = actionJoueur(grille, col, joueur)[2]
            validMoves.append(temp)
    # on regarde si la partie est finie
    if depth == 0 or len(validMoves) == 0 or gameIsOver(grille):
        return Heuristique(grille, joueur)

    alpha = a
    # on évalue les scores
    for move in validMoves:
        grilleScore = -1000000000000000000
        if alpha < b:
            grille_bis = actionJoueur(grille, move, joueur)[0]
            grilleScore = minimizeBeta(grille_bis, depth - 1, alpha, b, joueur, adversaire )

        if grilleScore > alpha:
            alpha = grilleScore
    return alpha


def joueurTurn(grille):
    Col = eval(input('Choisis une colonne entre 1 et 12 : '))
    colsPossibles = [1,2,3,4,5,6,7,8,9,10,11,12]

    if Col not in colsPossibles:
        print("Vous devez entrer un entier")
        return joueurTurn(grille)

    joueurMove = int(Col) - 1

    if joueurMove < 0 or joueurMove > 12:
        print("Vous devez entrer un nombre entre 1 et 12!")
        return joueurTurn(grille)

    if not(colonneValide(grille, joueurMove)):
        print("Cette colonne est déja pleine")
        return joueurTurn(grille)


    grille = actionJoueur(grille, joueurMove, JOUEUR)[0]
    joueurFourInRow  = recherchePuissance4(grille)
    return grille, joueurFourInRow


##Jeu
def GameIsOver(grille):
    """On regarde s'il y a un gagnant
    """
    if countSequence(grille,'O', 4) >= 1:
        return 1
    elif countSequence(grille, 'X', 4) >= 1:
        return -1
    else:
        return 0

def AquiLeTour_IA_commence(grille):
    #on considère que L'IA commence
    nbO = 0
    nbX = 0
    cjX=0
    cjO=1
    for i in range(6):
        for j in range(12):
            if grille[i][j] == 'X':
                nbX +=1
            if grille[i][j] == 'O':
                nbO +=1

    #s'il y a le même nombre de O et de X, c'est au tour de l'IA car elle commence le 'tour'
    #sinon, cela veut dire que le joueur n'a pas encore joué et c'est donc son tour
    if nbO >= nbX:
        return 'X'
    return 'O'

def AquiLeTour_Joueur_commence(grille):
    #on considère que le joueur est celui qui commence le jeu
    #on regarde le nombre de pions en jeu pour chacun
    nbX=0
    nbO=0
    for i in range(6):
        for j in range(12):
            if grille[i][j] == 'X':
                nbX +=1
            if grille[i][j] == 'O':
                nbO += 1

    #s'il y a le même nombre de O et de X, c'est que chacun a joué, on revient donc au début du 'tour' et le joueur commence
    #sinon, c'est que l'IA n'a pas encore joué et c'est donc à son tour
    if nbX >= nbO:
        return 'O'
    return 'X'

def jeu():
    grille=creationGrille()
    quicommence = True if input('Voulez-vous commencer (oui/non)? ').lower() == 'oui' else False

    nbPions=0

    while nbPions <42 and GameIsOver(grille) == 0:

        if quicommence:

            if AquiLeTour_Joueur_commence(grille) == 'O':
                print('A votre tour de jouer')
                printGrille(grille)
                print('Voici la liste des coups possibles: ')
                coupsPossibles=coupsValides(grille)
                for i in range (len(coupsPossibles)):
                    coupsPossibles[i] = coupsPossibles[i]+1
                print(coupsPossibles)
                print('Sur quelle colonne souhaitez-vous jouer ?')
                coupchoisi = input()
                a = int(coupchoisi)-1
                grille=actionJoueur(grille,a,'O')[0]
                printGrille(grille)
                nbPions += 1

            else:
                ActionIA = MiniMaxAlphaBeta(grille, 4, 'X')
                grille=actionJoueur(grille,ActionIA,'X')[0]
                print('Voici l état actuelle du jeu')
                printGrille(grille)
                print("L'IA a joué en ",ActionIA+1)
                nbPions += 1


        else:

            if AquiLeTour_IA_commence(grille) == 'X':
                print('L IA va jouer')
                ActionIA = MiniMaxAlphaBeta(grille, 4, 'X')
                grille=actionJoueur(grille,ActionIA,'X')[0]
                printGrille(grille)
                print("L'IA a joué en ",ActionIA+1)
                nbPions += 1

            else:
                print('A votre tour de jouer')
                printGrille(grille)
                print('Voici la liste des coups possibles: ')
                coupsPossibles=coupsValides(grille)
                for i in range (len(coupsPossibles)):
                    coupsPossibles[i] = coupsPossibles[i]+1
                print(coupsPossibles)
                print('Sur quelle colonne souhaitez-vous jouer ?')
                coupchoisi = input()
                a = int(coupchoisi)-1
                grille=actionJoueur(grille,a,'O')[0]
                printGrille(grille)
                nbPions += 1


    print('Voici l etat final du jeu')
    printGrille(grille)
    if GameIsOver(grille) == 1:
        print('Victoire !')
    elif GameIsOver(grille) == -1:
        print('Défaite !')
    else:
        print('Match nul')

jeu()
































