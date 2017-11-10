#!usr/bin/env python3

import datetime
import os
from collections import OrderedDict
import sys

from peewee import *

db = SqliteDatabase('diary.db')


class Entry(Model):
  # content
  content = TextField()
  # timestamp
  timestamp = DateTimeField(default=datetime.datetime.now)
  
  class Meta:
    database = db
    
def initialize():
  """ Initialize the database if it doesn't exist """
  db.connect()
  db.create_tables([Entry], safe=True)
  
def clear():
  os.system('cls' if os.name == 'nt' else 'clear')
  
def menu_loop():
  """ Show the menu """
  choice = None
  
  while choice != 'q':
    clear()
    print('Enter "q" to quit.')
    for key, value in menu.items():
      print('{}) {}'.format(key,value.__doc__))
    choice = input('Action: ').lower().strip() 
    
    if choice in menu:
      clear()
      menu[choice]()
    
def add_entry():
  """ Add new entries """
  print('Enter your entry. Press Ctrl+D when finished.')
  data = sys.stdin.read().strip()
  
  if data:
    if input('Save the Entry [Y/n]: ').lower()!='n':
      Entry.create(content=data)
      print('Saved successfully!')
  
def view_entries(search_query=None):
  """ View the added entries """
  entries = Entry.select().order_by(Entry.timestamp.desc())
  if search_query:
    entries = entries.where(Entry.content.contains(search_query))
  
  for entry in entries:
    timestamp = entry.timestamp.strftime(' %A %B %d, %Y %I:%M%p')
    clear()
    print(timestamp)
    print('='*len(timestamp))
    print(entry.content)
    print('\n\n' + '='*len(timestamp))
    print('n) next entry')
    print('d) delete entry')
    print('q) quit')
    
    next_action = input('Action: [n/d/q] ').lower().strip()
    if next_action == 'q':
       break
    elif next_action == 'd':
      delete_entry(entry)
  
def delete_entry(entry):
  """ Delete previous entries """
  if input('Are you sure? [Y/n] ').lower() == 'y':
    entry.delete_instance()
    print('Entry deleted!')
  
def search_entries():
  """Search a string"""
  view_entries(input('Search query: '))
  

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
  ])

  
if __name__ == '__main__':
  initialize()
  menu_loop()
