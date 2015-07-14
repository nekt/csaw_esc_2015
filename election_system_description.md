Election System Description
===========================

The election system to be attacked is supposedly secure, since it has
been developed by the company you work for, and you were actually
involved in building it; however, being a malicious insider, you
tampered with the overall system security. For confidentiality and
integrity of the election results, the system incorporates the newly
designed "AHE-1" cryptoprocessor that implements **authenticated**
**homomorphic encryption** based on **Paillier cryptosystem** and "AHE"
fast **Message Authentication Code (MAC)** over a sequence of
concatenated ciphertexts, following the **Encrypt-then-MAC** paradigm.
The AHE-1 cryptoprocessor is installed on the central tally server as
well as each election terminal, so that votes for each candidate are
encrypted under an open public key and paired with the candidate unique
id, before the unordered sequence of pairs is concatenated and MAC-ed
under a factory installed/pre-shared secret key. Consequently, these
pairs and the MAC are sent via a broadcasted Ethernet frame to the tally
server for homomorphic accumulation and verification of the MAC. After
all votes are collected, each candidate id will have an encrypted number
corresponding to their votes, and decrypting them using the private key
would reveal the winner. The tally server performs a sanity check to
ensure that the total number of votes corresponds to the number of
voters.

AHE Fast MAC
------------

The fast MAC of a long message **m** is computed using
hash function **H** and a 16-bit pre-shared factory key **k**, by
concatenating **k** with **m** before hashing their combined result with
**H**. Function **H** is constructed using padded Merkle-Damgard
chaining of several instances of one-way compression function **h**, and
a fixed initialization vector **IV** required for the chain head.
Function **h** is defined as **h(h', m') = (((((h' `lshift` 13) `concat`
m') `mod` 524287) + (h' `*` (h' `rshift` 5))) `xor` (m' `lshift` 7)) `mod`
65536**, where **h'** is the chaining variable (i.e. output of the
previous compression function **h** in the chain, or **IV** for the
chain head) and **m'** is a message block of size 16 bits. All
concatenations are applied over binary representations of the
corresponding blocks, while the padding format consists of bit `1`
followed by enough `0` bits to match the block size (dummy blocks are
possible), followed by a 16-bit block representing the *total* number of
blocks (i.e. limited to 65535 blocks).

AHE-1 Trojan 
------------

As an insider, you planned to launch attacks to any
election system using the AHE-1 cryptoprocessor. Specifically, you have
already inserted a hardware Trojan in the implementation of the Paillier
KeyGen algorithm within AHE-1 of the tally server, so that it generates
weak keypairs. The Trojan actually affects the size of the prime numbers
used to generate the keypair, and they have weak sizes anywhere between
16 and 28 bits each, instead of secure sizes of at least 512 bits each.

Ethernet frame format
---------------------

The Ethernet frame is broadcast to Media
Access Control address `ff:ff:ff:ff:ff:ff`, and its **payload** (data)
is an unordered concatenated sequence of pairs of candidate ids and
encrypted vote counts, followed by the **AHE Fast MAC** of the
concatenation of all previous sequence pairs. Each pair is delimited by
start/finish 16 bit values, and any bytes outside any delimited pairs
are ignored. The tally server would also accept Ethernet frames where
not all candidate ids are included at once. Each candidate id is a
random 16 bit value assigned to each candidate.
