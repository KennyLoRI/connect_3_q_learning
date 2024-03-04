from connect_3_classes import agent, connect_three_board
import connect_3_classes
from evaluate import evaluate_agent
import random
random.seed(42)

def q_learn(agent, episodes = 10000):
    env = connect_three_board()
    avg_loss_rates = []

    for episode in range(episodes):
        state = str(env.board.flatten().tolist())
        while True:
            #perceive state & available actions
            available_actions = env.get_available_actions()
            #print("Available actions:", available_actions)
            #print(f"Current player:{env.current_player}")
            #agent's turn
            if env.current_player==1:
                action = agent.choose_action(state, available_actions)
                env.apply_action(action)
                #print(f"Action taken:{action}")
            #opponent's turn
            elif env.current_player==-1:
                opponent_action = random.choice(available_actions)
                env.apply_action(opponent_action)
                #print(f"Action taken:{opponent_action}")

            #Update Q-value at endstate
            if (len(env.get_available_actions()) == 0) or (env.check_winner() != 0):
                #print("Game ended. Winner:", env.check_winner())
                if env.check_winner() == 1:
                    reward = 1
                    next_state = str(env.board.flatten().tolist())
                    agent.update_q_value(state, action, reward, next_state)
                elif env.check_winner()==-1:
                    reward = -1
                    agent.update_q_value(previous_state, action, reward, state)
                else: #draw
                    reward = 0.5
                    if env.current_player == -1:
                        agent.update_q_value(previous_state, action, reward, state)
                    elif env.current_player ==1:
                        next_state = str(env.board.flatten().tolist())
                        agent.update_q_value(state, action, reward, next_state)

                env.reset() #begin new game
                break

            # Update Q-value at in-between-states
            next_state = str(env.board.flatten().tolist())
            if env.current_player == 1:
                reward = 0.14  # No reward for in-between-states
                agent.update_q_value(state, action, reward, next_state)
            env.current_player = -env.current_player
            previous_state = state
            state = next_state
        #print(f"episode:{episode}")
        agent.exp_rate = 1/(1+0.0001*episode)
        agent.learn_rate = 1/(1+0.0001*episode)
        if episode % 100 ==0:
            current_q_table = agent.q_table
            current_agent_non_random = connect_3_classes.agent(exp_rate=0, q_table=current_q_table)
            avg_loss_rate = evaluate_agent(current_agent_non_random, eval_episodes=1000)
            print(f"Episode: {episode}, Average Loss Rate: {avg_loss_rate * 100:.2f}%")
            avg_loss_rates.append((avg_loss_rate * 100))

    print(f"episodes simulated:", episode)

    return agent.q_table, avg_loss_rates




