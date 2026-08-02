from pathlib import Path
from typing import Type, TypeVar

import pandas as pd
from pydantic import BaseModel

from schemas.incoming_message import IncomingMessage
from schemas.users import UserProfile
from schemas.groups import Group
from schemas.group_membership import GroupMembership
from schemas.business import BusinessAccount
from schemas.user_business_history import UserBusinessHistory
from schemas.message_events import MessageEvents
from schemas.images import ImageFile
from schemas.voice_notes import VoiceFile
from schemas.daily_notification import DailyNotification

T = TypeVar("T", bound=BaseModel)


class DataLoader:

    def __init__(self, dataset_path: str | Path = Path(__file__).resolve().parent.parent.parent):

        self.dataset_path = Path(dataset_path)

        self.messages = self.load_csv(
            "messages.csv",
            IncomingMessage
        )

        self.users = self.load_csv(
            "users.csv",
            UserProfile
        )

        self.groups = self.load_csv(
            "groups.csv",
            Group
        )

        self.group_members = self.load_csv(
            "group_members.csv",
            GroupMembership
        )

        self.business_accounts = self.load_csv(
            "business_accounts.csv",
            BusinessAccount
        )

        self.user_business_history = self.load_csv(
            "user_business_history.csv",
            UserBusinessHistory
        )

        self.message_history = self.load_csv(
            "message_history.csv",
            IncomingMessage
        )

        self.message_events = self.load_csv(
            "message_events.csv",
            MessageEvents
        )

        self.images = self.load_csv(
            "images.csv",
            ImageFile
        )

        self.voice_notes = self.load_csv(
            "voice_notes.csv",
            VoiceFile
        )

        self.daily_notification_summary = self.load_csv(
            "daily_notification_summary.csv",
            DailyNotification
        )

    def load_csv(
        self,
        filename: str,
        model: Type[T]
    ) -> list[T]:

        file_path = self.dataset_path/"dataset"/filename
        df = pd.read_csv(file_path)

        records = []

        for row in df.to_dict(orient="records"):

            cleaned = {
                key: (None if pd.isna(value) else value)
                for key, value in row.items()
            }

            records.append(model(**cleaned))

        return records


if __name__ == "__main__":

    loader = DataLoader()

    print(f"Messages : {len(loader.messages)}")
    print(f"Users    : {len(loader.users)}")
    print(f"Groups   : {len(loader.groups)}")