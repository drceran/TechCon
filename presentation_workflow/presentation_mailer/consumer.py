import json
import pika
import django
import os
import sys
from django.core.mail import send_mail
import time
from pika.exceptions import AMQPConnectionError


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()


def process_approval(ch, method, properties, body):
    print("  Received %r" % body)

    message = json.loads(body)
    presenter_email = message["presenter_email"]
    presenter_name = message["presenter_name"]
    title = message["title"]

    recipient_list = [presenter_email]
    from_email = "admin@conference.go"
    subject = "Your presentation has been accepted"
    message = f"{presenter_name}, we're happy to inform you that your presentation {title} has been accepted."
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )


def process_rejection(ch, method, properties, body):
    print("  Received %r" % body)

    message = json.loads(body)
    presenter_email = message["presenter_email"]
    presenter_name = message["presenter_name"]
    title = message["title"]

    recipient_list = [presenter_email]
    from_email = "admin@conference.go"
    subject = "Your presentation has been rejected"
    message = f"{presenter_name}, we're here to inform you that your presentation {title} has been rejected."
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )


while True:
    try:
        parameters = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue="presentation_approvals")
        channel.queue_declare(queue="presentation_rejections")
        channel.basic_consume(
            queue="presentation_approvals",
            on_message_callback=process_approval,
            auto_ack=True,
        )
        channel.basic_consume(
            queue="presentation_rejections",
            on_message_callback=process_rejection,
            auto_ack=True,
        )
        channel.start_consuming()
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
