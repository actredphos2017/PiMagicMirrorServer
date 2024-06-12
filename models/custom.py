from datetime import datetime
import json


class Compose:
    def __init__(self, compose_id: str, params=None):
        if params is None:
            params = {}
        self.compose_id = compose_id
        self.params = params

    def __dict__(self):
        return {
            "id": self.compose_id,
            "params": self.params
        }

    @staticmethod
    def from_dict(compose: dict):
        return Compose(compose_id=compose["id"], params=compose["params"])


class CustomComposeStructure:
    def __init__(self, left: list[Compose], right: list[Compose]):
        self.left = left
        self.right = right

    def __dict__(self):
        return {
            "left": list(map(lambda c: c.__dict__(), self.left)),
            "right": list(map(lambda c: c.__dict__(), self.right))
        }

    @staticmethod
    def from_dict(composes: dict):
        return CustomComposeStructure(
            left=list(map(lambda c: Compose.from_dict(c), composes["left"])),
            right=list(map(lambda c: Compose.from_dict(c), composes["right"]))
        )

    @staticmethod
    def default():
        return CustomComposeStructure(
            left=[
                Compose('clock'),
                Compose('calendar'),
            ],
            right=[
                Compose('weather'),
            ]
        )


class CustomSingleNote:
    def __init__(self, content: str, create_time: datetime = datetime.now()):
        self.content = content
        self.create_time = create_time

    def __dict__(self):
        return {
            "content": self.content,
            "create_time": int(self.create_time.timestamp() * 1000)
        }

    @staticmethod
    def from_dict(note: dict):
        return CustomSingleNote(
            content=note["content"],
            create_time=datetime.fromtimestamp(float(note["create_time"]) / 1000)
        )


class CustomNote:
    def __init__(self, notes: list[CustomSingleNote]):
        self.notes = notes

    def __dict__(self):
        return {
            "notes": [
                (note.__dict__() if not isinstance(note, dict) else note) for note in self.notes
            ],
        }

    @staticmethod
    def from_dict(note: dict):
        return CustomNote(
            notes=note["notes"]
        )

    @staticmethod
    def default():
        return CustomNote(notes=[
            CustomSingleNote(
                content="在这里可以创建你的记事",
                create_time=datetime.now()
            )
        ])


class CustomSingleSchedule:
    def __init__(self, name: str, content: str = "", date: datetime = datetime.now()):
        self.name = name
        self.date = date
        self.content = content

    def __dict__(self):
        return {
            "name": self.name,
            "content": self.content,
            "date": int(self.date.timestamp() * 1000)
        }

    @staticmethod
    def from_dict(schedule: dict):
        return CustomSingleSchedule(
            name=schedule["name"],
            content=schedule["content"],
            date=datetime.fromtimestamp(schedule["date"] / 1000),
        )


class CustomScheduleList:
    def __init__(self, schedules: list[CustomSingleSchedule]):
        self.schedules = schedules

    @staticmethod
    def default():
        return CustomScheduleList(schedules=[
            CustomSingleSchedule(
                name="开会",
                date=datetime.now()
            )
        ])

    def __dict__(self):
        return {
            "schedules": [
                (schedule.__dict__() if not isinstance(schedule, dict) else schedule) for schedule in self.schedules
            ]
        }

    @staticmethod
    def from_dict(schedule_list: dict):
        return CustomScheduleList(schedule_list["schedules"])


class CustomSetting:
    def __init__(
            self,
            compose_structure: CustomComposeStructure,
            note: CustomNote = CustomNote.default(),
            schedule_list: CustomScheduleList = CustomScheduleList.default()
    ):
        self.compose_structure = compose_structure
        self.note = note
        self.schedule_list = schedule_list

    def __dict__(self):
        return {
            "compose_structure": self.compose_structure.__dict__(),
            "note": self.note.__dict__(),
            "schedule_list": self.schedule_list.__dict__(),
        }

    @staticmethod
    def from_dict(setting: dict):
        return CustomSetting(
            compose_structure=CustomComposeStructure.from_dict(
                setting["compose_structure"]
            ),
            note=CustomNote.from_dict(
                setting["note"]
            ),
            schedule_list=CustomScheduleList.from_dict(
                setting["schedule_list"]
            ),
        )

    @staticmethod
    def default():
        return CustomSetting(
            compose_structure=CustomComposeStructure.default(),
            note=CustomNote.default(),
            schedule_list=CustomScheduleList.default(),
        )


if __name__ == '__main__':
    print(json.dumps(CustomSetting.default().__dict__()))
