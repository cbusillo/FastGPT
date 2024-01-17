# docker_interaction.py
from time import sleep

import docker
from docker.models.containers import Container

from config import DOCKER_URL
from .logging_config import setup_logging

logger = setup_logging(__name__)


class DockerManager:
    def __init__(self, image: str = "python:3.11") -> None:
        self.client = docker.DockerClient(base_url=DOCKER_URL)
        self.image = image
        self.container: Container | None = None

    def start_container(self) -> None:
        logger.info("Starting docker container.")
        self.container = self.client.containers.run(
            image=self.image, detach=True, tty=True, stdin_open=True
        )
        self.create_app_directory()

    def remove_container(self) -> None:
        self.wait_for_container()

        self.container.stop()
        self.container.remove(force=True)
        self.container = None

    def create_app_directory(self) -> None:
        self.container.exec_run(cmd="mkdir -p /app")

    def execute_python(self, code: str) -> str:
        self.wait_for_container()
        exit_code, output = self.container.exec_run(
            cmd=["python", "-c", code], workdir="/app"
        )
        return output.decode("utf-8")

    def execute_bash(self, commands: list[str] | str) -> str | None:
        if isinstance(commands, str):
            commands = [commands]
        self.wait_for_container()
        exit_code, output = self.container.exec_run(cmd=commands, workdir="/app")
        return output.decode("utf-8") if exit_code == 0 else None

    def execute_pip_install(self, packages: [str]) -> str:
        self.wait_for_container()
        outputs = []
        for package in packages:
            exit_code, output = self.container.exec_run(
                cmd=["pip", "install", package, "-v"], workdir="/app"
            )
            if exit_code != 0:
                message = "Failed to install package"
            else:
                message = "Successfully installed package"
            outputs.append(f"{message} {package}")
        return "\n\n".join(outputs)

    def wait_for_container(self) -> None:
        retries = 20
        while retries > 0:
            if self.container:
                return
            retries -= 1
            sleep(1)
        logger.warning("Failed to start container.")
