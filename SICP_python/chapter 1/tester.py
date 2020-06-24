def intersect_tester (m:list):
    test = False
    test_el = False
    for el in m[1]:
        if test_el == True:
            break
        test_el = True
        for matrx in m:
            if el not in matrx:
                test_el = False
    return test

m = [[16],[16],[16]]

intersect_tester(m)