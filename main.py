import threading

from registered_modules import module_list
from utils.pipe import Pipe, Event, Notification

if __name__ == '__main__':
    pipe = Pipe()


    def logger(n: Event, _):
        print(
            n.stamp.strftime("%Y-%m-%d %H:%M:%S"),
            n.data['sender'],
            n.data['msg'],
            sep='\t'
        )


    pipe.on("LOG", logger)
    main_logger = Notification.create_notifier(pipe, "MAIN")

    for module in module_list:
        def run_module():
            try:
                module.main_function(pipe)
            except Exception as e:
                main_logger(f"Module {module.name} MEET ERROR: {e}")


        threading.Thread(target=run_module).start()
    pipe.hold()
