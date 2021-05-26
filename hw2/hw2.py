import os


def CFG(r):
    count = 0
    while count != len(r):
        count = 0
        for x in r:
            if x.isalpha() or x.isspace() or x == '-' or x == '>':
                count += 1
                continue
            else:
                print("please re-enter again")
                r = input()
                break
    print(r)
    r_split = r.split()
    lhs = r_split[0]
    rhs = r_split[-1]
    dic = {}

    # set up first pair
    first = rhs[0]
    rest = rhs[1:]
    if first.islower():
        first = '<' + first + '>'
    rest = '<' + rest + '>'
    rhs = first + rest
    if lhs not in dic:
        dic[lhs] = rhs
    if first not in dic:
        dic[first] = ''
    if rest not in dic:
        dic[rest] = ''
    print(lhs + ' - ' + rhs)

    # loop rules:
    while len(rest) > 3:
        temp = ''
        first = ''
        end = ''
        rhs_split = rhs.split('<')
        if len(rhs_split) > 2:
            temp = rhs_split[0]
            first = '<' + rhs_split[1]
            rest = '<' + rhs_split[2]
        elif rhs[0] == '<':
            first = '<' + rhs_split[0]
            if rhs_split[1][-1] == '>':
                rest = '<' + rhs_split[1]
        else:
            temp = rhs_split[0]
            if rhs_split[1][-1] != '>':
                index = rhs_split[1].find('>')
                rest = '<' + rhs_split[1][:index+1]
                end = rhs_split[1][index+1:]
                #print('end'+end+'rest'+rest)
            else:
                rest = '<' + rhs_split[1]

        #print('temp: ' + temp + 'first:' + first + ':rest' + rest)

        ftemp = first
        if len(first) > 1 and first[1].islower():
            if first not in dic or dic[first] == '':
                dic[first] = first[1]
                first = first[1]
            else:
                first = dic[first]
            print(ftemp + ' - ' + first)

        rtemp = rest
        flag = False
        if len(rest) > 3:
            if len(rest) == 4:
                if rest[1].islower() and rest[2].islower():
                    if rest not in dic or dic[rest] == '':
                        dic[rest] = '<' + rest[1] + '>' + '<' + rest[2] + '>'
                        rest = '<' + rest[1] + '>' + '<' + rest[2] + '>'
                    else:
                        rest = dic[rest]
                elif rest[1].islower() and rest[2].isupper():
                    if rest not in dic or dic[rest] == '':
                        dic[rest] = '<' + rest[1] + '>' + rest[2]
                        rest = '<' + rest[1] + '>' + rest[2]
                        flag = True
                    else:
                        rest = dic[rest]
                elif rest[1].isupper() and rest[2].isupper():
                    if rest not in dic or dic[rest] == '':
                        dic[rest] = rest[1] + rest[2]
                        rest = rest[1] + rest[2]
                    else:
                        rest = dic[rest]
            elif rest[1].isupper():
                if rest not in dic or dic[rest] == '':
                    dic[rest] = rest[1] + '<' + rest[2:]
                    rest = rest[1] + '<' + rest[2:]
                else:
                    rest = dic[rest]
            else:
                if rest not in dic or dic[rest] == '':
                    dic[rest] = '<' + rest[1] + '>' + '<' + rest[2:]
                    rest = '<' + rest[1] + '>' + '<' + rest[2:]
                else:
                    rest = dic[rest]

            print(rtemp + ' - ' + rest)
           # if flag:
             #   rest = rest[:-1]
        rhs = temp + first + rest
        print()
        #print(rhs)
    # print('after loop: ' + rhs + ',')
    rtemp = rest
    if len(rest) == 3:
        if rest[1].islower():
            if rest not in dic or dic[rest] == '':
                dic[rest] = rest[1]
                rest = rest[1]
            else:
                rest = dic[rest]
            print(rtemp + ' - ' + rest)
        else:
            if rest not in dic:
                dic[rest] = ''
                rest = rest[1]
    rhs = temp + first + rest + end

    #print(dic)
    for i in rhs:
        if i.isupper() and '<' + i + '>' in dic:
            if len(dic['<' + i + '>']) == 1 and dic['<' + i + '>'].islower():
                rhs = rhs.replace(i, dic['<' + i + '>'])

    #print(rhs)



#r = "A - aBCdeF"
#CFG(r)

#q = "B - abCdE"
#CFG(q)

#p = "C - AbCde"
#CFG(p)

#y = "D - EFG"
#CFG(y)

#X = "A - abc"
#CFG(X)


val = input("Enter your value,format: A - aBCdeF or A -> aBCdeF, only alphabet, space, - and -> allowed")
CFG(val)