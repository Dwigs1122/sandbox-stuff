from time import sleep

def cnc_main(channel, module_instruction):
    print("[CNCModule.cnc_main] CNC module here. I am operating in {}. I was just instructed to do: {}".format(channel,module_instruction), flush=True)

    # here is where the logic belongs for deciding which method/function to call based on info originating from plc:
    if module_instruction == 'Open_Door':
        open_door()

    elif module_instruction == 'Close_Door':
        close_door()


    print("[CNCModule.cnc_main] CNC module again, I am in {}. just finished doing: {}".format(channel, module_instruction), flush=True)

    results = "done. success. etc. or maybe i return metrics."
    result_list = [channel, 'cnc_main',module_instruction, results]



    return result_list

def open_door():
    print("[CNCModule.open_door] starting open_door method", flush=True)
    sleep(4)
    print("[CNCModule.open_door] done with opening door.", flush=True)


def close_door():
    print("[CNCModule.close_door] starting close_door method", flush=True)
    sleep(1)
    print("[CNCModule.close_door] done with closing door", flush=True)

