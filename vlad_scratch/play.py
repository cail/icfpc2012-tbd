from game import DictWorld, play

    
def main():
    map = DictWorld.load_file('../data/sample_maps/contest8.map')
    
    play(map)
    
    
if __name__ == '__main__':    
    main()    