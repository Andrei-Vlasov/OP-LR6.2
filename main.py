from abc import abstractmethod


class Group:
    def __init__(self):
        self.children = []
        self.count = 0
        self.schedule = Schedule()
        self.agenda = Agenda(self)

    def join(self, child):
        if child not in self.children:
            self.children.append(child)
            self.count += 1
            child.group = self
            print(child.name, "joins group! Welcome")
        else:
            print(child.name, "already in group")

    def leave(self, child):
        if child in self.children:
            self.children.remove(child)
            self.count -= 1
            child.group = None
            print(child.name, "leaves group! Goodbye")
        else:
            print(child.name, "not in group")


class Child:
    def __init__(self, name, wallet=0):
        self.name = name
        self.group = None
        self.wallet = wallet

    def subscribe(self, event):
        if self.group is None:
            print(self.name, 'not in group')
            return
        if event in self.group.agenda.events:
            if self not in event.attendees:
                if self.wallet >= event.cost:
                    event.attendees.append(self)
                    self.wallet -= event.cost
                    self.group.agenda.announce(event)
                    print(self.name, 'subscribed to event', event.title, ', prepaid', event.cost)
                else:
                    print(self.name, "doesn't have enough funds for", event.title)
            else:
                print(self.name, 'already subscribed to the event', event.title)
        else:
            if event in self.group.schedule.events:
                print('Buy tickets to event', event.title, 'in schedule')
            else:
                print('No event found for', event.title)

    def unsubscribe(self, event):
        if self.group is None:
            print(self.name, 'not in group')
            return
        if event in self.group.agenda.events:
            if self in event.attendees:
                event.attendees.remove(self)
                self.wallet += event.cost
                print(self.name, 'unsubscribed from event', event.title, ', returned', event.cost)
            else:
                print(self.name, 'was not subscribed to the event', event.title)
        else:
            if event in self.group.schedule.events:
                print('Buy tickets to event', event.title, 'in schedule')
            else:
                print('No event found for', event.title)

    def buy(self, event):
        if self.group is None:
            print(self.name, 'not in group')
            return
        if event in self.group.schedule.events:
            if self not in event.attendees:
                if self.wallet >= event.cost:
                    self.wallet -= event.cost
                    event.attendees.append(self)
                    print(self.name, 'just bought ticket to event', event.title, ', paid', event.cost)
                else:
                    print(self.name, "doesn't have enough money for", event.title)
            else:
                print(self.name, 'already bought ticket to event', event.title)
        else:
            if event in self.group.agenda.events:
                print('Book tickets to event', event.title, 'in agenda')
            else:
                print('No event found for', event.title)

    def donate(self, num):
        self.wallet+=num

class Agenda:
    def __init__(self, group):
        self.events = []
        self.group = group

    def write(self, event):
        if event not in self.events:
            if event not in self.group.schedule.events:
                print('Added', event.title, 'to agenda')
                self.events.append(event)
            else:
                print(event.title, 'already in group schedule')
        else:
            print('Event', event.title, "already in agenda")

    def remove(self, event):
        if event in self.events:
            self.events.remove(event)
        else:
            print('Event', event.title, "not found in schedule")

    def announce(self, event):
        if len(event.attendees) > self.group.count / 3:
            self.group.schedule.write(event)
            print('Group will be attending', event.title, 'on', event.date)
            for e in self.events:
                if e.date == event.date and e!=event:
                    for pers in e.attendees:
                        pers.wallet += e.cost
                    print('so the group already has plans on day of', e.title, ". Money returned.")
                    del e


class Schedule:
    def __init__(self):
        self.events = []
        self.timetable = {}
        for day in range(1, 32):
            self.timetable.update({day:[]})

    def write(self, event):
        if event not in self.events:
            self.events.append(event)
            self.timetable[event.date].append(event)
        else:
            print(event.title, "already added to schedule")


    def remove(self, event):
        if event in self.events:
            self.events.remove(event)
        else:
            print(event.title, "not found in schedule")

    def show(self):
        print("=========GROUP SCHEDULE=========")
        for i in range(1, 32):
            if self.timetable[i] != []:
                for event in self.timetable[i]:
                    print("Day:", i)
                    print(event.title)
                    for desc in [event.genre,event.sights,event.tricks]:
                        if desc is not None:
                            if type(desc) is list:
                                print(", ".join(desc))
                            else:
                                print(desc)
                    print("Cost:", event.cost)
                    if event.description is not None:
                        print(event.description)
                    print("Attendees: ", end='')
                    for attendee in event.attendees:
                        print(attendee.name, end=' ')
                    print('\n')


