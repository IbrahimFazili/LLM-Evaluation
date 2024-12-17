import subprocess
import os

if __name__ == "__main__":
    if not os.path.exists('experiments'):
        os.makedirs('experiments')
        os.makedirs('experiments/0_0')
        os.makedirs('experiments/0_1')
        os.makedirs('experiments/0_2')
        os.makedirs('experiments/0_3')
        os.makedirs('experiments/0_4')
        os.makedirs('experiments/0_5')
        os.makedirs('experiments/0_6')
        os.makedirs('experiments/0_7')
        os.makedirs('experiments/0_8')
        os.makedirs('experiments/0_9')
    rc = subprocess.call("translation/bash_scripts/temperature_tests.sh")