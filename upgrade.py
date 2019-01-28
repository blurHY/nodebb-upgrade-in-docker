from json import load, loads
from subprocess import run, PIPE, Popen


def loadConfig(container):
    config = open(f"/var/lib/docker/containers/{container}/config.v2.json")
    return load(config)


def runCmd(*cmd):
    return run(cmd, stdout=PIPE).stdout.decode("utf-8")


def runFollow(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line


container = "dd7eba130a8c7186f501a3d900662954cf1941fd49ff6d62594bdd8fe91f1b30"
configobj = loadConfig(container)
print("Modify args for upgrading")
configobj["Args"][2] = "./nodebb upgrade"
print("Restart docker:")
out = runCmd("service", "docker", "restart")
print(out)
out = runCmd("docker", "inspect", container)
print("Run with ", loads(out)[0]["Args"])
for line in runFollow(f"docker logs --tail 100 -f {container}"):
    print(line)