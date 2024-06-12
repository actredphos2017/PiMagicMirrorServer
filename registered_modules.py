from utils.define_module import ModuleEntity
#from modules.facial_recognition.main import main as facial_recognition
from modules.master.main import main as manager
from modules.messanger.main import main as messanger
from modules.voice_assistant.main import main as voice_assistant
#from modules.mobile_connector.main import main as mobile_connector

module_list: list[ModuleEntity] = [
    messanger(),
    manager(),
    voice_assistant(),
    #facial_recognition(),
    #mobile_connector(),
]
