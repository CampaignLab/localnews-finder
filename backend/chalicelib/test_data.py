from data import towns,media

def test_data():
    #print(towns)
    #print(media)
    missing = []
    dtowns = {}
    for townlist in towns:
        for town in townlist:
            dtowns[town] = town
    for (constituency, website) in media:
        if not constituency in dtowns:
            missing.append(constituency)
        
    missing = sorted(set(missing))
    for constituency in missing:
        print(f'{constituency} NOT MAPPED')
    assert missing == []
