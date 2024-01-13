import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime as dt
import requests
import mysql.connector as mysql
# ^ again, vscode doesn't like this import but it works
# look into tg bots

class EntryRequest:
    def __str__(self) -> str:
        pass

    def __init__(self, place="", object="", uid="", addl="", phone=None) -> None:
        self.Addl = addl
        self.Place = place
        self.Object = object
        self.Contact = uid
        self.Phone = phone

# mysql connection class
class DatabaseConnector:
    def __init__(self) -> None:
        self.conn = mysql.connect(user='bot', password='SdZBB!9vUW&U]VofDfum', host='localhost', database='shelter_orders')
        self.cur = self.conn.cursor()
        self.drivers = []

        driver_query = ("select uid from drivers")
        self.cur.execute(driver_query)
        for driver in self.cur:
            self.drivers.append(driver[0])

    def __del__(self):
        self.cur.close()
        self.conn.close()

    # get statistics for a specific driver id (maybe leaderboard later)
    def get_driver_stats(self, did: int) -> int:
        cmd = (f"select pickupcnt from drivers where uid={did}")
        self.cur.execute(cmd)
        res = [entry for entry in self.cur]
        return res[0][0]

    # add new driver entry into the database
    def add_new_driver(self, uid: int) -> None:
        cmd = (f"insert into drivers (uid, pickupcnt) values ({uid}, 0)")
        self.cur.execute(cmd)
        self.conn.commit()
        self.drivers.append(uid)

    # create new active order
    def publish_order(self, odr: EntryRequest) -> None:
        if odr.Phone != None:
            cmd = ("insert into orders (address, item, usrid, phone, addlinfo) "
                "values (%s, %s, %s, %s, %s)")
            data = (odr.Place, odr.Object, odr.Contact, odr.Phone, odr.Addl)
        else:
            cmd = ("insert into orders (address, item, usrid, addlinfo) "
                "values (%s, %s, %s, %s)")
            data = (odr.Place, odr.Object, odr.Contact, odr.Addl)
        self.cur.execute(cmd, data)
        self.conn.commit()

    # get all orders from a person
    def get_orders_by_person(self, uid: int) -> list:
        cmd = ("select * from orders "
               f"where uid={uid} "
               "order by taken")

    # get a list of all active orders with the unassigned ones going first
    def get_active_orders(self) -> list:
        cmd = ("select * from orders "
               "where taken=0 "
               "order by assigned")
        
        self.cur.execute(cmd)
        res = [entry for entry in self.cur]
        return res

    # check if the current user is a driver without looking into the database
    def check_if_driver(self, uid: int) -> bool:
        return uid in self.drivers

class Bot:
    def __init__(self) -> None:
        self.session = vk_api.VkApi(token='vk1.a.kMtsEwP0865Fsp0czDXxzx_HTIrmtRj1OIrXMB2Yj57sqIsKL0fNdHYQAaND_hr3k6VdHX7Rm9ZtcLwub_Mkg2yH3_j8FT7pheOtA_34jJ23t7fdyxozyE244tVZybCEtMAXhATwylCTu3fHw5HJ7ovlgz618_uB8vFw_KYqf_PJM-aMa5Y-d_kf6YuOKD89aYk-Mffi8t6xZzZ14dezyQ')
        self.longpoll = VkLongPoll(self.session)
        self.vk = self.session.get_api()
        self.connector = DatabaseConnector()
        self.ctxs = dict()
        self.sync_roles()
        print("Started successfully")

    # store all roles in context dictionary
    def sync_roles(self):
        for uid in self.connector.drivers:
            self.ctxs[uid] = 'driver'
        self.ctxs[121434527] = 'admin'

    # generate a response based on the message and context of the conversation
    def process(self, msg, role):
        pass

    def Listen(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
                print(f"* >>> Received a message: {event.message} \n From: {event.user_id} / {event.from_user}")

                if event.user_id not in self.ctxs:
                    self.ctxs[event.user_id] = 'user'

                self.process(event.message, self.ctxs[event.user_id])
                # self.vk.messages.send(user_id=event.user_id, message="Test response", random_id=0)

def main():
    bot = Bot()
    # print(bot.connector.get_driver_stats(121434527))
    # bot.Listen()

if __name__ == '__main__':
    main()