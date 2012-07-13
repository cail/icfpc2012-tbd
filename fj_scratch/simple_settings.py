#!/usr/bin/env python2.7

'''Use sqlite3 db somewhere in the user home directory to store per-app settings, when an unknown setting is encountered, the user is prompted

>>> from simple_settings import settings
>>> print settings['some setting']

or 

>>> from simple_settings import Settings
>>> settings = Settings('my app', use_gui = True)
>>> print settings['some setting']

mailto:fj.mail@gmail.com
'''

import sys
import os
from os import path as os_path
import sqlite3

class Lazy_initialization_trap(object):
    '''On the first attribute access the provided handler would be called.
    It should replace this object with a calculated value _and_ return
    it too, so that this first access could be performed.'''
    __slots__ = ['handler']
    def __init__(self, handler):
        object.__setattr__(self, 'handler', handler)
    def __getattribute__(self, name):
        res = object.__getattribute__(self, 'handler')()
        return getattr(res, name)
    def __setattr__(self, name, value):
        res = object.__getattribute__(self, 'handler')()
        return setattr(res, name, value)
    def __delattr__(self, name, value):
        res = object.__getattribute__(self, 'handler')()
        return delattr(res, name)
        

class Settings(object):
    def __init__(self, app_name = None, db_name = None, use_gui = None):
        '''DB is actually created/opened on the first access.
        
        If app_name is not specified then realpath(argv[0]) is used. It should
        be the full path to the original script being executed (even if it's
        run as "python script.py" or "special_wrapper ./script.py"), but is
        something weird for things launched from the interactive interpreter
        (like, argv[0] is '', then it gets expanded into the name of the
        current directory). 
        
        db_name can be either absolute path or relative, in which case it's
        interpreted as relative to %appdata%/simple_settings on windows or
        $HOME/.simple_settings on UNIX.
        
        If use_gui is None (default) then when user input is required (setting
        not present) the object first tries to use tkinter, then falls back to
        command line input. Specifying True or False makes it use the
        corresponding option only.  '''
        if app_name is None:
            app_name = os_path.realpath(sys.argv[0])
        if db_name is None:
            db_name = 'commondb.sqlite'
        self.app_name = app_name
        if os.name == 'nt':
            self.db_name = os_path.join(os.environ['appdata'], 'simple_settings', db_name)
        else:
            self.db_name = os_path.join(os.environ['HOME'], '.simple_settings', db_name)


        self.use_gui = use_gui
        
        def initialize():
            dir = os_path.dirname(self.db_name)
            if not os_path.exists(dir):
                os.makedirs(dir) 
            self.conn = conn  = sqlite3.connect(self.db_name)
            conn.isolation_level = None
            conn.execute('''create table if not exists string_settings
            (app text not null, 
             name text not null, 
             value text not null, 
             primary key (app, name))''')
            return conn
        self.conn = Lazy_initialization_trap(initialize)
        
    def get_value(self, name, default = None):
        res = self.conn.execute('select value from string_settings where app=? and name=?', 
                (self.app_name, name)).fetchone()
        if res is not None:
            return res[0]
        if default is None:
            default = self.prompt(name)
        self.set_value(name, default)
        return default
    def set_value(self, name, value):
        self.conn.execute(
                'insert or replace into string_settings ' +
                '(app, name, value) values (?, ?, ?)',
                (self.app_name, name, value))
    def delete_value(self, name):
        self.conn.execute(
                'delete from string_settings where app = ? and name = ?',
                (self.app_name, name))
    def clear_all_settings(self):
        self.conn.execute(
                'delete from string_settings where app = ?',
                (self.app_name,))
    def __getitem__(self, name): return self.get_value(name)
    def __setitem__(self, name, value): return self.set_value(name, value)
    def __delitem__(self, name): return self.delete_value(name)

    def prompt_cli(self, name):
        print 'Enter value for \'%s\':' % name,
        return raw_input().strip()
    
    def prompt_gui(self, name, propagate_exception = False):
        ''' Returns None if failed to load tkinter or open display.
        (unless propagate_exception == True).'''
        
        ''' I thought about caching and reusing the tkinter instance, but it might be hard
        to properly temporarily exit from mainloop and suspend the application.
        Anyway, it takes like 10ms to restart it.'''
        try:
            from Tkinter import Tk, Label, Frame, Entry, StringVar
            root = Tk()
        except:
            if propagate_exception:
                raise
            return None

        root.title('Enter value for \'%s\':' % name)
        frame = Frame(root)
        frame.pack(fill = 'y', expand = True)

        label = Label(frame, text='Enter value for \'%s\':' % name)
        label.pack(side='left')
        
        var = StringVar()
        entry = Entry(frame, textvariable = var)
        entry.pack(side='left')
        
        result = []
        root.bind('<Return>', lambda ev: (result.append(var.get()), root.destroy()))
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        root.geometry('+%d+%d' % (ws * 0.4, hs * 0.4))
        entry.focus()
        
        # If I don't do this then for some reason the window doesn't get focus
        # on the second and following invocations. 
        root.focus_force()

        root.mainloop()
        if not len(result):
            # mimic the behaviour of CLI version
            raise KeyboardInterrupt()
        return result[0]
    
    def prompt(self, name):
        if self.use_gui is None:
            res = self.prompt_gui(name)
            if res: return res
            return self.prompt_cli(name)
        if self.use_gui:
            return self.prompt_gui(name, True)
        return self.prompt_cli(name)

    def iter_all_db_values(self):
        '''Iterate over all values in the database (not only for current application)'''
        for row in self.conn.execute('select * from string_settings order by app, name'):
            yield row

settings = Settings()
# default settings object

def main(argv):
    if not 1 <= len(argv) <= 2:
        print 'Print all settings in the database'
        print 'Usage simple_settings.py [db_name]'
        return
    if len(argv) > 1:
        s = Settings(db_name = argv[1])
    else:
        s = settings
    for row in s.iter_all_db_values():
        print ' '.join(repr(s.encode('utf-8')) for s in row)


if __name__ == '__main__':
    main(sys.argv)

