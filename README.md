# LLM-Evaluation

## Testing with Graalvm and Graalpy

### Setting up the Graalvm and Graalpy

This is is a slightly complicated procedure and easy to get wrong (especially in the graalpy) so try to follow it step by step.

#### Graalvm

The first step is to install graalvm. This can be downloaded from here https://www.graalvm.org/downloads/# based on your platform and jdk version required. We used jdk 23.

Once this is done, you can follow the steps here https://www.graalvm.org/latest/getting-started/ and finish the install steps (extracting, exporting to path etc.)

### Graalpy

In order to call java code from python, it will require graalpy to be installed ontop of graalvm. You can download it from here https://github.com/oracle/graalpython/releases based on your platform and architecture. Two key notes

- you will need to download one that has the `-jvm` in the name in order to be compatible with the graalvm
- you will need to make sure that the release version is compatible with the graalvm you have. you can do this by searching for that specific version in release.

for reference, this is what Ibrahim has downloaded (he's running on an M1 Mac)

![alt text](image.png)

Once you have installed it, you can follow the steps here https://www.graalvm.org/latest/reference-manual/python/Python-Runtime/, specifically the alternative steps because you will be downloading it from Github releases.
For the export path, you can use the following command `export PATH=~/graalpy-24.1.1-macos-aarch64/bin:$PATH` and change it to match whichever graalpy you have installed and wherever you have kept the extracted file.

Once this is done, you can activate the virtual environment with the following command, `source graal-venv/bin/activate`

And to test that it works, you run `graalpy TestGraal.py` and it should work on a small code.

The rest TBD