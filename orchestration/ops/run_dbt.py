from dagster import op
import subprocess

@op
def run_dbt(start):
    subprocess.run(["dbt", "run"], cwd="dbt_project", check=True)
