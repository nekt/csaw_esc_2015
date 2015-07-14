CSAW 2015 Embedded Security Challenge (Phase 1)
==============================================

Challenge Overview
------------------

For this year's ESC competition you will play the role of an
**attacker**, and your goal is to **overthrow an election** by altering
the results in your favor. To do so, you will impersonate an election
terminal using an **embedded system** and launch a **real attack to the
weakened cryptographic security of the election system.** The election
system uses **homomorphic encryption** to accumulate votes, and your
objective is to deceive the central tally service responsible for
counting those votes as well as deciding the election winner. Your
mission is to modify the final tally count and elect your favorable
candidate.

The challenge will be is divided into **two phases**.

-   In the **first phase** you will compile a written report where you
    will elaborate on your cryptanalysis of the system and describe your
    strategy and tactics to deceive the tally server, in order to ensure
    that your favorite candidate will win the election. You must be very
    specific on the cryptanalysis of the provided [election system
    description](election_system_description.md), 
    as well as how you will use this cryptanalysis to
    develop an embedded system that will send frames to the tally server
    with deceiving information to alter the election result in
    your favor. The components and functionality of the modules in your
    embedded system should also be described in detail. Your designs
    must be **area-constrained** for `Nexys 4` FPGAs and optimized for
    performance, as the latter will be a major metric to determine the
    challenge winner.

-   All first phase reports will be evaluated for their merit by a team
    of judges, and each will be assigned a score based on **correctness**,
    **potential**, **novelty** and **performance optimizations**. The 10 best teams
    will move forward to the second phase.

-   Details about the **second phase** will be announced together with
    the first phase finalists.

