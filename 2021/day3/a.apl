#!/usr/local/bin/apl --script

m ← ⎕FIO[49] 'input.dat'
g ← ∊500<+/'1'=m
e ← ~g
⎕ ← ×/2⊥¨g e

)OFF
