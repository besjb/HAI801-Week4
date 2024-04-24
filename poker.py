import numpy as np
import random
from collections import Counter
from itertools import combinations

# Define the deck of cards
suits = ['H', 'D', 'C', 'S']  # Hearts, Diamonds, Clubs, Spades
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Create a full deck
deck = [(rank, suit) for suit in suits for rank in ranks]

# Function to determine the best poker hand from a set of seven cards
def evaluate_poker_hand(cards):
    # Generate all possible 5-card combinations from the set of 7 cards
    possible_hands = list(combinations(cards, 5))
    
    # Evaluate the best hand
    best_score = 0
    for hand in possible_hands:
        score = fitness(hand)
        if score > best_score:
            best_score = score
            
    return best_score

# Basic fitness function for poker hand evaluation
def fitness(hand):
    # Evaluate the strength of a 5-card poker hand
    rank_counts = Counter([card[0] for card in hand])
    suits = Counter([card[1] for card in hand])

    # Determine hand rank based on poker rules
    is_flush = any(count >= 5 for count in suits.values())
    is_straight = is_straight_flush(rank_counts.keys())
    
    if is_straight and is_flush:
        return 1000  # Straight flush or royal flush
    elif len([count for count in rank_counts.values() if count >= 4]) >= 1:
        return 800  # Four of a kind
    elif len([count for count in rank_counts.values() if count >= 3]) >= 1 and len([count for count in rank_counts.values() if count >= 2]) >= 2:
        return 700  # Full house
    elif is_flush:
        return 600  # Flush
    elif is_straight:
        return 500  # Straight
    elif len([count for count in rank_counts.values() if count >= 3]) >= 1:
        return 400  # Three of a kind
    elif len([count for count in rank_counts.values() if count >= 2]) >= 2:
        return 300  # Two pairs
    elif len([count for count in rank_counts.values() if count >= 2]) >= 1:
        return 200  # One pair
    else:
        # High card (sum of card values)
        return sum([card_value(rank) for rank in rank_counts.keys()])

# Helper function to check if a set of ranks forms a straight
def is_straight_flush(ranks):
    rank_values = sorted([card_value(rank) for rank in ranks])
    # Check if there's a sequence of five consecutive card values
    for i in range(len(rank_values) - 4):
        if rank_values[i:i+5] == list(range(rank_values[i], rank_values[i] + 5)):
            return True
    return False

# Get card value for fitness calculation
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

# Create initial population
def create_population(size):
    population = []
    for _ in range(size):
        individual = random.sample(deck, 7)  # Two hole cards and five community cards
        population.append(individual)
    return population

# Crossover operation
def crossover(parent1, parent2):
    # Simple crossover by combining hole cards from one parent and community cards from another
    child = parent1[:2] + parent2[2:7]
    return child

# Mutation operation
def mutation(individual, mutation_rate):
    if random.random() < mutation_rate:
        index = random.randint(0, len(individual) - 1)  # Choose a card to replace
        new_card = random.choice(deck)
        individual[index] = new_card
    return individual

# Selection based on fitness
def select_parents(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    pick = random.uniform(0, total_fitness)
    current = 0
    for idx, score in enumerate(fitness_scores):
        current += score
        if current > pick:
            return population[idx]

# Genetic algorithm implementation
def genetic_algorithm(population_size, generations, mutation_rate):
    population = create_population(population_size)
    
    for generation in range(generations):
        fitness_scores = [evaluate_poker_hand(individual) for individual in population]
        
        # Generate new population with crossover and mutation
        new_population = []
        while len(new_population) < population_size:
            parent1 = select_parents(population, fitness_scores)
            parent2 = select_parents(population, fitness_scores)
            child = crossover(parent1, parent2)
            child = mutation(child, mutation_rate)
            new_population.append(child)
        
        population = new_population  # Update population
        
        # Display best fitness in the current generation
        best_fitness = max(fitness_scores)
        print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")

    # Return the best individual from the final population
    best_index = np.argmax([evaluate_poker_hand(individual) for individual in population])
    return population[best_index]

# Parameters for the genetic algorithm
population_size = 20
generations = 50
mutation_rate = 0.1

# Run the genetic algorithm
best_hand = genetic_algorithm(population_size, generations, mutation_rate)
print(f"Best Texas Hold'em hand after {generations} generations: {best_hand}")
