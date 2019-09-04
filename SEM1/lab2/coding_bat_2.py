# Anup Bagali
# Gabor Period 2
# 08/29/19

# Warm Up 2


def string_times(str, n):
  return str*n


def front_times(str, n):
  return str[0:3]*n


def string_bits(str):
  return ''.join([str[i] for i in range(0,len(str),2)])

def string_splosion(str):
  return ''.join(str[:i] for i in range(0,len(str)+1))


  ## MISING PROBLEM


def array_count9(nums):
  return nums.count(9)


def array_front9(nums):
  return 9 in nums[:4]


def array123(nums):
  return str(nums).find('1, 2, 3') != -1


## MISSING PROBLEM


# String 2

def double_char(str):
  return ''.join([i*2 for i in str])



def count_hi(str):
  return str.count("hi")


def cat_dog(str):
  return str.count("cat") == str.count("dog")


def count_code(str):
  count=0
  for i in range(0,len(str)-3):
    if str[i:i+2] == "co":
      if str[i+3] == "e":
        count+=1
  return count


def end_other(a, b):
  return a.lower()[-len(b.lower()) :] == b.lower() or b.lower()[-len(a.lower()) :] == a.lower()


## MISSING PROBLEM  


# List 2

def count_evens(nums):
  return len([x for x in nums if x%2==0])


def big_diff(nums):
  return max(nums) - min(nums)


def centered_average(nums):
  return (sum(nums) - (min(nums) + max(nums)) )/(len(nums)-2)


def sum13(nums):
  arr = []
  i =0
  while i < len(nums):
    if nums[i] == 13:
      i += 2
    else:
      arr.append(nums[i])
      i += 1
  return sum(arr)

  ## MISSING PROBLEM


def has22(nums):
  return "2, 2" in str(nums)