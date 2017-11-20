#!/usr/bin/python3
import melee
import keras
import argparse
import signal
import myMenuHelper
import sys

#This example program demonstrates how to use the Melee API to run dolphin programatically,
#   setup controllers, and send button presses over to dolphin

def check_port(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 4:
         raise argparse.ArgumentTypeError("%s is an invalid controller port. \
         Must be 1, 2, 3, or 4." % value)
    return ivalue

def signal_handler(signal, frame):
    dolphin.terminate()
    if args.debug:
        log.writelog()
        print("") #because the ^C will be on the terminal
        print("Log file created: " + log.filename)
    print("Shutting down cleanly...")
    if args.framerecord:
        framedata.saverecording()
    sys.exit(0)

def main():
    chain = None

    parser = argparse.ArgumentParser(description='Example of libmelee in action')
    parser.add_argument('--port', '-p', type=check_port,
                        help='The controller port your AI will play on',
                        default=2)
    parser.add_argument('--opponent', '-o', type=check_port,
                        help='The controller port the opponent will play on',
                        default=1)
    parser.add_argument('--debug', '-d', action='store_true',
                        help='Debug mode. Creates a CSV of all game state')
    parser.add_argument('--framerecord', '-r', default=False, action='store_true',
                        help='Records frame data from the match, stores into framedata.csv')
    #parser.add_argument('model', '-m', type=str, default="",
    #                    help='The file of the AI')

    args = parser.parse_args()

    log = None
    if args.debug:
        log = melee.logger.Logger()

    framedata = melee.framedata.FrameData(args.framerecord)
    opponent_type = melee.enums.ControllerType.UNPLUGGED

    #Create our Dolphin object. This will be the primary object that we will interface with
    dolphin = melee.dolphin.Dolphin(ai_port=args.port, opponent_port=args.opponent,
        opponent_type=opponent_type, logger=log)
    #Create our GameState object for the dolphin instance
    gamestate = melee.gamestate.GameState(dolphin)
    #Create our Controller object that we can press buttons on
    controller = melee.controller.Controller(port=args.port, dolphin=dolphin)
    #controller2 = melee.controller.Controller(port=1, dolphin=dolphin)


    signal.signal(signal.SIGINT, signal_handler)

    #Run dolphin and render the output
    dolphin.run(render=False)

    #Plug our controller in
    #   Due to how named pipes work, this has to come AFTER running dolphin
    #   NOTE: If you're loading a movie file, don't connect the controller,
    #   dolphin will hang waiting for input and never receive it
    controller.connect()
    #controller2.connect()

    model = []
    #if args.model == "":
    #    pass
        #model = createModel()
    #else:
    #    pass
        #model = keras.models.load_model('models/' + args.model)

    #Main loop
    i = 0
    pickedCPU = 0
    while True:
        i += 1
        i = i % 101
        #"step" to the next frame
        gamestate.step()
        if(gamestate.processingtime * 1000 > 12):
            print("WARNING: Last frame took " + str(gamestate.processingtime*1000) + "ms to process.")

        #What menu are we in?
        if gamestate.menu_state == melee.enums.Menu.IN_GAME:
            print(gamestate.tolist())
            if args.framerecord:
                framedata.recordframe(gamestate)
            #XXX: This is where your AI does all of its stuff!
            #This line will get hit once per frame, so here is where you read
            #   in the gamestate and decide what buttons to push on the controller
            if args.framerecord:
                melee.techskill.upsmashes(ai_state=gamestate.ai_state, controller=controller)
            else:
                melee.techskill.multishine(ai_state=gamestate.ai_state, controller=controller)


        #If we're at the character select screen, choose our character
        elif gamestate.menu_state == melee.enums.Menu.CHARACTER_SELECT:
            print(gamestate.tolist())
            if (gamestate.player[1].controller_status != melee.enums.ControllerStatus.CONTROLLER_CPU
                and pickedCPU == 0):
                myMenuHelper.changecontrollerstatus(controller, gamestate, 1, 
                    melee.enums.ControllerStatus.CONTROLLER_CPU, character=None)
            else:
                pickedCPU = 1
                melee.menuhelper.choosecharacter(character=melee.enums.Character.KIRBY,
                    gamestate=gamestate, controller=controller, swag=False, start=True)
        #If we're at the postgame scores screen, spam START
        elif gamestate.menu_state == melee.enums.Menu.POSTGAME_SCORES:
            melee.menuhelper.skippostgame(controller=controller)
        #If we're at the stage select screen, choose a stage
        elif gamestate.menu_state == melee.enums.Menu.STAGE_SELECT:
            melee.menuhelper.choosestage(stage=melee.enums.Stage.FINAL_DESTINATION,
                gamestate=gamestate, controller=controller)
        #Flush any button presses queued up
        controller.flush()
        if log:
            log.logframe(gamestate)
            log.writeframe()

if __name__ == '__main__':
    main()
