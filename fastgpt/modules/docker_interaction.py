# docker_interaction.py
import base64
import logging
from datetime import datetime
from time import sleep

import docker
from docker.models.containers import Container

from modules.config import config

logger = logging.getLogger(__name__)


class DockerManager:
    def __init__(self, image: str = "python:3.11") -> None:
        self.client = docker.DockerClient(base_url=config["DOCKER_URL"])
        self.image = image
        self.container: Container | None = None

    def start_container(self) -> None:
        logger.info("Starting docker container.")
        self.container = self.client.containers.run(
            image=self.image, detach=True, tty=True, stdin_open=True
        )
        self._create_app_directory()

    def remove_container(self) -> None:
        self._wait_for_container()

        self.container.stop()
        self.container.remove(force=True)
        self.container = None

    def _create_app_directory(self) -> None:
        self.container.exec_run(cmd="mkdir -p /app")

    def execute_bash(self, command: str) -> tuple[int, str]:
        self._wait_for_container()

        encoded_command = base64.b64encode(command.encode()).decode()
        command_str = f"echo {encoded_command} | base64 --decode | /bin/bash"

        exit_code, output = self.container.exec_run(
            cmd=["/bin/bash", "-c", command_str], workdir="/app"
        )
        return exit_code, output.decode("utf-8")

    def save_python_script(self, code: str) -> str:
        filename = f"script_{datetime.now().strftime('%Y%m%d%H%M%S')}.py"
        filepath = f"/app/{filename}"

        command = f"cat <<EOF > {filepath}\n{code}\nEOF"
        self.execute_bash(command)

        return filepath

    def execute_python_string(self, code: str) -> str:
        python_script_path = self.save_python_script(code)
        return self.execute_python_script(python_script_path)

    def execute_python_script(self, file_path: str) -> str:
        exit_code, output = self.execute_bash(f"python {file_path}")
        if exit_code != 0:
            return f"Error executing Python script: {output}"
        return output

    def execute_pip_install(self, packages: set[str]) -> str:
        outputs = []
        for package in packages:
            install_command = f"pip install {package} -v"
            exit_code, output = self.execute_bash(install_command)
            if exit_code != 0:
                message = "Failed to install package"
            else:
                message = "Successfully installed package"
            outputs.append(f"{message} {package}.")
        return "\n".join(outputs)

    def _wait_for_container(self) -> None:
        retries = 20
        while retries > 0:
            if self.container:
                return
            retries -= 1
            sleep(1)
        logger.warning("Failed to start container.")
