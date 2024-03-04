import random
from connect_3_classes import connect_three_board
random.seed(42)
def evaluate_agent(trained_agent, eval_episodes):
    total_reward = 0
    losses = 0
    env = connect_three_board()
    for episode in range(eval_episodes):
        state = str(env.board.flatten().tolist())
        while True:
            # perceive state & available actions
            available_actions = env.get_available_actions()
            # print("Available actions:", available_actions)
            # print(f"Current player:{env.current_player}")
            # agent's turn
            if env.current_player == 1:
                action = trained_agent.choose_action(state, available_actions)
                env.apply_action(action)
                # print(f"Action taken:{action}")
            # opponent's turn
            elif env.current_player == -1:
                opponent_action = random.choice(available_actions)
                env.apply_action(opponent_action)
                # print(f"Action taken:{opponent_action}")

            # check if end-state reached
            if (len(env.get_available_actions()) == 0) or (env.check_winner() != 0):
                #print("Game ended. Winner:", env.check_winner())
                if env.check_winner() == 1:
                    total_reward += 1
                elif env.check_winner() == -1:
                    total_reward -= 1
                    losses+=1
                env.reset()  # begin new game
                break
            next_state = str(env.board.flatten().tolist())
            state = next_state
            env.current_player = -env.current_player

    average_loss_rate = losses / eval_episodes
    average_total_reward = total_reward / eval_episodes
    #print(f"Average Loss Rate: {average_loss_rate * 100:.2f}%")
    #print(f"Average Total Reward: {average_total_reward:.2f}")
    #print(f"Q-Table:{trained_agent.q_table}")
    return average_loss_rate




