

Project 3: Better, Smarter, Faster 16:198:520

Developed an agent to efficiently capture prey in a graph environment using 𝐝𝐲𝐧𝐚𝐦𝐢𝐜 𝐩𝐫𝐨𝐠𝐫𝐚𝐦𝐦𝐢𝐧𝐠 to compute optimal utility "U*" for all possible states. 

Represented the environment as an adjacency matrix and precomputed distances using 𝐅𝐥𝐨𝐲𝐝-𝐖𝐚𝐫𝐬𝐡𝐚𝐥𝐥 algorithm. 

Computed U* values through value iteration, modeling transition probabilities, and rewards. 

The "U*" agent chooses actions that minimize utility to efficiently navigate toward the prey while avoiding the predator. Also, trained neural network models "V" and "Vpartial" to predict utility values and implemented agents "V*" and "Vpartial" using these models. "V" achieves 97% success rate in 16.78 steps on average. For partial prey information, modeled the belief array but faced overfitting issues. Instead took the most likely prey position, improving the success rate to 94% in 32 steps. Overall, the "U*" agent using true utility values performs best, but the models can approximate utilities for efficient prey capture in this environment.
