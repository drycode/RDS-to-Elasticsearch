import os
from dotenv import load_dotenv
import subprocess
from types import SimpleNamespace


BASH_COMMAND = "which bash"

basedir = os.path.abspath(os.path.dirname(__file__))
res = load_dotenv(os.path.join(basedir, "../dev.env"))

Config = SimpleNamespace(
    ELASTICSEARCH_URL=os.environ.get("ELASTICSEARCH_URL"),
    RDS_USERNAME=os.environ.get("RDS_USERNAME"),
    RDS_PASSWORD=os.environ.get("RDS_PASSWORD"),
    JDBC_DRIVER_LIBRARY=os.environ.get("JDBC_DRIVER_LIBRARY"),
    JDBC_CONNECTION_STRING=os.environ.get("JDBC_CONNECTION_STRING"),
    SQL_DB_NAME=os.environ.get("SQL_DB_NAME"),
    JDBC_DRIVER_CLASS=os.environ.get("JDBC_DRIVER_CLASS"),
    SQL_SCRIPT=os.environ.get("SQL_SCRIPT"),
    AWS_SECRET_KEY=os.environ.get("AWS_SECRET_KEY"),
    AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID"),
    INDEX_TARGET=os.environ.get("INDEX_TARGET"),
    CPU_AVAILABLE=os.cpu_count(),
)


if __name__ == "__main__":
    process = subprocess.Popen(BASH_COMMAND.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    with open(os.path.join(basedir, "../dev_env.sh"), "w") as f:
        f.write(f'#!{output.decode("utf-8").strip()}\n')
        for name, value in vars(Config).items():
            # Escape symbols commonly used by Bash.
            if isinstance(value, str):
                value = (
                    value.replace('"', '\\"').replace("$", "\\$").replace("`", "\\`")
                )
            f.write(f'export {name}="{value}"\n')
