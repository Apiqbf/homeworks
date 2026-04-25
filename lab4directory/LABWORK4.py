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

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, value)

    @property
    def inventory(self):
        return self._inventory

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

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


class Warrior(Player):
    def handle_event(self, event: Event):
        if event.type == "ATTACK":
            damage=event.data.get("damage", 0)
            damage=damage * 0.9
            event.data["damage"]=damage
        super().handle_event(event)


class Mage(Player):
    def handle_event(self, event: Event):
        if event.type == "LOOT":
            item = event.data.get("item")
            if item:
                item.power = int(item.power * 1.1)
        super().handle_event(event)



sword = Item(1, "Sword", 50)
warrior = Warrior(1, "Thor", 100)
warrior.handle_event(Event("ATTACK", {"damage": 20}))
#print(warrior)


mage = Mage(2, "Merlin", 100)
mage.handle_event(Event("LOOT", {"item": sword}))
#print(sword.power)

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

        line=f"{ts};{player._id};{event.type};{safe_data}\n"
        with open(filename,"w")as f:
            f.write(line)

    def read_logs(self,filename):
        events=[]
        with open(filename,"r")as file:
            for line in file:
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

    top_player=max(damage_by_player,key=lambda pid:damage_by_player[pid]) if damage_by_player else None

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
    all_items=[item for inv in inventories for item in inv]

    unique=set(all_items)

    top=max(all_items, key=lambda item: item.power) if all_items else None

    return {
        "unique_items": unique,
        "top_power": top
    }




def main():
    players=[
        Warrior(1, "Thor", 100),
        Mage(2, "Merlin", 100),
        Player(3,"Robin", 80)
    ]
    items=[
        Item(1,"Sword",50),
        Item(2,"Shield",30),
        Item(3,"Axe",70),
        Item(4,"Staff",60)
    ]

    events=generate_events(players,items,n=5)

    logger = Logger()
    open("game.log", "w").close()

    for event in events:
        player_id = event.data.get("player_id")
        player = next((p for p in players if p._id == player_id), None)
        if player:
            player.handle_event(event)
            logger.log(event, player, "game.log")

    logged_events=logger.read_logs("game.log")
    print(f"\nВсего записано событий:{len(logged_events)}")

    result=analyze_logs(events)
    print(f"Общий урон:{result['total_damage']}")
    print(f"Игрок с наибольшим уроном:{result['top_player']}")
    print(f"Самое частое событие:{result['most_common_event']}")

    top_inventory=max(players,key=lambda p:len(p.inventory.get_items()))
    print(f"Игрок с наибольшим инвентарём:{top_inventory}")

    inv_result = analyze_inventory([p.inventory for p in players])
    print(f"Уникальных предметов: {len(inv_result['unique_items'])}")
    print(f"Самый мощный предмет: {inv_result['top_power']}")

    print("\nСостояние игроков:")
    for p in players:
        print(p)


main()