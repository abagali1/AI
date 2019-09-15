def string_times(str, n):
  return str*n
def front_times(str, n):
  return str[0:3]*n
def string_bits(str):
  return ''.join([str[i] for i in range(0,len(str),2)])
def string_splosion(str):
  return ''.join(str[:i] for i in range(0,len(str)+1))
def last2(str):
  return  sum( [ len([i for i in ([str[x:x+2] for x in range(len(str)-1)]) if i==str[-2:]])-1 for x in [0] if len(str)>1]) + sum([0 for x in [0] if not len(str)>2 ])
def array_count9(nums):
  return nums.count(9)
def array_front9(nums):
  return 9 in nums[:4]
def array123(nums):
  return str(nums).find('1, 2, 3') != -1
def string_match(a, b):
  return len([x for x in range(min(len(a),len(b))-1) if a[x:x+2] == b[x:x+2]])
def double_char(str):
  return ''.join([i*2 for i in str])
def count_hi(str):
  return str.count("hi")
def cat_dog(str):
  return str.count("cat") == str.count("dog")
def count_code(str):
  return len([x for x in range(0,len(str)-3) if str[x:x+2] == "co" and str[x+3] == "e"])
def end_other(a, b):
  return a.lower()[-len(b.lower()) :] == b.lower() or b.lower()[-len(a.lower()) :] == a.lower()
def xyz_there(str):
  return len([x for x in range(1,len(str)-2) if str[x-1] != "." and str[x:x+3] == "xyz"]) != 0 or str[:3] == "xyz"
def count_evens(nums):
  return len([x for x in nums if x%2==0])
def big_diff(nums):
  return max(nums) - min(nums)
def centered_average(nums):
  return (sum(nums) - (min(nums) + max(nums)) )//(len(nums)-2)
def sum13(nums):
  return sum([0 for x in [0] if len(nums)==0]) + sum([y for x,y in enumerate(nums+[0]) if len(nums)!=0 and y!=13 and ((nums+[0])[x-1] != 13)])
def sum67(nums):
  inside = False
  s=0
  for i in nums:
    if i==6: inside =True
    elif not inside: s += i
    elif i == 7: inside = False
  return s
def has22(nums):
  return len([x for x,y in zip(nums,nums[1:]) if x == 2 and y == 2]) > 0
def make_bricks(small, big, goal):
  return small >= goal-(big*5) and small >= goal%5
def lone_sum(a, b, c):
  return sum([0 for x in [a] if a==b and b==c]) + sum([c for x in [a] if a==b and b!=c]) + sum([b for x in [a] if a==c and a!=b and b!=c]) + sum([a for x in [a] if a!=b and b==c and a!=c]) + sum([a+b+c for x in [a] if a!=b and b!=c and a!=c])
def lucky_sum(a, b, c):
  return sum([0 for x in [a] if x==13]) + sum([a for x in [b] if a!=13 and b==13]) + sum([a+b for x in [c] if a!=13 and b!=13 and c==13]) + sum([a+b+c for x in [a] if a!=13 and b!=13 and c!=13])
def no_teen_sum(a, b, c):
  return sum([x for x in [a,b,c] if x>19 or x<13 or x==15 or x==16 ])
def round_sum(a, b, c):
  return sum([x-x%10 for x in [a,b,c] if x%10<5]) + sum([x+(10-x%10) for x in [a,b,c] if not x%10<5])
def close_far(a, b, c):
  return (abs(b-a)<=1 and abs(c-a)>=2 and abs(c-b) >=2) or (abs(c-a)<=1 and abs(b-a)>=2 and abs(b-c)>=2)
def make_chocolate(small, big, goal):
  return -1 if goal%5>small or goal>small+big*5 else goal-big*5 if not big*5>goal else goal%5