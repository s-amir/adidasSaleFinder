import os
import time

import django
from user.models import User


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adidasSaleFinder.settings')
django.setup()
import pywhatkit
from datetime import datetime
from crawler.models import SaleProduct


def send_whatsapp_msg(contact_number, msg):
    now1 = datetime.now()
    current_time_hour = int(now1.strftime("%H"))
    current_time_minute = int(now1.strftime("%M")) + 1
    pywhatkit.sendwhatmsg(contact_number, msg, current_time_hour, current_time_minute)


# send_whatsapp_msg('+989102101536','new msg')


def send_sale_product_to_user():
    message_header = "---Adidas Sale Finder---\n\n"
    objects = SaleProduct.objects.all()
    users = User.objects.all()
    message = ""
    number = 0
    for object in objects:
        number += 1
        message = message + f"{number}){object}\n"

    # send message to all registered user
    for user in users:
        user_name_text=f"Hello {user.name}\n"
        user_number=user.phone_number
        complete_message=message_header+user_name_text+message
        send_whatsapp_msg(user_number, complete_message)
        time.sleep(3.0)




# send_sale_product_to_user()
