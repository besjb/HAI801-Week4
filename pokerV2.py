import random
from itertools import combinations
from collections import Counter

# Définition des valeurs et des couleurs
suits = ['H', 'D', 'C', 'S']  # Coeurs, Carreaux, Trèfles, Piques
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Génération de la totalité du deck de cartes
full_deck = [(rank, suit) for suit in suits for rank in ranks]

# Fonction pour évaluer la force d'une main de poker
def evaluate_poker_hand(hand):
    rank_counts = Counter([card[0] for card in hand])
    suits = Counter([card[1] for card in hand])

    # Classement des mains (des plus faibles aux plus fortes)
    if is_straight_flush(sorted(rank_counts.keys()), suits):
        return 1000  # Quinte flush
    elif len([c for c in rank_counts.values() if c == 4]) >= 1:
        return 800  # Carré
    elif len([c for c in rank_counts.values() if c == 3]) >= 1 and len([c for c in rank_counts.values() if c == 2]) >= 1:
        return 700  # Full House
    elif any(c >= 5 for c in suits.values()):
        return 600  # Couleur
    elif is_straight(sorted(rank_counts.keys())):
        return 500  # Quinte
    elif len([c for c in rank_counts.values() if c == 3]) >= 1:
        return 400  # Brelan
    elif len([c for c in rank_counts.values() if c == 2]) >= 2:
        return 300  # Deux Paires
    elif len([c for c in rank_counts.values() if c == 2]) >= 1:
        return 200  # Une Paire
    else:
        return 100  # Carte Haute

# Fonction pour vérifier si une main forme une quinte
def is_straight(ranks):
    rank_values = sorted([card_value(rank) for rank in ranks])
    return any(rank_values[i:i + 5] == list(range(rank_values[i], rank_values[i] + 5)) for i in range(len(rank_values) - 4))

# Fonction pour vérifier une quinte flush
def is_straight_flush(ranks, suits):
    if not any(s >= 5 for s in suits.values()):
        return False
    
    # Vérifie si une quinte est formée avec la même couleur
    for suit in suits:
        same_suit_cards = sorted([card_value(rank) for rank, s in ranks if s == suit])
        if any(same_suit_cards[i:i + 5] == list(range(same_suit_cards[i], same_suit_cards[i + 5])) for i in range(len(same_suit_cards) - 4)):
            return True
    return False

# Fonction pour obtenir la valeur d'une carte
def card_value(rank):
    if rank.isdigit():
        return int(rank)
    elif rank == 'J':
        return 11
    elif rank == 'Q':
        return 12
    elif rank == 'K':
        return 13
    elif rank == 'A':
        return 14

# Fonction pour générer une population initiale
def generate_population(population_size):
    population = []
    for _ in range(population_size):
        hand = random.sample(full_deck, 5)
        population.append(hand)
    return population

# Fonction de fitness pour évaluer la force d'une main
def fitness(hand):
    return evaluate_poker_hand(hand)

# Fonction pour croiser deux individus
def crossover(parent1, parent2):
    # Croise deux mains pour créer un nouvel individu
    child = list(set(parent1[:3] + parent2[3:]))
    while len(child) < 5:
        remaining_cards = [card for card in full_deck if card not in child]
        child.append(random.choice(remaining_cards))
    return child

# Fonction de mutation
def mutate(hand):
    if random.random() < 0.1:  # Mutation avec une probabilité de 10%
        card_to_mutate = random.choice(hand)
        new_card = random.choice([card for card in full_deck if card not in hand])
        hand.remove(card_to_mutate)
        hand.append(new_card)
    return hand

# Fonction de sélection
def selection(population):
    # Tri de la population par fitness et sélection des meilleurs individus
    population.sort(key=lambda hand: fitness(hand), reverse=True)
    return population[:len(population)//2]

# Fonction pour exécuter l'algorithme génétique
def genetic_algorithm(population_size, generations):
    # Génération de la population initiale
    population = generate_population(population_size)

    for _ in range(generations):
        # Sélection des meilleurs individus
        selected_population = selection(population)

        # Création d'une nouvelle population par croisement
        new_population = []
        while len(new_population) < population_size:
            parent1 = random.choice(selected_population)
            parent2 = random.choice(selected_population)
            child = crossover(parent1, parent2)
            child = mutate(child)  # Mutation aléatoire
            new_population.append(child)

        population = new_population

    # Retourne le meilleur individu de la population finale
    best_individual = selection(population)[0]
    return best_individual

# Exécution de l'algorithme génétique
best_hand = genetic_algorithm(100, 50)
print("Meilleure main:", best_hand)
print("Score:", evaluate_poker_hand(best_hand))
