class Thing:
    '''Fields: id (Nat),
               name (Str),
               description (Str)
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        
    def __repr__(self):
        return '<thing #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        
class Player:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               location (Room),
               inventory ((listof Thing))
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.location = None
        self.inventory = []
        
    def __repr__(self):
        return '<player #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.inventory) != 0:
            print('Carrying: {0}.'.format(
                ', '.join(map(lambda x: x.name,self.inventory))))
 
class Room:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               contents ((listof Thing)),
               exits ((listof Exit))
    '''    
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.contents = []
        self.exits = []
        
    def __repr__(self):
        return '<room {0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.contents) != 0:
            print('Contents: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.contents))))
        if len(self.exits) != 0:
            print('Exits: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.exits)))) 
 
class Exit:
    '''Fields: name (Str), 
               destination (Room)
               key (Thing)
               message (Str)
    '''       
    
    def __init__(self,name,dest,key,message):
        self.name = name
        self.destination = dest
        self.key = None 
        self.message = ''
        
    def __repr__(self):
        return '<exit {0}>'.format(self.name)

class World:
    '''Fields: rooms ((listof Room)), 
               player (Player)
    '''       
    
    msg_look_fail = "You don't see that here."
    msg_no_inventory = "You aren't carrying anything."
    msg_take_succ = "Taken."
    msg_take_fail = "You can't take that."
    msg_drop_succ = "Dropped."
    msg_drop_fail = "You aren't carrying that."
    msg_go_fail = "You can't go that way."
    
    msg_quit = "Goodbye."
    msg_verb_fail = "I don't understand that."
    
    def __init__(self, rooms, player):
        self.rooms = rooms
        self.player = player

    def look(self, noun):
        if noun == 'me': 
            return self.player.look()
        elif noun == 'here': 
            return self.player.location.look()
        for thing in self.player.inventory: 
            if thing.name == noun: 
                return thing.look()
        for thing in self.player.location.contents: 
            if thing.name == noun: 
                return thing.look()
        print("You don't see that here.")
            
    def inventory(self):
        if self.player.inventory != []:
            items=''
            for item in self.player.inventory[0:-1]:
                items += item.name + ", "                               
            final = "Inventory: " + items + self.player.inventory[-1].name
            print( final ) 
        else: 
            print("You aren't carrying anything.")
            
    def take(self, noun):
        #accepts a noun argument, giving the name of the thing to pick up and
        #doesnt return anything. If noun corresponds to a thing in the player's 
        #current room, it gets added to players inventory and removed from room
        for thing in self.player.location.contents: 
            if thing.name == noun: 
                self.player.inventory += [thing]
                self.player.location.contents.remove(thing)
                print( self.msg_take_succ )
                return None
        
        print( self.msg_take_fail )
            
    def drop(self, noun):
        #accepts noun argument, giving the name of the thing to put down 
        # doesnt return anything. If noun corresponds to a thing in player's 
        #inventory, it is removed and appended to contents of current room
        for thing in self.player.inventory: 
            if thing.name == noun: 
                self.player.location.contents += [thing]
                self.player.inventory.remove(thing)
                print( self.msg_drop_succ )
                return None        
        print( self.msg_drop_fail )
        
    def go(self, noun):
        '''consumes a noun argument, giving the name of the exit to go through, 
        and doesnt return anything. If noun corresponds to the name of one of 
        the exits, it mutates the contents of WOrld so that the player moves 
        to another room at the other end of the exit'''
        for exit in self.player.location.exits: 
            if exit.name == noun: 
                if exit.key == None: 
                    self.player.location = exit.destination
                    return self.player.location.look()
                else: 
                    for items in self.player.inventory: 
                        if items == exit.key: 
                            self.player.location = exit.destination
                            return self.player.location.look()
                    print(exit.message)
                    return self.player.location.look()
        
        print( self.msg_go_fail )
                
    def play(self):
        player = self.player
        
        player.location.look()
        
        while True:
            line = input( "- " )
            
            wds = line.split()
            verb = wds[0]
            noun = ' '.join( wds[1:] )
            
            if verb == 'quit':
                print( self.msg_quit )
                return
            elif verb == 'look':
                if len(noun) > 0:
                    self.look(noun)  
                else:
                    self.look('here')
            elif verb == 'inventory':
                self.inventory()     
            elif verb == 'take':
                self.take(noun)    
            elif verb == 'drop':
                self.drop(noun)
            elif verb == 'go':
                self.go(noun)   
            else:
                print( self.msg_verb_fail )

    ## Q3
    def save(self, fname):
        # saves a gave at that current point
        # save: Str -> World
        f=open(fname,"w")
        for items in self.player.inventory:
            f.write("thing #{0} {1}\n".format(items.id,items.name))
            f.write(items.description+"\n")
        for items in self.rooms:
            for i in items.contents:
                f.write("thing #{0} {1}\n".format(i.id,i.name))
                f.write(i.description+"\n")
        for items in self.rooms:
            f.write("room #{0} {1}\n".format(items.id,items.name))
            f.write(items.description+"\n")
            f.write("contents ")
            for i in items.contents:
                f.write("#{0} ".format(i.id))
            f.write("\n")
        f.write("player #{0} {1}".format(self.player.id,self.player.name))
        f.write("\n")
        f.write(self.player.description)
        f.write("\n")
        f.write("inventory ")
        for items in self.player.inventory:
            f.write("#{0} ".format(items.id))
        f.write("\n")
        f.write("location #{0}".format(self.player.location.id))
        f.write("\n")
        for items in self.rooms:
            for j in items.exits:
                if j.key!=None:
                    f.write("keyexit #{0} #{1} {2}\n".format(items.id,j.destination.id,j.name))
                    f.write("#{0} ".format(j.key.id)+  j.message + "\n")
                else:
                    f.write("exit #{0} #{1} {2}\n".format(items.id,j.destination.id,j.name))
        f.close()
        return None
    
    
    
    
    
    
def lst_to_str(los):
    '''concatenates a list of string to a string
    lst_to_str: (listof Str) -> Str'''
    str_output = ''
    for s in los[0:-1]: 
        str_output += s + ' '
    str_output += los[-1]
    return str_output
## Q2
def load( fname ):
    '''
    opens a file with file name, fname, and makes a world using information 
    from the file
    load: Str -> World
    '''
    f = open(fname, "r")
    lines = f.readlines()
    list_of_things = []
    for ith_line in range(len(lines)): 
        items = lines[ith_line].split()
        if items[0] == "thing": 
            name = lst_to_str(items[2:])
            index = int((items[1])[1:])
            thing_object = Thing(index)
            thing_object.name = name 
            thing_object.description = lines[ith_line + 1]
            list_of_things += [thing_object]
    rooms = []
    for ith_line in range(len(lines)): 
        items = lines[ith_line].split()            
        if items[0] == "room": 
            name = lst_to_str(items[2:])
            index = int((items[1])[1:])
            room_object = Room(index)
            room_object.name = name 
            room_object.exits = []
            room_object.description = lines[ith_line + 1]
            rooms += [room_object]
            room_object.contents = []
            list_of_ids = (lines[ith_line + 2].split())[1:]
            if list_of_ids == []: 
                room_object.contents = [] 
            else: 
                for ids in list_of_ids: 
                    for thing in list_of_things: 
                        if int(ids[1:]) == thing.id: 
                            room_object.contents += [thing]
    for ith_line in range(len(lines)): 
        items = lines[ith_line].split()
        if items[0] == "player": 
            name = lst_to_str(items[2:])
            index = int((items[1])[1:])
            player = Player(index)
            player.name = name 
            player.description = lines[ith_line + 1]
            player.inventory = []
            list_of_ids = (lines[ith_line + 2].split())[1:]
            if list_of_ids == []: 
                player.inventory = []
            else: 
                for ids in list_of_ids: 
                    for thing in list_of_things: 
                        if int(ids[1:]) == thing.id: 
                            player.inventory += [thing] 
            location_id = int(lines[ith_line + 3].split()[1][1:])
            for room in rooms: 
                if location_id == room.id: 
                    player.location = room
    for ith_line in range(len(lines)): 
        items = lines[ith_line].split()
        if items[0] == "exit": 
            name = items[-1]
            index = int((items[2])[1:])
            
            for room in rooms: 
                if room.id == index: 
                    exit_object = Exit(name, room, None, '') 
                    #exit_object.destination = room
            index_of_room = int((items[1])[1:])
            for room in rooms: 
                if room.id == index_of_room: 
                    room.exits += [exit_object]
    for ith_line in range(len(lines)): 
        items = lines[ith_line].split()
        if items[0] == "keyexit": 
            name = items[-1]
            index = int((items[2])[1:])
            
            for room in rooms: 
                if room.id == index: 
                    exit_object = Exit(name, room, int(lines[ith_line +1][0][1:]), lst_to_str(lines[ith_line +1][1:])) 
                    #exit_object.destination = room
            index_of_room = int((items[1])[1:])
            for room in rooms: 
                if room.id == index_of_room: 
                    room.exits += [exit_object]
                        
            
            
            
    
    f.close()
    
    return World(rooms,player)
             

def makeTestWorld(usekey):
    wallet = Thing(1)
    wallet.name = 'wallet'
    wallet.description = 'A black leather wallet containing a WatCard.'
    
    keys = Thing(2)
    keys.name = 'keys'
    keys.description = 'A metal keyring holding a number of office and home keys.'
    
    phone = Thing(3)
    phone.name = 'phone'
    phone.description = 'A late-model smartphone in a Hello Kitty protective case.'
    
    coffee = Thing(4)
    coffee.name = 'cup of coffee'
    coffee.description = 'A steaming cup of black coffee.'
    
    hallway = Room(5)
    hallway.name = 'Hallway'
    hallway.description = 'You are in the hallway of a university building. \
Students are coming and going every which way.'
    
    c_and_d = Room(6)
    c_and_d.name = 'Coffee Shop'
    c_and_d.description = 'You are in the student-run coffee shop. Your mouth \
waters as you scan the room, seeing many fine foodstuffs available for purchase.'
    
    classroom = Room(7)
    classroom.name = 'Classroom'
    classroom.description = 'You are in a nondescript university classroom. \
Students sit in rows at tables, pointedly ignoring the professor, who\'s \
shouting and waving his arms about at the front of the room.'
    
    player = Player(8)
    player.name = 'Stu Dent'
    player.description = 'Stu Dent is an undergraduate Math student at the \
University of Waterloo, who is excelling at this studies despite the fact that \
his name is a terrible pun.'
    
    c_and_d.contents.append(coffee)
    player.inventory.extend([wallet,keys,phone])
    player.location = hallway
    
    hallway.exits.append(Exit('shop', c_and_d,None,''))
    ex = Exit('west', classroom,None,'')
    if usekey:
        ex.key = coffee
        ex.message = 'On second thought, it might be better to grab a \
cup of coffee before heading to class.'
    hallway.exits.append(ex)
    c_and_d.exits.append(Exit('hall', hallway,None,''))
    classroom.exits.append(Exit('hall', hallway,None,''))
    
    return World([hallway,c_and_d,classroom], player)

testworld = makeTestWorld(False)
testworld_key = makeTestWorld(True)
