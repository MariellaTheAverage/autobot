import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

class EntryRequest:
    def __init__(self, date, time, place) -> None:
        self.Date = date
        self.Time = time
        self.Place = place

def main():
    session = vk_api.VkApi(token='vk1.a.kMtsEwP0865Fsp0czDXxzx_HTIrmtRj1OIrXMB2Yj57sqIsKL0fNdHYQAaND_hr3k6VdHX7Rm9ZtcLwub_Mkg2yH3_j8FT7pheOtA_34jJ23t7fdyxozyE244tVZybCEtMAXhATwylCTu3fHw5HJ7ovlgz618_uB8vFw_KYqf_PJM-aMa5Y-d_kf6YuOKD89aYk-Mffi8t6xZzZ14dezyQ')
    longpoll = VkLongPoll(session)
    vk = session.get_api()
    print("Started successfully")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print(f"* >>> Received a message: {event.message}")
            vk.messages.send(user_id=event.user_id, message="Test response", random_id=0)

if __name__ == '__main__':
    main()