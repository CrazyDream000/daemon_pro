import os
import uuid
from random import randrange
from configparser import ConfigParser


class RipConf:
    @staticmethod
    def load_app_conf(props_conf: ConfigParser, conf_file_name: str):

        print("---------------- result:" + str(conf_file_name))
        print("---------------- result:" + str(os.path.isfile(conf_file_name)))
        if not os.path.isfile(conf_file_name):
            # init new config file
            print("creating... " + conf_file_name)
            props_conf['keys'] = {
                'dns_key': "aaaa-bbbb-eeee-ffff-rrrr-qqqq",
                'api_key_number': '1',
                'api_user': 'test',
                'requested_domain': 'testdomain2',
                'management_key': 'replace_with_takamaka_key_for_management'
            }
            props_conf['app'] = {
                'bind_address': 'localhost',
                'bind_port': '13131',
                'debug': False
            }
            props_conf['app_debug'] = {
                'bind_address': '0.0.0.0',
                'bind_port': '13131'
            }
            props_conf['ddns_server'] = {
                'delivery_url': "https://supportlink.takamaka.org:6000/ddns/",
                'ip_retrieval_url': 'https://supportlink.ch/myip.php',
                'uuid': uuid.uuid4(),
                'nickname': RipConf.prepare_nickname()
            }
            with open(conf_file_name, 'w') as configfile:
                props_conf.write(configfile)
        else:
            # load from config file
            print("loading... " + conf_file_name)
            props_conf.read(conf_file_name)

    @staticmethod
    def prepare_nickname():
        animals = [
            "frog", "frogspawn", "newt", "tadpole", "toad", "harvestman", "scorpion", "spider", "tarantula",
            "albatross", "biddy", "blackbird", "canary", "crow", "cuckoo", "dove", "pigeon", "duck", "eagle", "falcon",
            "finch", "flamingo", "goose", "gull", "hawk", "jackdaw", "jay", "kestrel", "kookaburra", "mallard",
            "nightingale", "nuthatch", "ostrich", "owl", "parakeet", "parrot", "peacock", "pelican", "penguin",
            "pheasant", "piranha", "raven", "robin", "rooster", "sparrow", "stork", "swallow", "swan", "swift", "tit",
            "turkey", "vulture", "woodpecker", "wren", "peacock", "butterfly", "red", "admiral", "silkworm",
            "swallowtail", "barbel", "carp", "cod", "crab", "eel", "goldfish", "haddock", "halibut", "jellyfish",
            "lobster", "perch", "pike", "plaice", "ray", "salmon", "sawfish", "scallop", "shark", "shell", "shrimp",
            "trout", "ant", "aphid", "bee", "beetle", "bumblebee", "caterpillar", "cockroach", "dragonfly", "flea",
            "fly", "gadfly", "grasshopper", "harvestman", "ladybug", "larva", "louse", "maggot", "midge", "moth",
            "nymph", "wasp", "anteater", "antelope", "armadillo", "badger", "bat", "bear", "beaver", "bullock", "camel",
            "chimpanzee", "dachshund", "deer", "hart", "dolphin", "elephant", "elk", "moose", "fox", "gazelle",
            "gerbil", "giraffe", "goat", "grizzly", "bear", "guinea", "pig", "hamster", "hare", "hare", "hedgehog",
            "horse", "hyena", "lion", "llama", "lynx", "mammoth", "marmot", "mink", "mole", "mongoose", "mouse", "mule",
            "otter", "panda", "pig", "hog", "platypus", "polar", "bear", "polecat", "pony", "porcupine", "prairie",
            "dog", "puma", "racoon", "rat", "reindeer", "rhinoceros", "seal", "seal", "sheep", "skunk", "sloth",
            "squirrel", "tiger", "weasel", "whale", "wolf", "zebra", "slug", "snail", "blindworm", "boa", "chameleon",
            "constrictor", "snake", "copperhead", "coral", "snake", "cottonmouth", "crocodile", "diamondback",
            "rattlesnake", "gecko", "iguana", "lizard", "rattlesnake", "poisonous", "venomous", "snake", "python",
            "salamander", "saurian", "sea", "snake", "sidewinder", "snake", "rattlesnake", "tortoise", "turtle",
            "tapeworm", "leech", "earthworm", "round", "worm", "millipede"]
        random_suffix = randrange(1, 100)
        random_index_animal = randrange(0, len(animals))
        return animals[random_index_animal] + "_" + str(random_suffix)
