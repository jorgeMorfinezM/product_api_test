# -*- coding: utf-8 -*-
"""
Requires Python 3.0 or later
"""

__author__ = "Jorge Morfinez Mojica (jorgemorfinez@ofix.mx)"
__copyright__ = "Copyright 2020, Jorge Morfinez Mojica"
__license__ = ""
__history__ = """ Email script to notify about change of data to Product object"""
__version__ = "1.21.H28.1 ($Rev: 1 $)"

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import email.mime.application
from logger_controller.logger_control import *

cfg_app = get_config_settings_app()

logger = configure_logger('api')


# Metodo para enviar el correo electronico con la notificacion de cambio
def email_notifier(sku_producto, nombre_producto, data_updated, email_recipients):

    port = cfg_app.email_port.__str__()
    smtp_server = cfg_app.email_smtp_server.__str__()
    sender_email = cfg_app.email_user.__str__()
    password = cfg_app.email_password.__str__()

    # recipients = [cfg['EMAIL_RECEIVER'], cfg['EMAIL_RECEIVER2']]

    logger.info('Email Recipients: %s', email_recipients)

    subject = "El producto " + sku_producto + " - " + nombre_producto + " ha sido Actualizado"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = ", ".join(email_recipients)

    # Create the plain-text and HTML version of your message
    text = """\
           Hola!,
           
           Te informamos que los datos de un producto han sido actualizados.

           Los datos actualizados del producto son:""" + f"{str(data_updated)}" + " \n Saludos!"

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    # part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # attach_file = attach_file_to_email(file_attached, file_name)
    #
    # message.attach(attach_file)
    #
    # logger.info('Email File attached: %s', file_name)

    # Create secure connection with server and send email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)

        server.sendmail(
            sender_email, recipients, message.as_string()
        )

        logger.info('Email sending: %s', 'Server: {}, User: {}, Subject: {}'.format(smtp_server, sender_email, subject))

    server.close()


def attach_file_to_email(file_to_atach, file_name):
    attach_file = open(file_to_atach, 'rb')  # open the file
    # report = MIMEBase("application", "octate-stream")  #quiza vaya

    attach_f = email.mime.application.MIMEApplication(attach_file.read(), subtype="pdf")

    attach_file.close()

    # report.set_payload(attach_file.read())
    # encoders.encode_base64(attach_f)
    # add report header with the file name

    attach_f.add_header('Content-Disposition', 'attachment', filename=file_name)

    return attach_f

