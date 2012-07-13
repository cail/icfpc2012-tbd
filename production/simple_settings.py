#!/usr/bin/env python2.7

'''Use sqlite3 db somewhere in the user home directory to store global per-machine settings, 
when an unknown setting is encountered, the user is prompted via GUI.

Database is created/connected lazily, on first access.

All settings are stored as, and automatically converted to, strings, so take care to convert them back. 

>>> from simple_settings import settings
>>> print settings['some setting']
>>> print settings.get_value('some other setting', 'default value')
>>> settings['some other setting'] = 'modified value'

mailto:fj.mail@gmail.com
'''

import sys
import os
from os import path as os_path
import sqlite3

class Settings(object):
    def __init__(self):
        self.app_name = 'icfpc2012'
        db_file_name = 'simple_settings.sqlite'
        if os.name == 'nt':
            self.db_path = os_path.join(os.environ['appdata'], 'simple_settings', db_file_name)
        else:
            self.db_path = os_path.join(os.environ['HOME'], '.simple_settings', db_file_name)
        self._db = None

    @property
    def db(self):
        db = self._db
        if db is None:
            db_dir = os_path.dirname(self.db_path)
            if not os_path.exists(db_dir):
                os.makedirs(db_dir)
            self._db = db = sqlite3.connect(self.db_path)
            db.isolation_level = None
            db.execute('''create table if not exists string_settings
            (app text not null, 
             name text not null, 
             value text not null, 
             primary key (app, name))''')
        return db
            
    def get_value(self, name, default = None):
        res = self.db.execute('select value from string_settings where app=? and name=?', 
                (self.app_name, name)).fetchone()
        if res is not None:
            return res[0]
        if default is None:
            default = self.prompt(name)
        self.set_value(name, default)
        return default

    def set_value(self, name, value):
        self.db.execute(
                'insert or replace into string_settings ' +
                '(app, name, value) values (?, ?, ?)',
                (self.app_name, name, value))
    
    def delete_value(self, name):
        self.db.execute(
                'delete from string_settings where app = ? and name = ?',
                (self.app_name, name))
    
    def clear_all_settings(self):
        self.db.execute(
                'delete from string_settings where app = ?',
                (self.app_name,))
    
    def __getitem__(self, name): return self.get_value(name)
    def __setitem__(self, name, value): return self.set_value(name, value)
    def __delitem__(self, name): return self.delete_value(name)

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
        return self.prompt_gui(name, True)

    def iter_all_db_values(self):
        '''Iterate over all values in the database (not only for current application)'''
        for row in self.db.execute('select * from string_settings order by app, name'):
            yield row

# default settings object
settings = Settings()

def main(argv):
    print 'Printing all settings in the database:'
    for row in settings.iter_all_db_values():
        print ' '.join(repr(s.encode('utf-8')) for s in row)

if __name__ == '__main__':
    main(sys.argv)

