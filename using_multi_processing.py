from multiprocessing import Pool
import sys
from time import sleep
from asyncua import Client, Node, ua

import cnc_module
import robot_module


def callback_from_any_module(result_list):
    x=result_list
    #channel, cell_module,module_instruction, results_passed_in  = [result_list[i] for i in (range(0,2))]
    channel, cell_module, module_instruction, results_passed_in  = [result_list[i] for i in (range(0,4))]

    a = channel
    b = cell_module
    print("[callback_from_any_module] The {} module called in channel: {} returned: {} . this is where we would write back to PLC on correct channel.".format(cell_module, channel, results_passed_in))

    ## write to opcua var to blindly communicate the results from this module
    ## some function or inline code to do this



def master_commander_in_chief():
    # commenting out, since this is just a demonstration, won't actually connect to opc client
    #async with Client(url='http://127 - etc...') as client:

        ## poll the opcua server perpetually
        while True:
            try:
                print('[master_commander_in_chief] Waiting for instructions...')
                ## pool for 4, reset every time you are in while true - all pooled processes will complete prior to returning to the beginning of this while, again
                pool=Pool()
                results = []
                ## 4 channels
                for num in list(range(1,5)):
                    channel = 'CHANNEL_' + str(num)
                    ## "listen" on channel x
                    # commenting out, since this is just a demonstration, won't actually connect to opc client
                    #opcua_var = client.get_node("ns=4;s=|var|CODESYS Control for Raspberry Pi MC SL.Application.PLC_PRG.CHANNEL_1")
                    #opcua_var_content = await opcua_var.read_value()

                    # dummy for now, let's say we got a value on channel x ...
                    opcua_var_content = None
                    if channel == 'CHANNEL_1':
                        opcua_var_content = 'ROBOT|Pick_Stock'
                    elif channel == 'CHANNEL_2':
                        # simulate nothing coming thru on this channel from PLC
                        pass
                    elif channel == 'CHANNEL_3':
                        opcua_var_content = 'CNC|Open_Door'
                    elif channel == 'CHANNEL_4':
                        # simulate nothing coming thru on this channel from PLC
                        pass


                    ## if we have content coming thru on channel x, do something...
                    if opcua_var_content != '' and opcua_var_content is not None:
                        ## content from channel will contain two pieces of info. which piece of hardware that needs to be controlled and what to do on that hardware
                        ## pipe delimiting the info would work well, since it would be error-prone to divide that info into two opcua vars
                        ## hardware = module
                        cell_module,module_instruction = opcua_var_content.split('|')

                        print("[master_commander_in_chief] {} was just instructed by PLC to do: {} on channel: {}".format(cell_module,module_instruction,channel))

                        # pass the instructions to the appropriate module. also pass channel to maintain "state," as it were
                        if cell_module == 'ROBOT':
                            args = [channel,module_instruction]
                            r = pool.apply_async(robot_module.robot_main, args, callback=callback_from_any_module)
                            results.append(r)
                            print("[master_commander_in_chief] just issued instruction to {} to do: {} on channel: {}".format(cell_module,module_instruction,channel))

                        elif  cell_module == 'CNC':
                            a=1
                            args = [channel,module_instruction]
                            r = pool.apply_async(cnc_module.cnc_main, args, callback=callback_from_any_module)
                            results.append(r)
                            print("[master_commander_in_chief] just issued instruction to {} to do: {} on channel: {}".format(cell_module,module_instruction,channel))

                for r in results:
                    r.wait()

                print("[master_commander_in_chief] done with for loop, sleeping at the bottom of while loop")
                print("......................................................\n\n\n")
                sleep(2)
            except Exception as e:
                print("bad. exception. {}".format(e))




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    master_commander_in_chief()


