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


class CustomSetting:
    def __init__(self, compose_structure: CustomComposeStructure):
        self.compose_structure = compose_structure

    def __dict__(self):
        return {
            "compose_structure": self.compose_structure.__dict__()
        }

    @staticmethod
    def from_dict(setting: dict):
        return CustomSetting(
            compose_structure=CustomComposeStructure.from_dict(
                setting["compose_structure"]
            )
        )

    @staticmethod
    def default():
        return CustomSetting(
            compose_structure=CustomComposeStructure.default()
        )


if __name__ == '__main__':
    print(json.dumps(CustomSetting.default().__dict__()))
