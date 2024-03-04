from connect_3_classes import agent, connect_three_board
import connect_3_classes
from evaluate import evaluate_agent
import random
random.seed(42)

def q_learn(agent, episodes = 10000):
    env = connect_three_board()
    avg_loss_rates = []
    avg_win_rates = []

    for episode in range(episodes):
        state = str(env.board.flatten().tolist())
        while True:
            #perceive state & available actions
            available_actions = env.get_available_actions()

            #agent's turn
            if env.current_player==1:
                action = agent.choose_action(state, available_actions)
                pre_agent_state = str(env.board.flatten().tolist())
                env.apply_action(action)
                post_agent_state = str(env.board.flatten().tolist())

            #opponent's turn
            elif env.current_player==-1:
                opponent_action = random.choice(available_actions)
                env.apply_action(opponent_action)
                post_opponent_state = str(env.board.flatten().tolist())


            #Update Q-value at endstate
            if (len(env.get_available_actions()) == 0) or (env.check_winner() != 0):
                #print("Game ended. Winner:", env.check_winner())
                if env.check_winner() == 1:
                    reward = 1
                    agent.update_q_value(pre_agent_state, action, reward, post_agent_state)
                elif env.check_winner()==-1:
                    reward = -1
                    agent.update_q_value(pre_agent_state, action, reward, post_opponent_state)
                else: #draw
                    reward = 0.6
                    if env.current_player == -1:
                        agent.update_q_value(pre_agent_state, action, reward, post_opponent_state)
                    elif env.current_player ==1:
                        agent.update_q_value(state, action, reward, post_agent_state)

                env.reset() #begin new game
                break

            # Update Q-value at in-between-states

            if env.current_player == -1:
                reward = 0.0  # No reward for in-between-states
                agent.update_q_value(pre_agent_state, action, reward, post_opponent_state)
            env.current_player = -env.current_player

        #perform evaluation
        if episode % 50 ==0:
            current_q_table = agent.q_table
            current_agent_non_random = connect_3_classes.agent(exp_rate=0, q_table=current_q_table)
            avg_win_rate, average_loss_rate = evaluate_agent(current_agent_non_random, eval_episodes=1000)
            print(f"Episode: {episode}, Average win Rate: {avg_win_rate * 100:.2f}%")
            print(f"Episode: {episode}, Average loss Rate: {average_loss_rate * 100:.2f}%")
            avg_win_rates.append((avg_win_rate * 100))
            avg_loss_rates.append((average_loss_rate * 100))
            # update rates
            agent.exp_rate = agent.exp_rate * 0.99
            agent.learn_rate = agent.learn_rate * 0.99

    print(f"episodes simulated:", episode)

    return agent.q_table, avg_win_rates, avg_loss_rates




