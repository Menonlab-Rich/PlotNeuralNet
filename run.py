import argparse
import os
import importlib


def normalize_project_name(project_name):
    '''
    Normalize a project name to a valid Python module name.
    Replace hyphens with underscores and replace directory separators with dots.
    '''
    name = project_name.replace('-', '_').replace(os.sep, '.')
    if name.startswith('projects'):
        name = name[9:]

    # trim leading dots
    while name.startswith('.'):
        name = name[1:]

    # remove file extension if present
    if name.endswith('.py'):
        name = name[:-3]

    # remove trailing dots
    while name.endswith('.'):
        name = name[:-1]

    return name


def main():
    cwd = os.getcwd()
    parser = argparse.ArgumentParser(
        description='Run a specific project file.')
    parser.add_argument('project', type=str,
                        help='The name of the project to run.')
    args = parser.parse_args()

    project_name = normalize_project_name(args.project)
    module_name = f'projects.{project_name}'

    try:
        project_module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"Module '{module_name}' not found.")
        return

    
    project_dir = os.path.dirname(
        project_module.__file__)
    program = project_module.main
    os.chdir(project_dir)
    program()
    # run pdflatex
    os.system(f"pdflatex {os.getcwd() + os.sep}run.tex")
    os.chdir(cwd) # restore the original working directory


if __name__ == '__main__':
    main()
