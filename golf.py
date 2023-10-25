import random as r,re
class D:
 def __init__(s,t,n=1):s.t,s.n=t,n
 def r(s):return sum(r.randint(1,s.t)for _ in[0]*s.n)if s.t<101 else r.randint(1,99)+1
class R:
 d={f"d{i}":i for i in[20,12,10,8,6,4,100]}
 def p(s,i):return sum([(int(x[0]+(x[1]or'1'))if x[2]else int(x[3]))*D(s.d[f"d{x[2]}"]if x[2]else 1).r()for x in re.findall(r'([+-]?)(\d*)d(\d+)|([+-]?\d+)',i)])
 def pr(s):
  while 1:i=input('Input: ');print(f"Rolled {i}: {s.p(i)}")
if __name__=="__main__":R().pr()