from time import sleep


def robot_main(channel, module_instruction):
    # Use a breakpoint in the code line below to debug your script.

    print("[robot_main] Robot module here. I am operating in {}. I was just instructed to do: {}".format(channel,module_instruction))
    sleep(1)
    print("[robot_main] Robot module again, I am in {}. just finished doing: {}".format(channel, module_instruction))
    results = "done. success. etc. or maybe i return metrics."
    result_list = [channel, 'robot_main',module_instruction, results]
    return result_list

