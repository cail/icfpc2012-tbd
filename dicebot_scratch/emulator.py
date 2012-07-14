import dual_world
import dict_world
import world 

def interpret(world_string, commands):
    instance1 = dict_world.DictWorld.from_string(world_string)
    instance2 = world.World.from_string(world_string)
    instance_dual = dual_world.DualWorld(instance1, instance2)
    for cmd in commands:
        instance_dual, score = instance_dual.apply_command(cmd)
        if score is not None:
            break
    return score

def interpret_dict(world_string, commands):
    instance = dict_world.DictWorld.from_string(world_string)
    for cmd in commands:
        instance, score = instance.apply_command(cmd)
        if score is not None:
            break
    return score

def interpret_main(world_string, commands):
    instance = world.World.from_string(world_string)
    for cmd in commands:
        instance, score = instance.apply_command(cmd)
        if score is not None:
            break
    return score