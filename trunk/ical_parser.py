from __future__ import with_statement

"""
The MIT License

Copyright (c) 2008 meseretgebre.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


#DISCLAIMER: this parser is not up to the icalendar standards. Take code "AS IS".
#Will grab VEvents and VTodos and can convert to gdata event entry kind. It gives enough 
#data to create google calendar events. 
#ical <--> google calendar event objects! 

#last-update: 4/26/2008

__author__ = 'meseret.gebre@gmail.com (Mez)'
__version__ = 'V-0.1'

#IMPORT START HERE



#IMPORT END HERE



"""
     BEGIN:VCALENDAR
     VERSION:2.0
     PRODID:-//hacksw/handcal//NONSGML v1.0//EN
     BEGIN:VEVENT
     DTSTART:19970714T170000Z
     DTEND:19970715T035959Z
     SUMMARY:Bastille Day Party
     END:VEVENT
     END:VCALENDAR
     
     BEGIN:VTODO
     UID:19970901T130000Z-123404@host.com
     DTSTAMP:19970901T1300Z
     DTSTART:19970415T133000Z
     DUE:19970416T045959Z
     SUMMARY:1996 Income Tax Preparation
     CLASS:CONFIDENTIAL
     CATEGORIES:FAMILY,FINANCE
     PRIORITY:1
     STATUS:NEEDS-ACTION
     END:VTODO
"""

#Icalendar standard variables
calname = "X-WR-CALNAME"
caltz   = "X-WR-TIMEZONE"
version = "VERSION"
calendar_start = "BEGIN:VCALENDAR"
calendar_end = "END:VCALENDAR"
vevent_start = "BEGIN:VEVENT"
vevent_end = "END:VEVENT"
vtodo_start  = "BEGIN:VTODO"
vtodo_end = "END:VTODO"
summary = "SUMMARY"
dtstart = "DTSTART"
dtend  = "DTEND"
due = "DUE"
visibility = "CLASS"
private = "CLASS:CONFIDENTIAL"
public  = "CLASS:PUBLIC"
rrule = "RRULE"

class IcalParser():
    """This is the main ical parser, use this class to parse and convert formats."""

    def parse_ics(self, file_name):
        """parse a .ics file.
        
        Input 
        file_name -- this is the .ics file, must be a .ics file
        
        Output
        VCalendar object
        
        """
        vcal = VCalendar()
        if not file_name.endswith('.ics'):
            raise "Incorrect file type! please make sure it's a .ics file"
        with open(file_name, 'r') as ics:
            start_event_capture = False
            start_todo_capture = False
            if not ics.readline().startswith(calendar_start):
                raise "Parse error: make sure the file starts with BEGIN:VCALENDAR"
            for line in ics:
                #for calendar info
                if line.startswith(version):
                    vcal.version = line.split(":")[1]
                if line.startswith(calname):
                    vcal.calname = line.split(":")[1]
                if line.startswith(caltz):
                    vcal.caltz = line.split(":")[1]
                #for vevents
                if line.startswith(vevent_start):
                    event = VEvent()
                    start_event_capture = True
                    
                if start_event_capture:
                    if line.startswith(vevent_end):
                        vcal.add_vevent(event)
                        start_event_capture = False
                        del event
                    if line.startswith(summary):
                        event.summary=line.split(":")[1]
                    if line.startswith(dtstart):
                        event.dtstart = line
                    if line.startswith(dtend):
                        event.dtend=line
                    if line.startswith(rrule):
                        event.rrule=line
                    if line.startswith(visibility):
                        event.visibility=line.split(":")[1]
                
                #for vtodos
                if line.startswith(vtodo_start):
                   todo = VTodo()
                   start_todo_capture = True
                   
                if start_todo_capture:
                    if line.startswith(vtodo_end):
                        vcal.add_vtodo(todo)
                        start_todo_capture = False
                        del todo
                    if line.startswith(summary):
                        todo.summary=line.split(":")[1]
                    if line.startswith(dtstart):
                        todo.dtstart = line
                    if line.startswith(due):
                        todo.due=line
                    if line.startswith(rrule):
                        todo.rrule=line
                    if line.startswith(visibility):
                        todo.visibility=line.split(":")[1]
        return vcal
    
    
class VCalendar():
    """Models a Icalendar objects (not to standard). """
    
    def __init__(self):
        self.vevents = []
        self.vtodos = []
        self.version = ''
        self.calname = ''
        self.caltz = ''
    def add_vevent(self,vevent):
        """Takes an VEvent object.""" 
        if type(vevent) == type(VEvent()): #doesn't work like i thought it did. I.E will let other classes through
            self.vevents.append(vevent)
        else: 
            raise "Not a VEvent object, can't be added."
    
    def get_vevents(self):
        return self.vevents
    
    def add_vtodo(self,vtodo): 
        """Takes an VTodo object.""" 
        if type(vtodo) == type(VTodo()): #doesn't work like i thought it did. I.E will let other classes through
            self.vtodos.append(vtodo)
        else: 
            raise "Not a VTodo object, can't be added."
    
    def get_vtodos(self):
        return self.vtodos
    
class VEvent():
    """Represents an icalendar event (not to standard)."""
    def __init__(self):
        self.summary = ''
        self.dtstart = ''
        self.dtend = ''
        self.rrule = 'none'
        self.visibility = ''
    
    def is_recurring(self):
        return not self.rrule == 'none'
    
    def get_recurring_data(self):
        return (self.dtstart +'\r\n' 
                + self.dtend+'\r\n'
                + self.rrule+'\r\n')
        
    def __str__(self):
        return self.summary+"\n"+self.dtstart+"\n"+self.dtend+"\n"+self.rrule+"\n"+self.visibility

class VTodo():
    """Represents an icalendar todo (not to standard)."""
    def __init__(self):
        self.summary = ''
        self.dtstart = ''
        self.due = ''
        self.rrule = 'none'
        self.visibility = 'public'
    def __str__(self):
        return self.summary+"\n"+self.dtstart+"\n"+self.due+"\n"+self.rrule+"\n"+self.visibility

class GEvent():
    pass

