# docker_interaction.py
import docker
from docker.models.containers import Container

from config import DOCKER_HOST
from .logging_config import setup_logging

logger = setup_logging(__name__)


class DockerManager:
    def __init__(self, image: str = "python:3.11") -> None:
        self.client = docker.DockerClient(base_url=DOCKER_HOST)
        self.image = image
        self.container: Container | None = None

    def start_container(self) -> None:
        self.container = self.client.containers.run(
            image=self.image, detach=True, tty=True, stdin_open=True
        )
        self.create_app_directory()

    def remove_container(self) -> None:
        self.container.stop()
        self.container.remove(force=True)
        self.container = None

    def create_app_directory(self) -> None:
        self.container.exec_run(cmd="mkdir -p /app")

    def execute_python(self, code: str) -> str:
        exit_code, output = self.container.exec_run(
            cmd=["python", "-c", code], workdir="/app"
        )
        return output.decode("utf-8")

    def execute_bash(self, code: str) -> str | None:
        exit_code, output = self.container.exec_run(cmd=[code], workdir="/app")
        return output.decode("utf-8") if exit_code == 0 else None

    def execute_pip_install(self, packages: [str]) -> str:
        outputs = []
        for package in packages:
            exit_code, output = self.container.exec_run(
                cmd=["pip", "install", package, "-v"], workdir="/app"
            )
            output = output.decode("utf-8")  # Decoding from bytes to string
            if exit_code != 0:
                logger.error(f"Failed to install package {package}.")
            else:
                logger.info(f"Successfully installed package {package}.")
            outputs.append(output)
        return "\n".join(outputs)
