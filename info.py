import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import mysql.connector as mysql
import datetime as dt
# ^ again, vscode doesn't like this import but it works

class EntryRequest:
    def __init__(self, date: dt.date, tstart: dt.time, tend: dt.time, place, object, uid: int, phone=None) -> None:
        self.Date = date
        self.Start = tstart
        self.End = tend
        self.Place = place
        self.Object = object
        self.Contact = uid
        self.Phone = phone

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

    def get_driver_stats(self, did: int) -> int:
        cmd = (f"select pickupcnt from drivers where uid={did}")
        self.cur.execute(cmd)
        res = [entry for entry in self.cur]
        return res[0][0]

    def add_new_driver(self, uid: int) -> None:
        cmd = (f"insert into drivers (uid, pickupcnt) values ({uid}, 0)")
        self.cur.execute(cmd)
        self.conn.commit()
        self.drivers.append(uid)

    def publish_order(self, odr: EntryRequest, time_flag: bool) -> None:
        if odr.Phone != None:
            cmd = ("insert into orders (address, item, day, tstart, tend, usrid, phone) "
                "values (%s, %s, %s, %s, %s, %s, %s)")
            data = (odr.Place, odr.Object, odr.Date, odr.Start, odr.End, odr.Contact, odr.Phone)
        else:
            cmd = ("insert into orders (address, item, day, tstart, tend, usrid) "
                "values (%s, %s, %s, %s, %s, %s)")
            data = (odr.Place, odr.Object, odr.Date, odr.Start, odr.End, odr.Contact)
        self.cur.execute(cmd, data)
        self.conn.commit()

    def check_if_driver(self, uid) -> bool:
        return uid in self.drivers

class Bot:
    def __init__(self) -> None:
        self.session = vk_api.VkApi(token='vk1.a.kMtsEwP0865Fsp0czDXxzx_HTIrmtRj1OIrXMB2Yj57sqIsKL0fNdHYQAaND_hr3k6VdHX7Rm9ZtcLwub_Mkg2yH3_j8FT7pheOtA_34jJ23t7fdyxozyE244tVZybCEtMAXhATwylCTu3fHw5HJ7ovlgz618_uB8vFw_KYqf_PJM-aMa5Y-d_kf6YuOKD89aYk-Mffi8t6xZzZ14dezyQ')
        self.longpoll = VkLongPoll(self.session)
        self.vk = self.session.get_api()
        self.connector = DatabaseConnector()
        print("Started successfully")
        # print(f"List of current drivers: {self.connector.drivers}")

    def process(self, msg, role):
        pass

    def Listen(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
                print(f"* >>> Received a message: {event.message} \n From: {event.user_id} / {event.from_user}")

                user_role = 'user'
                if event.user_id == 121434527:
                    user_role = 'admin'
                if self.connector.check_if_driver(event.user_id):
                    user_role = 'driver'

                self.process(event.message, user_role)
                # self.vk.messages.send(user_id=event.user_id, message="Test response", random_id=0)

def main():
    bot = Bot()
    exampleorder = EntryRequest(
        dt.date.today(), dt.time(14, 30, 00), dt.time(15, 00, 00), 
        "address", "stuff", 121434527
    )
    # print(bot.connector.get_driver_stats(121434527))
    # bot.Listen()

if __name__ == '__main__':
    main()