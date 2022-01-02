sound=[0]*10
s=0
a=0

for i in range(10):
    sound[i]=int(input())
    s=s+sound[i]
a=s/10
print(a)

While True:
    for i in range(9):
        sound[i]=sound[i+1]
    sound[9]=int(input())
    s=0
    for i in range(10)
        s=s+sound[i]
    a=s/10
    print(a)