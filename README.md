

Project 3: Better, Smarter, Faster 16:198:520

Consider the same environment as in Project 2 - a circle of 50 nodes, with random edges. Again we have the predator,

the agent, and the prey. The prey transitions as before, choosing a neighbor at random each time it moves. The

predator transitions in accordance with the Distracted Predator Model from the previous project. In this project,

we want to build an agent that captures the prey as eﬃciently as possible.

How many distinct states (conﬁgurations of predator, agent, prey) are possible in this environment?

For a given state s, let U∗(s) be the minimal expected number of rounds to catch the prey for an optimal agent,

assuming movement order as in Project 2.

• What states s are easy to determine U∗ for?

• How does U∗(s) relate to U∗ of other states, and the actions the agent can take?

Write a program to determine U∗ for every state s, and for each state what action the algorithm should take. Describe

your algorithm in detail.

• Are there any starting states for which the agent will not be able to capture the prey? What causes

this failure?

• Find the state with the largest possible ﬁnite value of U∗, and give a visualization of it.

• Simulate the performance of an agent based on U∗, and compare its performance (in terms of steps to

capture the prey) to Agent 1 and Agent 2 in Project 2. How do they compare?

• Are there states where the U∗ agent and Agent 1 make diﬀerent choices? The U∗ agent and Agent 2?
 Visualize such a state, if one exists, and explain why the U∗ agent makes its choice.

Build a model to predict the value of U∗(s) from the state s. Call this model V .

• How do you represent the states s as input for your model? What kind of features might be relevant?

• What kind of model are you taking V to be? How do you train it?

• Is overﬁtting an issue here?

• How accurate is V ?

Once you have a model V , simulate an agent based on the values V instead of the values U∗.

How does its performance stack against the U∗ agent?

In Project 2, we were also interested in the partial information situation, where we may not know exactly where the

prey or predator is. Consider the unknown prey position case - here, the state of the agent may be represented by

the position of the agent, the position of the predator, and a vector of probabilities p. Because there are inﬁnite

possible belief states, the optimal utility is hard to solve for. In this case, we might estimate the utility of a given

state as the expected utility based on where the prey might be.

Upartial(sagent, spredator, p) = X

ps

prey U∗(sagent, spredator, sprey). (1)

sprey

1




<a name="br2"></a>Computer Science Department - Rutgers University Spring 2019

` `Simulate an agent based on Upartial, in the partial prey info environment case from Project 2, using the
values of U∗ from above. How does it compare to Agent 3 and 4 from Project 2? Do you think this partial information agent is optimal?

Build a model Vpartial to predict the value Upartial for these partial information states. Use as the training data states

(including belief states) that actually occur during simulations of the Upartial agent.

• How do you represent the states s

agent, spredator, p as input for your model? What kind of features might

be relevant?

• What kind of model are you taking Vpartial to be? How do you train it?

• Is overﬁtting an issue here? What can you do about it?

• How accurate is Vpartial? How can you judge this?

• Is Vpartial more or less accurate than simply substituting V into equation [(1)?](#br1)

• Simulate an agent based on V

partial. How does it stack against the Upartial agent?

Bonus:

• Bonus 1: Build a model to predict the actual utility of the U

partial agent. Where are you getting your

data, and what kind of model are you using? How accurate is your model, and how does its predictions

compare to the estimated Upartial values?

• Bonus 2: Build an optimal partial information agent.

2
