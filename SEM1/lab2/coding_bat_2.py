
def string_times(str, n):
  return str*n
def front_times(str, n):
  return str[0:3]*n
def string_bits(str):
  return ''.join([str[i] for i in range(0,len(str),2)])
def string_splosion(str):
  return ''.join(str[:i] for i in range(0,len(str)+1))
def last2(str):
  return len([i for i in ([str[x:x+2] for x in range(len(str)-1)]) if i==str[-2:]])-1 if len(str) > 2 else 0
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
# List 2
def count_evens(nums):
  return len([x for x in nums if x%2==0])
def big_diff(nums):
  return max(nums) - min(nums)
def centered_average(nums):
  return (sum(nums) - (min(nums) + max(nums)) )//(len(nums)-2)
def sum13(nums):
  return sum([y for x,y in enumerate(nums) if y!=13 and (nums[x-1] != 13)])
def sum67(nums):
  six_index = [x for x,y in enumerate(nums) if y == 6]
  seven_index = [x for x,y in enumerate(nums) if y == 7]
  if not six_index:
    return sum(nums)
  else:
    sums = 0
    for i in range(len(six_index)-1):
      part = nums[:six_index[i]] + nums[seven_index[i]+1:] 
      sums += sum(part)
      return i
def has22(nums):
  return len([x for x,y in zip(nums,nums[1:]) if x == 2 and y == 2]) > 0


# Logic 2
def lone_sum(a, b, c):
  return 0 if a==b and b==c else c if a==b and b!=c else b if a==c else a if b==c else a+b+c
def lucky_sum(a, b, c):
  return 0 if a==13 else a if b==13 else a+b if c==13 else a+b+c