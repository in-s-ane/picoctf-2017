import sys

something = "yuoteavpxqgrlsdhwfjkzi_cmbn"

def func(a,b):
    result = []
    if a:
        if (a[2] >= b):
            a[0] = func(a[0], b)
            result = a
        else:
            a[1] = func(a[1], b)
            result = a
    else:
        result = [0,0,b]
    return result


def init_data(a):
    result = 0
    i = 0
    while i < len(a):
        result = func(result, a[i])
        i += 1
    return result

def func2(f, a, b):
    if f and len(a) > 0:
        print "in conditional, f[2]: {} and b: {}".format(f[2], b)
        if f[2] == b:
            print "Expecting D, {}".format(a)
            if a[0] == 'D':
                return True
            else:
                return False
        elif f[2] < b:
            print "Expecting R, {}".format(a)
            if a[0] == 'R':
                return func2(f[1], a[1:], b)
            else:
                return False
        elif a[0] == 'L':
            return func2(f[0], a[1:], b)
    print "\nFailing\nf:{}\na:{}\nb:{}\n".format(f,a,b)
    return False

def validate(f, s, p):
    if f and s and p:
        v6 = 1
        v5 = s
        v4 = p
        while len(v5) > 0 and len(v4) > 0:
            v6 = v6 and func2(f, v5, v4[0])
            v4 = v4[1:]
            while v5[0] == 'L' or v5[0] == 'R':
                v5 = v5[1:]
            v5 = v5[1:]
        #if v6 == 1: return True
        if len(v5) == 0 and len(v4) == 0 and v6 == 1:
            return True
        return False
        #return v5[0] == 0 and (v4[0] == 0) & v6
    else:
        return False

def main(password, string):
    forest = init_data(something)
    print forest

    if validate(forest, string, password):
        print "Success"
    else:
        print "Fail"

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
