from json import load

container = "dd7eba130a8c7186f501a3d900662954cf1941fd49ff6d62594bdd8fe91f1b30"
config = open(f"/var/lib/docker/containers/{container}/config.v2.json")
configobj = load(config)
print(configobj)