class Event:
    @abstractmethod
    def __init__(self, title, cost, date, tricks=None, genre=None, sights=None, description=None):
        self.title = title
        self.cost = cost
        self.date = date
        self.tricks = tricks
        self.genre = genre
        self.sights = sights
        self.description = description
        self.attendees = []

    @abstractmethod
    def cancel(self):
        pass


class Circus(Event):
    def __init__(self,title, cost, date, tricks, description=None):
        super().__init__(title, cost, date, tricks=tricks, description=description)

    def cancel(self):
        del self


class Theatre(Event):
    def __init__(self, title, cost, date, genre, description=None):
        super().__init__(title, cost, date, genre=genre, description=description)

    def cancel(self):
        del self


class Excursion(Event):
    def __init__(self, title, cost, date, sights, description=None):
        super().__init__(title, cost, date, sights=sights, description=description)

    def cancel(self):
        del self


###TEST###

A = Group()

ch1 = Child('Bob')
ch2 = Child('Nick')
ch3 = Child('Sam')
ch4 = Child('Pete')
ch5 = Child('Pam')
ch6 = Child('Amy')
ch7 = Child('Lisa')
ch8 = Child('Eva')
ch9 = Child('Lana')
ch10 = Child('Gabe')
ch11 = Child('Zoey')
ch12 = Child('Kyle')
A.join(ch1)
A.join(ch2)
A.join(ch3)
A.join(ch4)
A.join(ch5)
A.join(ch6)
A.join(ch7)
A.join(ch8)
A.join(ch9)
A.join(ch10)
A.join(ch11)
A.join(ch12)

ev1 = Circus('Bears on bicycles', 120, 1, tricks=['by animals'], description='Fun show!')
ev2 = Theatre('The 3 bears', 90, 3, genre='fairytale')
ev3 = Excursion('The catacombs', 45, 8, sights=['underground catacombs'])
ev4 = Circus('Clown Land', 80, 10, tricks=['by clowns', 'by mimes'])
ev5 = Theatre('Aladdin', 100, 10, genre='fairytale')
ev6 = Excursion('The national park', 30, 15, sights=['park'], description='See the beauty of our national park')
ev7 = Circus('Cirque de Paris', 200, 17, tricks=['stunts'], description="The notorious Cirque de Paris's first time in our city")
ev8 = Theatre('Swan Lake', 150, 17, genre='ballet', description="Classic by Tschaikovski")
ev9 = Excursion('Old castles', 60, 17, sights=['historical'])
A.agenda.write(ev1)
A.agenda.write(ev2)
A.agenda.write(ev3)
A.agenda.write(ev4)
A.agenda.write(ev5)
A.agenda.write(ev6)
A.agenda.write(ev7)
A.agenda.write(ev8)
A.agenda.write(ev9)


def quick_test():
    num = int(input('How much money for every person at start?(Try 300, 400, 500): '))
    for i in A.children:
        i.donate(num)

quick_test()

ch1.subscribe(ev1)
ch1.subscribe(ev4)
ch1.subscribe(ev6)
ch2.subscribe(ev2)
ch2.subscribe(ev4)
ch2.subscribe(ev5)
ch2.subscribe(ev7)
ch2.subscribe(ev9)
ch3.subscribe(ev2)
ch3.subscribe(ev3)
ch3.subscribe(ev8)
ch5.subscribe(ev3)
ch5.subscribe(ev8)
ch6.subscribe(ev2)
ch6.subscribe(ev7)
ch6.subscribe(ev9)
ch7.subscribe(ev4)
ch7.subscribe(ev8)
ch8.subscribe(ev9)
ch9.subscribe(ev1)
ch9.subscribe(ev4)
ch9.subscribe(ev8)
ch10.subscribe(ev7)
ch12.subscribe(ev2)
ch12.subscribe(ev8)
ch12.subscribe(ev9)
ch11.subscribe(ev9)

A.schedule.show()

print("Виконав Власов Андрій Олександрович ІП-9105")
print("Лабораторна з основ програмування 6.2В (варіант 5)")
print("Мова Python")
