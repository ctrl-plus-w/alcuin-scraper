from icalendar import Calendar, Event, vCalAddress, vText, Alarm
from datetime import datetime, timedelta
from pathlib import Path
import pytz
import os

# Titre, Groupe, Date, Heure, Minute, Salle

#BEGIN:VALARM
#ACTION:DISPLAY
#DESCRIPTION:TEST2
#TRIGGER:-PT15M
#END:VALARM


# Create Calendar Object and Event

cal = Calendar()
event = Event()

# Compliant properties (PRODID -> Identifier that created iCalendar object
# (Version -> specify version)

cal.add('prodid', '-//My calendar product//example.com//')
cal.add('version', '2.0')

# Add data Event 

event.add('name', 'TEST ALCUIN')
event.add('description', 'Test essai creation ics file')

# dtstart -> date commencement evenement

event.add('dtstart', datetime(2022, 1, 25, 8, 0, 0, tzinfo=pytz.utc))


# dtend -> date fin de l'évenement

event.add('dtend', datetime(2022, 1, 25, 10, 0, 0, tzinfo=pytz.utc))

# Creer un objet organisateur avec l'adresse email

organizer = vCalAddress('MAILTO:lukas@exemple.com')

event['location'] = vText('C109')
event['organizer'] = organizer

# Ajout de l'alarme

alarm = Alarm()
alarm.add('action', 'DISPLAY')
alarm.add('trigger', timedelta(minutes=-15))

# Ajout de l'alarme à l'evenement

event.add_component(alarm)

# Ajouter l'évenement au calendrier

cal.add_component(event)

# Enregistrer le fichier sur le disque

directory = Path.cwd() / 'MyCalendar' # "MyCalendar" -> name of the directory
try:
    directory.mkdir(parents=True, exist_ok=False)
except FileExistsError:
    print("Folder already exists")
else:
    print("Folder was created")

f = open(os.path.join(directory, 'exampl4.ics'), 'wb')
f.write(cal.to_ical())
f.close()

