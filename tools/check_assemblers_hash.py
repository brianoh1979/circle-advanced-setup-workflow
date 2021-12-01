import os

import hashlib

from pathlib import Path

 

RUN_TIME_WORKING_DIR = "module-a"

RUN_TIME_DIFF_DIR = "run_time_diff_dir"

 

 

def main():

    REPO_PATH = Path(__file__).resolve().parents[1]

 

    all_assemblers = os.listdir(REPO_PATH / "assemblers")

    print(f"all_assemblers: {all_assemblers}")

 

    current_branch = os.environ["CIRCLE_BRANCH"]  # get current branch from CircleCI

    os.system(f"mkdir {RUN_TIME_DIFF_DIR}")

 

    for assembler in all_assemblers:

 

        # generate hash for current branch

        os.system(f"rm -r {Path(RUN_TIME_WORKING_DIR)}") # clean up

        os.system(f"git checkout {current_branch}")

        os.system(f"python pmpx.py local-assemble {assembler} {RUN_TIME_WORKING_DIR}")

        current_branch_env_var = f"{current_branch}_" + assembler

        hash_dir(

            env_var=current_branch_env_var,

            directory=Path(RUN_TIME_WORKING_DIR) / assembler,

        )

        print(current_branch_env_var, os.environ[current_branch_env_var])

 

        # generate hash for master branch

        os.system(f"rm -r {Path(RUN_TIME_WORKING_DIR) / assembler}") # clean up

        os.system(f"git checkout createfile")

        os.system(f"python pmpx.py local-assemble {assembler} {RUN_TIME_WORKING_DIR}")

        master_env_var = "createfile_" + assembler

        hash_dir(

            env_var=master_env_var, directory=Path(RUN_TIME_WORKING_DIR) / assembler

        )

        print(master_env_var, os.environ[master_env_var])

        os.system(f"rm -r {Path(RUN_TIME_WORKING_DIR) / assembler}")

        os.system(f"git checkout {current_branch}")

 

        # store as env var

        if os.environ[master_env_var] != os.environ[current_branch_env_var]:

            diff_assembler = f"diff_{assembler}"

            os.environ[diff_assembler] = diff_assembler

            print(os.environ[diff_assembler])

 

    # write to file if diff exists

    for assembler in all_assemblers:

        diff_assembler = f"diff_{assembler}"

        if diff_assembler in os.environ:

            with open(f"assemblers/{assembler}/{diff_assembler}.txt", "w") as writer:

                writer.write(diff_assembler)

 

        os.system(f"ls assemblers/{assembler}")

 

 

def hash_dir(env_var, directory):

    print(directory)

    all_py_files = [x for x in directory.glob(f"**/*.py")]

    all_yml_files = [x for x in directory.glob(f"**/*.yml")]

 

    all_py_and_yaml_files = all_py_files + all_yml_files

 

    hash_obj = hashlib.md5()

    for file in all_py_and_yaml_files:

        hash_obj.update(open(file, "rb").read())

    checksum = hash_obj.digest()

    os.environ[env_var] = str(checksum)

 

 

if __name__ == "__main__":

    main()
