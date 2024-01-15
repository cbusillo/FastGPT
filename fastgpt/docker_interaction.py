import docker
from docker.errors import ContainerError
from docker.models.containers import Container

from config import DOCKER_HOST


class DockerManager:
    def __init__(self) -> None:
        self.client = docker.DockerClient(base_url=DOCKER_HOST)

    def run_code_in_container(
        self, code: str, image: str = "python:3.11"
    ) -> str | None:
        try:
            container = self.client.containers.run(
                image, command=["python", "-c", code], remove=True, detach=True
            )
            return self._get_container_output(container)
        except ContainerError as e:
            print(f"Container execution error: {e.stderr.decode('utf-8')}")
            return None
        except Exception as e:
            print(f"Error running container: {e}")
            return None

    @staticmethod
    def _get_container_output(container: Container) -> str:
        output = container.logs(stream=True)
        container_output = ""
        for line in output:
            container_output += line.decode("utf-8")
        return container_output
