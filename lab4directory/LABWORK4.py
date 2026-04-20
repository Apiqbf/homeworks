####3
class Item:
    def __init__(self,id,name,power):
        self.id=id
        self.name=name
        self.power=max(0,power)

    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return self.id==other.id
    def __str__(self):
        return f"Item(id={self.id},name={self.name},power={self.power})"

i1=Item(23,"Axe",45)
i2=Item(32,"Sword",35)
i3=Item(23,"Axe",45)
i4=Item(56,"Hammer",30)
i5=Item(60,"Chainsaw",50)

items={i1,i2,i3,i4,i5}

class Inventory:
    def __init__(self):
        self._items={}
    def __iter__(self):
        return iter(self._items.values())
    def add_item(self,item):
        if item.id not in self._items:
            self._items[item.id]=item
    def remove_item(self,item_id):
        if item_id in self._items:
            del self._items[item_id]
    def get_items(self):
        return list(self._items.values())
    def unique_items(self):
        return set(self._items.values())
    def to_dict(self):
        return dict(self._items)
    def get_strong_items(self,min_power):
        is_strong=lambda item:item.power>=min_power
        return [i for i in self._items.values() if is_strong(i)]

from datetime import datetime
class Event:
    valid_types = ["ATTACK", "HEAL", "LOOT"]
    def __init__(self,type,data):
        if type not in self.valid_types:
            raise ValueError(f"Неверный тип события:{type},требуемый:{self.valid_types}")

        self.type=type
        self.data=data
        self.timestamp=datetime.now()
    def __str__(self):
        ts=self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"Event(type-{self.type},data:{self.data},timestamp-{ts})"










####1
class Player:
    def __init__(self,id,name,hp):
        self._id=id
        self._name=name.strip().title()
        self._hp=max(0,hp)
        self._inventory=Inventory()

    def attack(self,other,amount):
        other._hp-=amount
        return f"{self._name} атаковал {other._name},player's hp={other._hp}"

    def handle_event(self,event):
        if event.type=="ATTACK":
            damage=event.data.get("damage",0)
            self._hp-=damage
        if event.type=="HEAL":
            amount=event.data.get("amount",0)
            self._hp+=amount
        if event.type=="LOOT":
            item=event.data.get("item")
            self._inventory.add_item(item)


    def __str__(self):
        return f"Player(id={self._id},name={self._name},hp={self._hp})"
    def __del__(self):
        return f"Player <{self._name}> удален"


####2
    @classmethod
    def from_string(cls,data):
        parts=data.split(";")

        if len(parts)!=3:
            raise ValueError("Неверный формат строки!")

        id=int(parts[0])
        name=parts[1]
        hp=int(parts[2])

        return cls(id,name,hp)

p1=Player(1,"Player1",100)
p2=Player(2,"Player2",100)

print(p1.attack(p2,40))

p2.handle_event(Event("HEAL",{"amount":25}))

print(p2._hp)

####3
class Item:
    def __init__(self,id,name,power):
        self.id=id
        self.name=name
        self.power=max(0,power)

    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return self.id==other.id
    def __str__(self):
        return f"Item(id={self.id},name={self.name},power={self.power})"

i1=Item(23,"Axe",45)
i2=Item(32,"Sword",35)
i3=Item(23,"Axe",45)
i4=Item(56,"Hammer",30)
i5=Item(60,"Chainsaw",50)

items={i1,i2,i3,i4,i5}











import ast
class Logger:
    def log(self,event,player,filename):
        ts=event.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        safe_data={}
        for key,value in event.data.items():
            if isinstance(value,Item):
                safe_data[key]=value.id
            else:
                safe_data[key]=value

        line=f"{ts};{player._id};{safe_data}\n"
        with open(filename,"w")as f:
            f.write(line)
    def read_logs(self,filename):
        events=[]
        with open(filename,"w")as f:
            for line in f:
                line=line.strip()
                line=line.split(";")
                event_type=line[2]
                event_data=ast.literal_eval(line[3])
                events.append(Event(event_type,event_data))

        return events

class EventIterator:
    def __init__(self,events):
        self._events=events
        self._index=0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index>=len(self._events):
            raise StopIteration
        event=self._events[self._index]
        self._index+=1
        return event

def damage_stream(events):
    for event in events:
        if event.type=="ATTACK":
            yield event.data.get("damage")

import random
def generate_events(players,items,n):
    event_types=["ATTACK","HEAL","LOOT"]
    choose_type=random.choice(event_types)

    events=[]
    for player in players:
        for _ in range(n):
            event_type=choose_type

            if event_type=="ATTACK":
                data={"damage":random.randint(10,50),"player_id":player._id}
            if event_type=="HEAL":
                data={"amount":random.randint(10,60),"player_id":player._id}
            if event_type=="LOOT":
                item=random.choice(items)
                data={"item":item,"player_id":player._id}

            events.append(Event(event_type,data))

    return events

def analyze_logs(events):
    total_damage=sum(
        e.data.get("damage") for e in events if e.type=="ATTACK"
    )

    damage_by_player={}
    for e in events:
        if e.type=="ATTACK":
            player_id=e.data.get("player_id")
            damage_by_player[player_id]=damage_by_player.get(player_id,0)+e.data.get("damage",0)

    top_player=max(damage_by_player,key=lambda pid:damage_by_player[pid])

    event_counts={}

    for e in events:
        if e.type not in event_counts:
            event_counts[e.type]=1
        else:
            event_counts[e.type]+=1

    most_common_event=max(event_counts,key=lambda e:event_counts[e])

    return {
        "total_damage":total_damage,
        "top_player":top_player,
        "most_common_event":most_common_event
    }




decide_action=lambda p:(
    "HEAL" if p._hp<50 else
    "LOOT" if len(p._inventory.get_items())<3
    else "ATTACK"
)



def analyze_inventory(inventories):
    unique_items=set()
    for inventory in inventories:
        items=inventory.get_items()

        for item in items:
            if item not in unique_items:
                unique_items.add(item)

    top_power=max(unique_items,key=lambda i:i.power)




