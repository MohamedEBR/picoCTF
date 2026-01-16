def unscramble(L):
  A = L

  # undo scramble until no more "history markers" exist
  while True:
    j = None

    # find the rightmost element that ends with a list (the history marker)
    for k in range(len(A) - 1, -1, -1):
      if isinstance(A[k][-1], list):
        j = k
        break

    # no markers -> fully unscrambled
    if j is None:
      break

    # 1) undo: A[j].append(A[:i-2])
    A[j].pop()

    # 2) undo: A[j-1] += A.pop(j)
    last_hex = A[j - 1].pop()   # get back the last merged hex string
    A.insert(j, [last_hex])     # re-insert as its own [hex]

  # convert [[ "0x70" ], [ "0x69" ], ...] -> "pi..."
  return "".join(chr(int(item[0], 16)) for item in A)


x = open("example.txt", "r").read()
print(unscramble(eval(x)))