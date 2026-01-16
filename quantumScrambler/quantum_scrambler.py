import sys

def exit():
  sys.exit(0)

def scramble(L):
  A = L
  i = 2

  print(A)
  # say A = [0,1,2,3,4]
  while (i < len(A)):
    A[i-2] += A.pop(i-1) #  
    print(A)
    A[i-1].append(A[:i-2])
    print(A)
    i += 1
  
    
  return L

def get_flag():
  flag = open('flag.txt', 'r').read()
  flag = flag.strip()
  hex_flag = []
  for c in flag:
    hex_flag.append([str(hex(ord(c)))])

  return hex_flag

def main():
  flag = get_flag()
  cypher = scramble(flag)
  print(cypher)

if __name__ == '__main__':
  main()
