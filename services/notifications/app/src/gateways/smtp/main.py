import logging
import smtplib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

logger = logging.getLogger()


@dataclass
class BaseSMTPServer(ABC):
    @abstractmethod
    async def start(self): ...

    @abstractmethod
    def create_message(self, content: str, to_address: str) -> MIMEMultipart: ...

    @abstractmethod
    async def send_email(self, message: MIMEMultipart) -> None: ...

    @abstractmethod
    async def stop(self): ...

    @abstractmethod
    async def check_connection(self): ...


@dataclass
class SyncSMTPServer(BaseSMTPServer):
    server: smtplib.SMTP_SSL
    from_address: str
    password: str
    subject: str

    def start(self) -> None:
        self.server.login(self.from_address, self.password)

    def create_message(self, content: str, to_address: str) -> EmailMessage:
        message = EmailMessage()
        message["Subject"] = self.subject
        message["From"] = self.from_address
        message["To"] = to_address
        message.set_content(content)
        return message

    def send_email(self, message: EmailMessage) -> None:
        self.server.send_message(message)

    def stop(self) -> None:
        self.server.quit()


@dataclass
class AsyncSMTPServer(BaseSMTPServer):
    server: aiosmtplib.SMTP
    from_address: str
    password: str
    subject: str

    async def start(self) -> None:
        logger.info("Starting smtp server")
        await self.server.connect()

    def create_message(self, content: str, to_address: str) -> MIMEMultipart:
        message = MIMEMultipart()
        message["Subject"] = self.subject
        message["From"] = self.from_address
        message["To"] = to_address
        html = MIMEText(content, "html")
        message.attach(html)
        return message

    async def send_email(self, message: MIMEMultipart) -> None:
        return await self.server.sendmail(
            self.from_address,
            message["To"],
            message.as_string(),
        )

    async def stop(self) -> None:
        logger.info("Stopping smtp server")
        await self.server.quit()

    async def check_connection(self):
        if self.server.is_connected == False:
            self.server.close()
            await self.server.connect()
