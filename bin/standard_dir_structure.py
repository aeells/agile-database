import os, fnmatch

def extract_patch_number(patch):
    return patch[patch.find("/patches/") + 9:patch.find("/patch/")]


def find_all_patch_scripts(scriptsBaseDir):
    patches = []
    for dirname, dirnames, filenames in os.walk(scriptsBaseDir):
        for filename in filenames:
            if fnmatch.fnmatch(dirname, '**/patches/**'):
                if fnmatch.fnmatch(filename, 'install.txt'):
                    with open(os.path.join(dirname, filename), 'r') as f:
                        for line in f:
                            patches.append(os.path.join(dirname, 'patch', line.rstrip('\n')))

    return patches
