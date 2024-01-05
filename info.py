import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import mysql.connector as mysql
# ^ again, vscode doesn't like this import but it works

class EntryRequest:
    def __init__(self, date, tstart, tend, place, object, phone=None) -> None:
        self.Date = date
        self.Start = tstart
        self.End = tend
        self.Place = place
        self.Object = object
        self.Phone = phone

class DatabaseConnector:
    def __init__(self) -> None:
        self.conn = mysql.connect(user='bot', password='SdZBB!9vUW&U]VofDfum', host='localhost', database='shelter_orders')
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def check_if_driver(self, uid) -> bool:
        pass

class Bot:
    def __init__(self) -> None:
        self.session = vk_api.VkApi(token='vk1.a.kMtsEwP0865Fsp0czDXxzx_HTIrmtRj1OIrXMB2Yj57sqIsKL0fNdHYQAaND_hr3k6VdHX7Rm9ZtcLwub_Mkg2yH3_j8FT7pheOtA_34jJ23t7fdyxozyE244tVZybCEtMAXhATwylCTu3fHw5HJ7ovlgz618_uB8vFw_KYqf_PJM-aMa5Y-d_kf6YuOKD89aYk-Mffi8t6xZzZ14dezyQ')
        self.longpoll = VkLongPoll(self.session)
        self.vk = self.session.get_api()
        self.connector = DatabaseConnector()
        print("Started successfully")

    def process(self, msg, role):
        pass

    def Listen(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
                print(f"* >>> Received a message: {event.message} \n From: {event.user_id} / {event.from_user}")
                user_role = 'user'
                if event.user_id == 121434527:
                    user_role = 'admin'
                self.process(event.message, user_role)
                # self.vk.messages.send(user_id=event.user_id, message="Test response", random_id=0)

def main():
    bot = Bot()
    bot.Listen()

if __name__ == '__main__':
    main()