####3
class Item:
    def __init__(self,id:int,name:str,power:int):
        self.id=id
        self.name=name.strip().title()
        self.power=power if power>=0 else 0

    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return self.id==other.id
    def __str__(self):
        return f"Item(id={self.id},name={self.name},power={self.power})"
    def __repr__(self):
        return self.__str__()

i1=Item(12455,"Dildo",45)
i2=Item(234,"Probka analnaya",34)
i3=Item(12455,"Dildo",45)
i4=Item(234,"Probka analnaya",34)

items={i1,i2,i3,i4}

####4
class Inventory:
    def __init__(self):
        self._items={}
####18
    def __iter__(self):
        return iter(self._items.values())
    def add_item(self,item:Item):
        if item.id not in self._items:
            self._items[item.id]=item
    def remove_item(self,item_id:int):
        if item_id in self._items:
            del self._items[item_id]
    def get_items(self):
        return list(self._items.values())
    def unique_items(self):
        return set(self._items.values())
    def to_dict(self):
        return dict(self._items)
####5
    def get_strong_items(self,min_power: int):
        is_strong=lambda item:item.power>=min_power
        return [item for item in self._items.values() if is_strong(item)]



inv=Inventory()

inv.add_item(i1)
inv.add_item(i2)
inv.add_item(i3)
inv.add_item(i4)

#for item in inv:
    #print(item)

strong=[item for item in inv if item.power>40]
#print(strong)
####6
from datetime import datetime
class Event:
    VALID_TYPES=["ATTACK","HEAL","LOOT"]

    def __init__(self,type:str,data:dict):
        if type not in self.VALID_TYPES:
            raise ValueError(f"Неверный тип действия:{type},требуемый-{self.VALID_TYPES}")

        self.type=type
        self.data=data
        self.timestamp=datetime.now()
    def __str__(self):
        ts=self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"Event(type-{self.type},data:{self.data},timestamp-{ts})"

e=Event("HEAL",{"damage":45})


####1
class Player:
     def __init__(self,id:int,name:str,hp:int):
         self._id=id
         self._name=name.strip().title()
         self._hp=max(0,hp)
####7
         self._inventory=Inventory()
     def handle_event(self,event:Event):
         if event.type=="ATTACK":
             damage=event.data.get("damage")
             self._hp-=damage
         if event.type=="HEAL":
             heal=event.data.get("amount")
             self._hp+=heal
         if event.type=="LOOT":
             item=event.data.get("item")
             self._inventory.add_item(item)
####16
     @property
     def hp(self):
         return self._hp

     @hp.setter
     def hp(self,value):
         self._hp=max(0,value)

     @property
     def inventory(self):
         return self._inventory

     @property
     def name(self):
         return self._name

     @property
     def id(self):
         return self._id

####2
     @classmethod
     def from_string(cls,data:str):
         parts=data.split(",")

         if len(parts)!=3:
             raise ValueError(f"Неверный формат данных:{data}")

         id=int(parts[0])
         name=parts[1]
         hp=int(parts[2])

         return cls(id,name,hp)
####1
     def __str__(self):
         return f"Player(id={self._id},name={self._name},hp={self._hp})"
     def __del__(self):
         return f"Player <{self._name}> удален"

####7
class Warrior(Player):
    def handle_event(self,event:Event):
        if event=="ATTACK":
            damage=event.data().get("damage")
            reduced = int(damage * 0.9)
            event["damage"]=reduced
        super().handle_event(event)


class Mage(Player):
    def handle_event(self,event:Event):
        if event=="LOOT":
            item=event.data.get("item")
            item.power = int(item.power * 1.1)
        super().handle_event(event)



sword = Item(1, "Sword", 50)

warrior = Warrior(1, "Thor", 100)
warrior.handle_event(Event("ATTACK", {"damage": 20}))


mage = Mage(2, "Merlin", 100)
mage.handle_event(Event("LOOT", {"item": sword}))


####8
import ast
class Logger:
    def log(self,event:Event,player:Player,filename:str):
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

####9
    def read_logs(self,filename:str):
        events=[]
        with open(filename,"r")as f:
            for line in f:
                line=line.strip()
                parts=line.split(";")
                event_type=parts[2]
                event_data=ast.literal_eval(parts[3])
                events.append(Event(event_type,event_data))
        return events




# logger=Logger()
#
# logger.log(Event("ATTACK",{"damage":20}),warrior,"game.log")
# logger.log(Event("HEAL",{"amount":15}),warrior,"game.log")
# logger.log(Event("LOOT",{"item_id":1}),warrior,"game.log")
#
#
#
# events=logger.readlogs("game.log")
#
# for e in events:
#     print(e)


