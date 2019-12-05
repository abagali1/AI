from sys import argv

expressions = [
    r"/^[.ox]{64}$/i", #40
    r"/^[ox]*\.[ox]*$/i", #41
    r"/^[ox]*\.[ox]*$|^x[ox]*\.$|^o[ox]*\.$/i", #42
    r"/^.(..)*$/s", #43
    r"/^(0|10|11)([01]{2})*$/", # 44
    r"/\b\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*\b/i", # 45
    r"/^0*(1*|1(0|01)*)1*$/", # 46
    r"/^a[bc]*$|^[bc]+a[bc]*$|^[bc]*a[bc]+$|^[bc]*a$|^[bc]+$/", # 47,
    r"/^[bc]+$|^(([bc]*a){2}[bc]*)+$/", # 48,
    r"/^(1[02]*1[02]*|2[02]*)([02]*1[02]*1[02]*)*$/", # 49,
]

if __name__ == '__main__':
    print(expressions[int(argv[1])-40])