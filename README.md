# FaB-DistAlgo
This is a DistAlgo implementation of Fast Byzantine Paxos.

Fast Byzantine Consensus, proposed by Martin et al. was one of the first byzantine consensus algorithms which reach consensus in two communication steps.

In the paper, they introduce three things:

1. Fast Byzantine (or FaB) Paxos, a Byzantine consensus protocol that completes in two communication steps in the common case. FaB Paxos requires 5f + 1 acceptors and tolerates f Byzantine faults.
2. A generalization of FaB Paxos—Parameterized FaB (PFaB) Paxos—that requires 3f + 2t + 1 acceptors to tolerate f Byzantine failures and is two-step as long as at most t acceptors fail.
3. FaB Paxos and Parameterized FaB Paxos are tight in the sense that they use the minimal number of processes required for two-step protocols.
However, several years later, researchers Ittai Abraham et al. in their 2017 paper "Revisiting Fast Practical Byzantine Fault Tolerance", discuss about the shortcomings of two algorithms, "Zyzzyva" and "Fast Byzantine Paxos", while trying to achieve 'optimism'.

In the second section of their paper, they discuss a possible scenario where a liveness violation occurs in PFaB.

Our main idea is to design implementation for the pseudocode given in the paper, identify and reproduce this liveness violation in our implementation and identify possible ways to fix it.

Links:

Fast Byzantine Paxos - http://www.cs.cornell.edu/lorenzo/papers/Martin06Fast.pdf
Revisiting Fast Practical Byzantine Fault Tolerance - https://arxiv.org/pdf/1712.01367.pdf

