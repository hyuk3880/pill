import random
import string
import numpy as np

a = ['Guest', 'Detroit', 'Woodlawn', 'Cemetary', 'People']
'''mx=a[0]
for i in a:
    if i>mx:
        mx = i
print(mx)
print(max([len(i) for i in a]))'''

# numbers=[]
# for i in range(10):
#     numbers.append(random.randrange(100))

list2 = [random.randrange(100) for a in range(10)]
print(list2)
# list.reverse()
# print(list)
print([i//10 + i%10*10 for i in list2])
print('-'*30)

alphabets = list(string.ascii_lowercase)
print(alphabets)
letters = [['a','b','c','d','e','f']
    ,['g','h','i','j','k','l']
    ,['m','n','o','p','q','r']
    ,['s','t','u','v','w','x']]
li = []
for j in letters:
    for i in j:
        li.append(i)
print(li)
print([letters[j][i] for j in range(4) for i in range(6)])
print([j for i in letters for j in i])
print('-'*30)

ran = [[random.randrange(10) for a in range(5)] for b in range(5)]
print(*ran, sep='\n')

print([[j for j in i if j%2] for i in ran])
print([sum([j for j in i if j%2]) for i in ran])
print(max([sum([j for j in i if j%2]) for i in ran]))
print(np.argmax([sum([j for j in i if j%2]) for i in ran]))