import phevaluator as phe
import pyCardDeck as pcd
from itertools import product
from copy import deepcopy
from timeit import default_timer as timer

denoms = [str(x) for x in range(2, 10)] + ['T', 'J', 'K', 'Q', 'A']
suits = ['c', 's', 'h', 'd']
all_cards = [denom + suit for denom, suit in product(denoms, suits)]

def sim_hand(my_hand, comm, n_opps, n_sims=16384):
    assert(len(my_hand) == 2)
    assert(len(comm) in range(0, 6))
    assert(len(my_hand) + len(comm) == len(set(my_hand + comm)))
    assert(n_opps > 0)

    n_comm_left = 5 - len(comm)
    is_undealt = lambda card: card not in my_hand and card not in comm
    remaining_cards = [card for card in all_cards if is_undealt(card)]
    deck = pcd.Deck(cards=remaining_cards)

    draw_n = lambda deck, n: [deck.draw() for _ in range(n)]
    eval = lambda hand, comm: phe.evaluate_cards(*(hand + comm))

    wins = 0
    for _ in range(n_sims):
        sim_deck = deepcopy(deck)
        sim_deck.shuffle()
    
        opp_hands = [draw_n(sim_deck, 2) for _ in range(n_opps)]
        sim_comm = comm + draw_n(sim_deck, n_comm_left)
    
        my_score = eval(my_hand, sim_comm)
        best_opp_score = min(eval(opp_hand, sim_comm) for opp_hand in opp_hands)
        wins += my_score < best_opp_score
    return wins / n_sims

start = timer()
result = sim_hand(['2s', '2c'], ['Ad'], 1)
end = timer()

elapsed_ms = (end - start) * 1000
print(f'odds: {result}')
print(f'time elapsed: {elapsed_ms} ms')
