import docker
import os
import shutil

client = docker.from_env()

def run_test_in_docker(submission_id: int, data: str, input_code: str):

    host_dir = f"./shared_sandbox/sub_{submission_id}"
    guest_dir = f"/sandbox_env/sub_{submission_id}"

    try:
        container = client.containers.get("algo_sandbox_container")

        file_path = os.path.join(host_dir, "main.py")
        os.makedirs(host_dir, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(input_code)
        if data != None:
            file_path = os.path.join(host_dir, "input.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(data)

        # Команда на таймер решения, сейчас стоит 5 секунд
        result = container.exec_run(f"sh -c 'timeout 5s python {guest_dir}/main.py < {guest_dir}/input.txt'")

        return result

    finally:
        shutil.rmtree(host_dir, ignore_errors=True)

