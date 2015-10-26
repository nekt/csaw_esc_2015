##Finalists are announced [here](esc2015_finalists.md)

CSAW 2015 Embedded Systems Challenge (Phase 2)
==============================================

Phase 2 Instructions
====================

In the second phase you will be asked to use a Nexys 4 DDR Artix-7
FPGA board to develop your embedded system in HDL and demonstrate
your attack by sending malicious Ethernet frames. In preparation for
the finals, you will also get black box access to a demo software
simulator of the election system, covering the central tally server
functionality over different message sequences from
election terminals (staging server `http://52.89.227.26:5000` -- *you 
are not allowed to launch DoS on the server or perform web attacks*). 
Your goal in this challenge is to launch your
attack using the Nexys board as quickly as possible, after observing
a limited number of frames in each scenario, and the software
simulator would allow testing your attack methods beforehand. The
final winners will be determined based on the following criteria:

-   **Correctness**: The attack successfully overthrows the election
	result and a chosen candidate wins; without the attack a
	different candidate would have won, based on the frames from the
	legitimate election terminals. The tally server should not
	encounter an incorrect Message Authentication Code, a malformed
	message or an abnormally high total number of votes. These
	issues are detected by the tally server and the corresponding
	attacks would fail. The system presents a number of legitimate
	messages that correspond to almost all possible human voters,
	and without intervention it elects an unfavorable candidate; you
	are asked to modify the election result under different random
	combinations (scenarios) of legitimate messages.

-   **Performance**: For the finals you will be asked to demonstrate
	the attack live, using a Nexys 4 DDR FPGA, by launching a
	malicious Ethernet frame, after observing a given sequence of
	legitimate frames. Your goal is to send the malicious frame(s)
	that alter(s) the results *as soon as possible*; if multiple
	frames are send, the timings of the last frame sent would
	determine performance. The sequence of legitimate frames will be
	generated at the same rate and the number of frames will be
	different in each scenario, as well as the Paillier security
	parameters, secret MAC keys, IVs and maximum number of
	human voters.

-   **Novelty**: The teams are asked to implement their attacks in HDL
	and employ novel strategies and performance optimizations in
	their implementations. The creativity of the solutions and
	sophistication of the used algorithms will be used to evaluate
	this criterion by a team of judges.

-   **Report**: The quality of each team’s final report, describing at
	least the implementation details of the attack and the
	corresponding cryptanalysis of the system will be assessed by
	the judges. In addition, the teams are asked to prepare a poster
	for interactive presentations and a 5 minute powerpoint
	slideshow to be presented to a wide audience. The report and
	related material should elaborate on the attack against the
	election system, as well as evaluation and theoretical support
	for the proposed methods.

*Note*: If participants choose to use third party IP cores along with their own HDL code, 
all such cores should be available to anyone cost-free. Using paid IP cores and 
cores that require a paid license or a demo license is not allowed.

Points distribution
-------------------

For this challenge, the most important metric is performance, which
corresponds to 35% of the total points received, while the correctness
and novelty will be 25% each; the report will be 15% of the total
points. For correctness, the team(s) that will be able to overthrow 100%
of the election scenarios presented to them will get maximum points in
that category, and grading will be proportional to the number of such
solved scenarios (no points for the teams not overthrowing any election
scenario). In terms of performance, the first/fastest team will receive
maximum points, while the remaining teams will receive points decreasing
linearly based on their ranking, with the last team receiving no points.
Both performance and correctness will be assessed automatically by a
computer.

In terms of novelty, a team of industry experts/judges will assess each
team by ranking their solution among the different solutions applicable
to the challenge. Maximum points will be given to the team(s) that
implementing the most novel and efficient approach, or demonstrate new
and powerful methods to solve the challenge using hardware. Detailed
score metrics will be revealed after the competition, as not to reveal
potential solutions. Finally, regarding the report, teams will be
evaluated by the same team of judges, who will assess the technical
content of the reports the level of elaboration and the overall
presentation of the material. Additional points will we awarded to the
team(s) that will have experimental evidence to support their
performance results/optimizations and comparisons with less efficient
attack methods. Finally, bonus points will be awarded to the team(s)
that provide detailed analysis of all vulnerabilities introduced to the
provided election system description and theoretical proof on how such
vulnerabilities can be exploited.

Attack Specifications
=====================

The attacks will be launched using a Nexys 4 DDR FPGA board connected to
a tally server through a network switch and standard Ethernet cables.
The tally server will be simulated by a PC, and will follow the
published specifications and the functionality of the provided black-box
demo simulator; in addition, another PC will broadcast simulated
messages from legitimate election terminals that can reach both the
tally server and the Nexys 4 DDR FPGA. The only communication interface
between the tally server and the FPGA will be the Ethernet cable and the
network switch. For our software simulators, the following Paillier
implementation has been chosen: `github.com/mikeivanov/paillier`
with weakened key sizes.

