# WriteUp

When I first ran the `nc` command, it printed a huge nested list full of hex values. At first it looked intimidating, but the challenge gives the Python source code, so the best move was to reverse engineer the logic instead of guessing.


## What the challenge does

The encryption has **two steps**:


### 1) Convert the flag into hex per character

`get_flag()` reads `flag.txt`, then converts each character into a hex string:

```py
hex_flag.append([str(hex(ord(c)))])
```

So the flag becomes a list like this:

```
[['0x70'], ['0x69'], ['0x63'], ...]
```

Each element is a list containing one hex string

---

### 2) Scramble the list structure

Then scramble() repeatedly modifies the list:

```py
A[i-2] += A.pop(i-1)
A[i-1].append(A[:i-2])
```


That means for each loop:

It removes the element at index (i-1) using pop()

Then concatenates it onto the element at (i-2)

Then it stores a copy of the earlier prefix A[:i-2] inside A[i-1] as a "history marker"

This creates a weird nested structure that looks “quantum” but is really just list operations.

--- 

### Reversing the scramble (Unscrambling)

To decode the flag, we reverse each scramble step in the opposite order.

### Key observation

Every loop in scramble() adds a history marker:

```py
A[i-1].append(A[:i-2])
```

So in the scrambled output, some elements end with a list inside them, like:

```py
['0x6e', [...some list...]]
```


That last list is the marker that tells us this element was affected by scrambling.

---

### How the reverse works

To undo one scramble step, we reverse the two operations in reverse order:

### Step 1: Undo the .append(A[:i-2])

In scrambling, an element ends with a list marker.

So we remove it using:

```py
A[j].pop()
```
(where j is the index of the element that contains the marker)

--- 
### Step 2: Undo the += pop(...) merge

Scramble did:

```py
A[i-2] += A.pop(i-1)
```


That means the (i-1) element got merged into (i-2).

To reverse it:

- take the last hex value back out of A[j-1]
- reinsert it at position j as its own singleton list again

Like:

```py
last_hex = A[j - 1].pop()
A.insert(j, [last_hex])
```

Doing this repeatedly restores the original format:

```py
[['0x70'], ['0x69'], ['0x63'], ...]
```
---

### Convert hex back into the final flag string

Once unscrambled, we decode hex back into characters:

chr(int(hex_value, 16))


Then join them into one string.

After reversing the scramble and converting hex to ASCII, the original picoCTF{...} flag is recovered.