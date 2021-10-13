import nltk
import string

text = 'John works at Intel'

print([i for i in text.split()])
print([len(i) for i in text.split()])
print({len(i) for i in text.split()})

a = [i for i in text.split()]
b = [len(i) for i in text.split()]
print([(a[i], b[i]) for i in range(len(a))])
print([(i,len(i)) for i in text.split()])
print([i for i in zip(a,b)])
print(list(zip(a,b)))
print('-'*30)

d = {i : len(i) for i in text.split()}
print(d)

print({value : key for key, value in d.items()})
print({x:y for x,y in zip(d.values(),d.keys())})
print({d[k]: k for k in d})