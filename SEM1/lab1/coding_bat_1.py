def sleep_in(weekday, vacation):
  return not weekday or vacation
def monkey_trouble(a_smile, b_smile):
  return a_smile and b_smile or not a_smile and not b_smile
def sum_double(a, b):
  return a + b + b + a if a == b else a + b
def diff21(n):
  return 21 - n if n < 21 else 2 * (n - 21)
def parrot_trouble(talking, hour):
  return talking and (hour < 7 or hour > 20)
def makes10(a, b):
  return a == 10 or b == 10 or a + b == 10
def near_hundred(n):
  return abs(100 - n) <= 10 or abs(200 - n) <= 10
def pos_neg(a, b, negative):
  return a<0 and b<0 if negative else (a<0 and b>0) or (a>0 and b<0)
def hello_name(name):
  return "Hello " + name + "!"
def make_abba(a, b):
  return a + b + b + a
def make_tags(tag, word):
  return "<" + tag + ">" + word + "</" + tag + ">"
def make_out_word(out, word):
  return out[0:(len(out)//2)] + word + out[len(out)//2:] 
def extra_end(str):
  return str[-2:] * 3
def first_two(str):
  return str[0:2]
def first_half(str):
  return str[:(len(str) // 2)]
def first_last6(nums):
  return (nums[0]) == 6 or (nums[-1]) == 6 or nums[0] == "6" or nums[-1] == "6"
def same_first_last(nums):
  return len(nums) >= 1 and nums[0] == nums[-1]
def make_pi(n):
  return [int(c) for c in "31415926535"[:n]]
def common_end(a, b):
  return a[-1] == b[-1] or a[0] == b[0]
def sum3(nums):
  return sum(nums)
def rotate_left3(nums):
  return list(nums[1:]) + [nums[0]]
def reverse3(nums):
  return nums[::-1]
def max_end3(nums):
  return [nums[0]]*len(nums) if nums[0] > nums[-1] else [nums[-1]]*len(nums)
def cigar_party(cigars, is_weekend):
  return cigars>=40 and cigars<=60 if not is_weekend else cigars>=40
def date_fashion(you, date):
  return 0 if you<= 2 or date <= 2 else 2 if you>=8 or date >= 8 else 1
def squirrel_play(temp, is_summer):
    return 60 <= temp and 90 >= temp if not is_summer else 60 <= temp and 100 >= temp
def caught_speeding(speed, is_birthday):
  return 2 if is_birthday and 86<=speed else 0 if speed<66 and is_birthday else 1 if is_birthday else 2 if 81<=speed else 0 if speed<61 else 1
def sorta_sum(a, b):
  return 20 if 10 <= (a + b) and 19 >= (a + b) else a + b
def alarm_clock(day, vacation):
  return "10:00" if vacation and 1<=day and 5>= day else "off" if vacation else "7:00" if 1<=day and 5>=day else "10:00"
def love6(a, b):
  return a == 6 or b == 6 or a + b == 6 or abs(a - b) == 6
def in1to10(n, outside_mode):
  return 1 <= n and n <= 10 if not outside_mode else 1 >= n or n >= 10