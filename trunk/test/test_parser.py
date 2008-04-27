from ical_parser import *

p = IcalParser()
vcal = p.parse_ics("school.ics")

#check events and todos
print "Calendar name %(e)s" % {'e':vcal.calname}
print "Calendar version %(e)s" % {'e':vcal.version}
print "Calendar TimeZone %(e)s" % {'e':vcal.caltz}
print "Imported %(e)d VEvents" % {'e':len(vcal.get_vevents())}
print "Imported %(e)d VTodos" % {'e':len(vcal.get_vtodos())}

#check adding vevents to calendar object
