import argparse, os, re, subprocess

# Create Parser
parser = argparse.ArgumentParser(description='Unzip and categorize files for me')
parser.add_argument('-T', '--targetDir', metavar='TargetDir', default='.', type=str, nargs=1,
                   help='Target Directory')
parser.add_argument('-U', '--unzip', action='store_true', default=False,
                   help='Unzip flag')
parser.add_argument('-S', '--verbose', action='store_true', default=True,
                   help='Show Unzip result flag')

# Create regular expression finder.
grouper = re.compile(r".*?(\[.+?\])", re.I)

# Get file names.
args          = parser.parse_args()
targetDir     = args.targetDir[0]
isUnzip       = args.unzip
isShowResult  = args.verbose

#files = [d.encode('utf8') for d in os.listdir(targetDir)]
fileList = os.listdir(targetDir)

dirList = []
groupUndefined = "UNDEFINED"

for fileName in fileList:
  srcFilepath = os.path.join(targetDir, fileName)
  if os.path.isfile(srcFilepath):
    groupName = groupUndefined
    result = grouper.match(fileName)
    if result:
      groupName = result.group(1)
      # Test output.
      # print(groupName.encode('utf8'))
    if groupName not in dirList:
      dirList.append(groupName)
      targetDirPath = os.path.join(targetDir, groupName)
      # Create dir in folder, if its not exist.
      if (not os.path.exists(targetDirPath)):
        os.mkdir(targetDirPath)
    dstFilePath = os.path.join(targetDir, groupName, fileName)

    # Move zip file to target directory.
    os.rename(srcFilepath, dstFilePath)

    if (isUnzip): #Call 7z to unzip target to a sub directory.
      zipResult = subprocess.Popen([
          '7z', 'x', '-bd',
          dstFilePath, 
          '-o'+os.path.splitext(dstFilePath)[0]],

          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT,
          universal_newlines=True
          )
      # ------ Show unzip result --------
      if isShowResult:
        zipResult.communicate()
        fName = os.path.splitext(fileName)[0]
        if 0 == zipResult.returncode:
          print(('File : ' + fName + ' unzip success.').encode('utf8'))
        else:
          print(('File : ' + fName + ' unzip fail.').encode('utf8'))
      # ------ Show unzip result --------
  
    