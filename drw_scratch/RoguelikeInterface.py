import curses

import game


class RoguelikeInterface(object):
    def __init__(self, map_name, route=''):
        self.world = game.Map.load(map_name)
        self.route = route
        
        self.interactive = True if route == '' else False
        self.step_by_step = True
        
        self.stats_width = 20
        self.stats_height = 7
        
        self.world_x = 1
        self.world_y = 1
        self.stats_x = self.world_x + self.world.width + 2
        self.stats_y = self.world_y
        
        self.help_x = self.world_x
        self.help_y = self.world_y + self.world.height + 1
        
        self.finished = False

        
    def draw_world(self):
        for i in xrange(self.world.height):
            self.world_pad.addstr(i, 0, self.world.get_line(i))

        self.world_pad.noutrefresh(0, 0, self.world_y, self.world_x, \
                                   self.world_y + self.world.height, \
                                   self.world_x + self.world.width)
    
    def draw_stats(self):
        self.stats_pad.erase()
        self.stats_pad.addstr(0, 0, 'robot at ' + str(self.world.robot))
        self.stats_pad.addstr(1, 0, 'moves: ' + str(self.world.moves))
        self.stats_pad.addstr(2, 0, 'lambdas: ' + str(self.world.lambdas))
        self.stats_pad.addstr(3, 0, 'dead: ' + str(self.world.dead))
        self.stats_pad.addstr(4, 0, 'aborted: ' + str(self.world.aborted))
        self.stats_pad.addstr(5, 0, 'lifted: ' + str(self.world.lifted))
        self.stats_pad.addstr(6, 0, 'score: ' + str(self.world.score()))
       
        self.stats_pad.noutrefresh(0, 0, self.stats_y, self.stats_x,  \
                                    self.stats_y + self.stats_height, \
                                    self.stats_x + self.stats_width)
    
    def draw_help(self):
        if self.interactive:
            help_text = "Controls: arrow keys and A, W"
        elif self.step_by_step:
            help_text = "Press space for next move, i to take over control"
        else:
            assert(False)
        
        self.stdscr.move(self.help_y, self.help_x)
        self.stdscr.clrtoeol()
        self.stdscr.addstr(self.help_y, self.help_x, help_text)
        
        
    def update(self):
        self.draw_stats()
        self.draw_world()
        self.draw_help()
        curses.doupdate()
    
    def get_move(self):
        commands = {curses.KEY_LEFT: 'L', curses.KEY_RIGHT: 'R', \
                     curses.KEY_UP: 'U', curses.KEY_DOWN: 'D', \
                     ord('A'): 'A', ord('a'): 'A', ord('W'): 'W', ord('w'): 'W'}
        while True:
            c = self.stdscr.getch()
            if c in commands:
                return commands[c]
   
    def curses_init(self):         
        self.stdscr = curses.initscr()
        curses.def_shell_mode()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        self.stdscr.keypad(1)
        self.world_pad = curses.newpad(self.world.height+1, self.world.width)
        self.stats_pad = curses.newpad(self.stats_height+1, self.stats_width)

        self.stdscr.refresh()    
        
    def curses_deinit(self):
        curses.reset_shell_mode()
        curses.endwin()
        
    def run_interactive(self):
        self.interactive = True
        self.update()
        while not self.world.dead:
            move = self.get_move()
            self.world.execute(move)
            self.update()
    
    def run_noninteractive(self):
        self.interactive = False
        self.update()
        for move in self.route:
            while True:
                c = self.stdscr.getch()
                if c == ord('i'):
                    self.run_interactive()
                    return
                elif c == ord(' '):
                    break
            self.world.execute(move)
            self.update()
    
    def run(self):
        assert(not self.finished)
        
        self.curses_init()
        
        if self.interactive:
            self.run_interactive()
        else:
            self.run_noninteractive()
    
        
        self.curses_deinit()
        
            
            


roguelike = RoguelikeInterface('../data/sample_maps/contest10.map', 'UULLLRLRLRL')
roguelike.run()