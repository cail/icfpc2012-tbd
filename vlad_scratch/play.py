from game import Map, play

    
def main():
    map = Map.load_file('../data/sample_maps/contest8.map')
    
    play(map)
    
    
if __name__ == '__main__':    
    main()    