import os
import sys

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)

def module_install():
    try:
        # Check if requirements.txt exists
        requirements_file = os.path.join(root, 'requirements.txt')
        wheelhouse = os.path.join(root , 'wheelhouse')
        if not os.path.exists(requirements_file) or not os.path.exists(wheelhouse):
            raise FileNotFoundError(
            f"""Could not find requirements.txt or wheelhouse in the current directory: {root}
            \nMake sure that your *wheelhouse* and requirements.txt are in the same directory as the setup.py file.
            """)

        with open(os.path.join(root, 'requirements.txt')) as file:
            for module_name in file:
                module_name = module_name.strip()  # Remove leading/trailing whitespaces
                print(f"Installing {module_name}...")
                try:
                    powershell_command = f'python -m pip install {module_name} --no-index --find-links wheelhouse'
                    os.system(f'powershell -Command "{powershell_command}"')
                    module_installed.append(i)
                except Exception as e:
                    pass

    except Exception as e:
        print(f"Error: {e}")

module_install()
