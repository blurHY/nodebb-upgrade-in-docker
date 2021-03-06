from json import load, loads, dump
from subprocess import run, PIPE, Popen


def loadConfig(container):
    return load(
        open(f"/var/lib/docker/containers/{container}/config.v2.json", "r"))


def writeConfig(container, obj):
    print("Write config")
    return dump(
        obj, open(f"/var/lib/docker/containers/{container}/config.v2.json",
                  "w"))


def runCmd(*cmd):
    return run(cmd, stdout=PIPE).stdout.decode("utf-8")


def runFollow(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip().decode("utf-8")
        if line == '' and process.poll() is not None:
            break
        if "Upgrade Complete!" in line:
            break
        if line:
            yield line.strip()


def restartDocker():
    print("Restart docker:")
    out = runCmd("service", "docker", "restart")
    print(out)


def startOrStopContainer(container, start):
    print(runCmd("docker", "start" if start else "stop", container))


container = "dd7eba130a8c7186f501a3d900662954cf1941fd49ff6d62594bdd8fe91f1b30"
configobj = loadConfig(container)

print("Modify args for upgrading")
startOrStopContainer(container, False)
configobj["Args"][0] = "-c"
configobj["Args"][1] = "./nodebb upgrade"
writeConfig(container, configobj)

restartDocker()

out = runCmd("docker", "inspect", container)
print("Run with ", loads(out)[0]["Args"])

startOrStopContainer(container, True)
for line in runFollow(f"docker logs --tail 100 -f {container}"):
    print(line)

startOrStopContainer(container, False)
configobj = loadConfig(container)
configobj["Args"][1] = "./nodebb start"
writeConfig(container, configobj)

restartDocker()
startOrStopContainer(container, True)
