import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Définition de la taille de la fenêtre
TAILLE_FENETRE = (800, 600)

# Chargement des mots à partir du fichier "mots.txt"
with open("mots.txt", "r") as f:
    mots = f.read().splitlines()

# Classe pour le jeu du pendu
class Pendu:
    def __init__(self):
        self.mot = random.choice(mots).upper()
        self.lettres_devinees = []
        self.lettres_incorrectes = []
        self.pendu_images = [
            pygame.image.load("images/pendu0.png"),
            pygame.image.load("images/pendu1.png"),
            pygame.image.load("images/pendu2.png"),
            pygame.image.load("images/pendu3.png"),
            pygame.image.load("images/pendu4.png"),
            pygame.image.load("images/pendu5.png"),
            pygame.image.load("images/pendu6.png")
        ]
        self.etat_pendu = 0

    def deviner(self, lettre):
        lettre = lettre.upper()
        if lettre in self.mot and lettre not in self.lettres_devinees:
            self.lettres_devinees.append(lettre)
        elif lettre not in self.lettres_incorrectes:
            self.lettres_incorrectes.append(lettre)
            self.etat_pendu += 1

    def est_gagne(self):
        return all(lettre in self.lettres_devinees for lettre in self.mot)

    def est_perdu(self):
        return self.etat_pendu == 6

    def afficher(self, fenetre):
        fenetre.fill(BLANC)
        largeur = 20
        hauteur = 100
        font = pygame.font.SysFont(None, 48)
        mot_affiche = ""
        for lettre in self.mot:
            if lettre in self.lettres_devinees:
                mot_affiche += lettre + " "
            else:
                mot_affiche += "_ "
        texte_mot = font.render(mot_affiche, True, NOIR)
        fenetre.blit(texte_mot, (largeur, hauteur))
        texte_lettres = font.render("Lettres incorrectes: " + ", ".join(self.lettres_incorrectes), True, NOIR)
        fenetre.blit(texte_lettres, (largeur, hauteur + 50))
        fenetre.blit(self.pendu_images[self.etat_pendu], (largeur, hauteur + 100))
        pygame.display.update()

# Création de la fenêtre du jeu
fenetre = pygame.display.set_mode(TAILLE_FENETRE)
pygame.display.set_caption("Jeu du Pendu")

# Boucle principale du jeu
while True:
    # Menu du jeu
    print("=== MENU ===")
    print("1. Jouer")
    print("2. Insérer un mot")
    print("3. Quitter")

    choix = input("Choisissez une option : ")
    if choix == "1":
        pendu = Pendu()
        while not pendu.est_gagne() and not pendu.est_perdu():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key >= pygame.K_a and event.key <= pygame.K_z:
                        pendu.deviner(chr(event.key))
            pendu.afficher(fenetre)

        if pendu.est_gagne():
            print("Bravo, vous avez gagné ! Le mot était :", pendu.mot)
        else:
            print("Dommage, vous avez perdu. Le mot était :", pendu.mot)

    elif choix == "2":
        nouveau_mot = input("Entrez un nouveau mot : ")
        with open("mots.txt", "a") as f:
            f.write(nouveau_mot.upper() + "\n")
        print("Le mot a été ajouté avec succès.")

    elif choix == "3":
        pygame.quit()
        sys.exit()

    else:
        print("Option invalide. Veuillez choisir une option valide.")

