import docker, os
client = docker.from_env()


def run_database():
    # os.system('ls -t1')
    cmd = """docker run - e "ACCEPT_EULA=Y" - e "SA_PASSWORD=Vaneck123!" - p 1433: 1433 - d  mcr.microsoft.com/mssql/server:2017 - latest"""
    print(cmd)
    os.system(cmd)
    print('database running')
    return True


def pull_images(image_name):
    client.images.pull(image_name)
    return True


def get_images():
    import docker
    client = docker.from_env()
    imgs = client.images.list()
    # print(imgs)
    l = []
    for i in imgs:
        l.append(i)
        # print(i)
    # for image in client.images.list():
    #     print(image.id)
    #     l.append(image.id)
    return l


def start_container(docker_image, port):

    client.containers.run(
        docker_image,
        detach=True,
        ports={
            '{}/tcp'.format(port): port
        }
    )
    return True


def restart_container(container_id):
    client.containers.get(container_id).restart()
    return True


# print(run_database())
print(get_images())
# print(pull_images('ubuntu'))
# print(start_container())
# print(restart_container())
