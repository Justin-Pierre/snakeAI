if __name__ == "__main__":
    
    coords = [(0,15),(0,0),(29,0)]
    last = (29,0)
    for x in range (1,30):
        if last[0] == 29:
            coords.append((29,x))
            coords.append((1,x))
            last = (1,x)
        else:
            coords.append((1,x))
            coords.append((29,x))
            last = (29,x)
    
    print(coords)