from connect_3_classes import agent
from q_learn import q_learn
from evaluate import evaluate_agent
import random
import matplotlib.pyplot as plt

# Train the agent
random.seed(42)
exploration_and_learn = 1/(1+0.0001)
best_agent = agent(exp_rate=exploration_and_learn, learn_rate=exploration_and_learn, discount_rate=0.95)
learned_q_table, avg_loss_rates = q_learn(best_agent, episodes=2000)
learned_best_agent = agent(exp_rate=0, q_table=learned_q_table)
evaluate_agent(learned_best_agent, eval_episodes=1000)

#plot training procedure
def plot_losses(losses, save_path = None):
    episodes = [i * 100 for i in range(len(losses))]
    plt.plot(episodes, losses, label='% of lost games playing 1000 evaluation games')
    plt.xlabel('Episodes')
    plt.ylabel('%Loss')
    plt.title('%Loss Over Episodes')
    plt.legend()
    plt.show()

# Assuming you have a list of average loss rates called 'average_losses'
plot_losses(avg_loss_rates)




