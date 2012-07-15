import dual_world
import dict_world
import world 

def interpret_impl(world_string, commands, instance):
    if commands == '':
        commands = 'A'
    for cmd in commands:
        instance, score = instance.apply_command(cmd)
        if score is not None:
            break
    if score is None:
        return instance.get_score_abort()
    else:
        return score

def interpret(world_string, commands):
    instance1 = dict_world.DictWorld.from_string(world_string)
    instance2 = world.World.from_string(world_string)
    instance_dual = dual_world.DualWorld(instance1, instance2)
    return interpret_impl(world_string, commands, instance_dual)

def interpret_dict(world_string, commands):
    return interpret_impl(world_string, commands,
                          dict_world.DictWorld.from_string(world_string))

def interpret_main(world_string, commands):
    return interpret_impl(world_string, commands,
                      world.World.from_string(world_string))