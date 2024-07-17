# Random Number Generator Code : Javascript V8 Engine
# Algorithum : XORShift128+ 

import z3
import struct

# Chrome Console : Array.from(Array(5), Math.random)

seq = [0.05531733875967171, 0.22772625785305145, 0.8329979038576423, 0.5288711078891453, 0.7764529681862142]
seq = seq[::-1]

s = z3.Solver()
p_state0, p_state1 = z3.BitVecs("p_state0 p_state1", 64)

for i in range(len(seq)):
    p_s0 = p_state1
    p_s1 = p_state0
    p_state0 = p_s0
    p_s1 ^= p_s1 << 23
    p_s1 ^= z3.LShR(p_s1, 17)
    p_s1 ^= p_s0
    p_s1 ^= z3.LShR(p_s0, 26)
    p_state1 = p_s1

    float64 = struct.pack("d", seq[i]+1)
    u64 = struct.unpack("<Q", float64)[0]
    mantissa = u64 & ((1 << 52)-1)
    s.add(int(mantissa) == z3.LShR(p_state0, 12))

if s.check() == z3.sat:
    model = s.model()

    states = {}
    for state in model.decls():
        states[state.__str__()] = model[state]
    state0 = states["p_state0"].as_long()

    u64 = (state0 >> 12) | (0x3FF0000000000000)
    float_64 = struct.pack("<Q", u64)
    prediction = struct.unpack("d", float_64)[0]
    prediction -= 1
    print(prediction)