The Ethernet frames will use Ethernet II (DIX) framing (without IEEE
802.1Q), which consists of 6 bytes for the destination address, 6 bytes
for the source address, 2 bytes for the type (assumed `0x0800`) and at
least 46 bytes of data (up to 1500). As part of the payload, each frame
from the election terminals includes the public security parameter N
that was used for encryption; this allows all nodes to verify that the
same keys are used by all terminals. The frame payload is defined as
follows: `SECPARAM` `PAIR` ignored\_bytes `PAIR` ignored\_bytes ... `MAC`. The
`SECPARAM` is Paillier’s parameter `N` prepended with zeros to 56 bits. Each
`PAIR` consists of a 2 byte start sequence `0x2b02`, a 2 byte candidate ID
(e.g. `0x2db1`), encrypted votes zero padded to 14 bytes (e.g.
`0x00000000003d93303be639e9259a`), and a 2 byte end sequence `0x2cce`.
Refer to [sample_recv.py](sample_recv.py) to verify that the Ethernet frames 
generated by Nexys 4 DDR are received correctly by the simulator; a sample 
program output for frames containing encrypted vote pairs is provided 
[here](sample_recv.out).

The relative order of `PAIR`s does not matter. Between `PAIR`s (after the
end sequence and before a start sequence) bytes that do not include the
start sequence are ignored. The last 2 bytes of the payload are always a
Message Authentication Code (MAC). The `MAC` is computed over the bits
corresponding to the `PAIR`s and ignored bytes (but not `SECPARAM`), subject
to padding (bit `1` followed by bit `0`s) to ensure 2 byte alignment and a
block counting the total blocks. The key and the data bits are first
concatenated before padding and block counting is applied. A dummy block
is inserted before the counting block when the original message aligns
exactly. The padding and block count are used only to compute the MAC
and are not actually transmitted. The initialization vector and the key
for the MAC are not revealed and the teams are expected find ways to
work around this limitation, and still pass the MAC verification checks.

Election terminals can send any amount of votes at any time: they can
choose to send their local accumulations at the once (e.g. at the end of
elections day) or send only differential votes periodically reflecting
the local votes added since the last message from that terminal. In both
cases, the tally server does not identify election terminals based on
their address. The encrypted votes in the system are accumulated by the
server using the additive property of Paillier. The plaintext numbers
representing votes are not encoded in any way before being encrypted,
and the tally server accumulates the votes directly without decrypting
the contents until the moment that the winner is announced. At that
point, the tally server checks if the total decrypted votes distributed
to the candidates are less than the maximum population of voters known
to the server beforehand. For this challenge, teams should expect that
the simulated elections have very high participation rates, so the
legitimate votes sent to the server are very close to the size of the
voter population.

The server validates the payload size in bytes (i.e.>= 46,
<=1500), the `SECPARAM`, the `MAC`, the start/end sequences of `PAIR`s and ignores
reappearing `PAIR`s for the same candidate ID in the same frame, other
than the first one (i.e. IDs are accounted only once per frame). At the
end of the elections, the server declares the winner by decrypting all
votes. If two winners share the same number of votes (i.e. there is a
tie) the server cannot declare one winner (note that your goal is to
deceive the system into electing one chosen candidate). The tally server
accepts frames that do not include all the candidate IDs and have only a
few of them; such frames should be expected in this competition, as
terminals can choose to send differential votes.

Administrative
==============

Each team is kindly asked to order a Nexys 4 DDR FPGA
(`digilentinc.com/nexys4ddr` - academic pricing) to be able to
participate at the competition (all teams should use the same hardware).
Each team can either keep the board afterwards or return it in good
condition to be reimbursed by NYU School of Engineering for this expense
(subject to 2-6 weeks processing time). Teams will be asked to complete
a W9 form and submit it along with all original invoices associated with
the purchase to NYU for processing. The CSAW ESC organizers through the
NYU Travel Agents will also arrange and cover the travel expenses, meal
plan and 2-night accommodation for one member of each participating team
to travel to NYC from within the US; the traveling member from each team
is also asked to register for WorldStrides Capstone Program (for trip ID
details please contact the challenge leaders).

The final report along with all the HDL code and files necessary to
program the Nexys 4 DDR board are due **November 8, 2015**. 
The teams are expected to be ready to demonstrate the correctness and
performance of their attacks on the day of the finals. The teams will
also participate in a poster session and a 5 minute auditorium
presentation where they will present their work.