####10
class EventIterator:
    def __init__(self,events:list):
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

# events=[
#     Event("ATTACK", {"damage": 20}),
#     Event("HEAL", {"amount": 15}),
#     Event("LOOT", {"item_id": 1})
# ]
#
# iterator=EventIterator(events)

####11
def damage_stream(events:list):
    for event in events:
        if event.type=="ATTACK":
            yield event.data.get("damage")


# events = [
#     Event("ATTACK", {"damage": 20}),
#     Event("HEAL", {"amount": 15}),
#     Event("ATTACK", {"damage": 35}),
#     Event("LOOT", {"item_id": 1}),
#     Event("ATTACK", {"damage": 10}),
# ]
#
# for damage in damage_stream(events):
#     print(damage)


####12
import random
def generate_events(players:list,items:list,n:int):
    event_types=["ATTACK","HEAL","LOOT"]
    choose_type=lambda:random.choice(event_types)

    events=[]
    for player in players:
        for _ in range(n):
            event_type=choose_type()

            if event_type=="ATTACK":
                data={"damage":random.randint(10,50),"player_id":player._id}
            if event_type=="HEAL":
                data={"amount":random.randint(10,50),"player_id":player._id}
            if event_type=="LOOT":
                item=random.choice(items)
                data={"item":item,"player_id":player._id}

            events.append(Event(event_type,data))

    return events


players=[Warrior(1,"Thor",100),Mage(2,"Merlin",100)]
items=[Item(1,"sword",45),Item(2,"axe",60)]

generator=generate_events(players,items,5)


####13
def analyze_logs(events:list):
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
        event_counts[e.type]=event_counts.get(e.type,0)+1

    most_common_event=max(event_counts,key=lambda t:event_counts[t])

    return {
        "total_damage":total_damage,
        "top_player":top_player,
        "most_common_event":most_common_event
    }

####14
decide_action=lambda player:(
    "HEAL" if player._hp<50 else
    "LOOT" if len(player._inventory.get_items())<3
    else "ATTACK"
)




####19
def analyze_inventory(inventories:list):
    unique_items=set()

    for inventory in inventories:
        items=inventory.get_items()
        for item in items:
            if item not in unique_items:
                unique_items.add(item)

    top_power=max(unique_items,key=lambda i:i.power)

    return {
        "unique_items":unique_items,
        "top_power":top_power
    }

inv1 = Inventory()
inv1.add_item(Item(1, "Sword", 50))
inv1.add_item(Item(2, "Shield", 30))

inv2 = Inventory()
inv2.add_item(Item(2, "Shield", 30))  # дубликат
inv2.add_item(Item(3, "Axe", 70))

inventories = [inv1, inv2]

result = analyze_inventory(inventories)



####20
def main():
    players = [
        Warrior(1, "Thor", 100),
        Mage(2, "Merlin", 100),
        Player(3, "Robin", 80)
    ]
    items = [
        Item(1, "Sword", 50),
        Item(2, "Shield", 30),
        Item(3, "Axe", 70),
        Item(4, "Staff", 60)
    ]

    # 2. Генерируем события
    events = generate_events(players, items, n=5)

    # 3. Обрабатываем события для каждого игрока
    logger = Logger()
    open("game.log", "w").close()  # очищаем файл

    for event in events:
        player_id = event.data.get("player_id")
        player = next((p for p in players if p._id == player_id), None)
        if player:
            player.handle_event(event)
            logger.log(event, player, "game.log")

    # 4. Читаем логи
    logged_events = logger.read_logs("game.log")
    print(f"\nВсего записано событий: {len(logged_events)}")

    # 5. Аналитика
    result = analyze_logs(events)
    print(f"Общий урон: {result['total_damage']}")
    print(f"Игрок с наибольшим уроном: {result['top_player']}")
    print(f"Самое частое событие: {result['most_common_event']}")

    # Игрок с максимальным количеством предметов
    top_inventory = max(players, key=lambda p: len(p.inventory.get_items()))
    print(f"Игрок с наибольшим инвентарём: {top_inventory}")

    # Общая статистика предметов
    inv_result = analyze_inventory([p.inventory for p in players])
    print(f"Уникальных предметов: {len(inv_result['unique_items'])}")
    print(f"Самый мощный предмет: {inv_result['top_power']}")

    # Состояние игроков
    print("\nСостояние игроков:")
    for p in players:
        print(p)


main()