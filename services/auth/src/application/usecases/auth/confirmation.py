from dataclasses import dataclass

from src.application.contracts.commands.user import UserConfirmationCommand


@dataclass
class UserConfirmationUseCase:

    async def execute(self, command: UserConfirmationCommand):
        return {"id": command.id, "code": command.code}
