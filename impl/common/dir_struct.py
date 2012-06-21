import os, fnmatch, cksum

class Script:
    def __init__(self, path, name, num, checksum):
        self.path = path
        self.name = name
        self.num = num
        self.checksum = checksum

    def getPath(self):
        return self.path

    def getName(self):
        return self.name

    def getPatchNumber(self):
        return self.num

    def getChecksum(self):
        return self.checksum


def all_patch_scripts_sorted_asc(baseDir):
    return sorted(all_patch_scripts(baseDir), key=lambda script: script.num)


def all_rollback_scripts_sorted_desc(baseDir):
    return sorted(all_rollback_scripts(baseDir), key=lambda script: script.num, reverse=True)


def all_patch_scripts(baseDir):
    return all_scripts_from(baseDir, 'patch', naturalOrdering)


def all_rollback_scripts(baseDir):
    return all_scripts_from(baseDir, 'rollback', reverseOrdering)


def naturalOrdering(lines):
    return lines


def reverseOrdering(lines):
    return reversed(lines)


def all_scripts_from(baseDir, subDir, order):
    patches = []
    for dirname, dirnames, filenames in os.walk(baseDir):
        for filename in filenames:
            if fnmatch.fnmatch(dirname, '**/patches/**'):
                if fnmatch.fnmatch(filename, 'install.txt'):
                    for line in order(open(os.path.join(dirname, filename), 'r').readlines()):
                        script = createScriptRepresentationFrom(dirname, subDir, line)
                        if script is not None:
                            patches.append(script)

    return patches


def createScriptRepresentationFrom(dirname, subDir, fileName):
    dir_path = os.path.join(dirname, subDir)
    full_path = os.path.join(dir_path, fileName.rstrip('\n'))
    if not os.path.isdir(full_path):
        checksum = cksum.memcrc(open(full_path, 'rb').read())
        return Script(dir_path, fileName.rstrip('\n'), int(extract_patch_number(full_path, subDir)), checksum)


def extract_patch_number(script, subDir):
    return script[script.find("/patches/") + 9:script.find("/" + subDir + "/")]
