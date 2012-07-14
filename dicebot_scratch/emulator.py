from game import DictWorld, play

def interpret(world, commands):
    instance = DictWorld.load_string(world)
    for cmd in commands:
        instance.execute_command(cmd)
        instance.update()
        if instance.aborted or instance.dead or instance.lifted:
            break
    return instance.ending()