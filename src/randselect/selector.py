import random

def random_selection(n_list, q_list):
  
  chosen_name = random.choice(n_list)
  chosen_question = random.choice(q_list)

  return (chosen_name, chosen_question)