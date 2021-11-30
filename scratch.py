match = []
    for row_1 in results['SHIP_ADDRESS']:
        print(row_1)
        for row_2 in results['SHIPPING_CITY']:
            print(row_2)
            if re.search(row_2, row_1, re.IGNORECASE):
                match.append('TRUE')
            else:
                match.append('FALSE')
    print(match)