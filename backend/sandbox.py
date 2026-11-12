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
        # Оборачиваем вызов в системный time -v.
        # Важно: stdout пишется в output.txt, а stderr (где живет time)
        # смешивается с выводом exec_run, так что мы заберем его в python-коде.
        command = f"sh -c 'timeout 5s /usr/bin/time -v python3 {guest_dir}/main.py < {guest_dir}/input.txt > {guest_dir}/output.txt'"

        result = container.exec_run(command)

        # Читаем настоящий output программы из файла, который записался в volume
        output_file_path = os.path.join(host_dir, "output.txt")
        program_output = ""
        if os.path.exists(output_file_path):
            with open(output_file_path, "r", encoding="utf-8") as f:
                program_output = f.read()

        # Возвращаем код выхода, чистый вывод программы и сырой текст time из stderr
        return result.exit_code, program_output, result.output.decode("utf-8")


    finally:
        shutil.rmtree(host_dir, ignore_errors=True)

