#!/usr/bin/env python
#============================================================================
# Copyright (c) Microsoft Corporation. All rights reserved. See license.txt for license information.
#============================================================================

from __future__ import print_function
from __future__ import with_statement
from contextlib import contextmanager

import os
import sys
import pwd
import shutil
import grp
import codecs


try:
    import hashlib
    md5const = hashlib.md5
except ImportError:
    import md5
    md5const = md5.md5

BLOCK_SIZE = 8192

def Set_Marshall(DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode):
    DestinationPath = DestinationPath.decode("utf-8")
    SourcePath = SourcePath.decode("utf-8")
    Ensure = Ensure.decode("utf-8")
    Type = Type.decode("utf-8")
    Force = Force.decode("utf-8")
    Checksum = Checksum.decode("utf-8")
    Recurse = Recurse.decode("utf-8")
    Links = Links.decode("utf-8")
    Owner = Owner.decode("utf-8")
    Group = Group.decode("utf-8")
    Mode = Mode.decode("utf-8")
    
    retval = Set(DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode)
    return retval

def Test_Marshall(DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode):
    DestinationPath = DestinationPath.decode("utf-8")
    SourcePath = SourcePath.decode("utf-8")
    Ensure = Ensure.decode("utf-8")
    Type = Type.decode("utf-8")
    Force = Force.decode("utf-8")
    Checksum = Checksum.decode("utf-8")
    Recurse = Recurse.decode("utf-8")
    Links = Links.decode("utf-8")
    Owner = Owner.decode("utf-8")
    Group = Group.decode("utf-8")
    Mode = Mode.decode("utf-8")
    
    retval = Test(DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode)
    return retval

def Get_Marshall(DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode):
    DestinationPath = DestinationPath.decode("utf-8")
    SourcePath = SourcePath.decode("utf-8")
    Ensure = Ensure.decode("utf-8")
    Type = Type.decode("utf-8")
    Force = Force.decode("utf-8")
    Checksum = Checksum.decode("utf-8")
    Recurse = Recurse.decode("utf-8")
    Links = Links.decode("utf-8")
    Owner = Owner.decode("utf-8")
    Group = Group.decode("utf-8")
    Mode = Mode.decode("utf-8")

    retval = 0
    (retval, DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode, ModifiedDate) = Get(DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode)

    DestinationPath = DestinationPath.encode("utf-8")
    SourcePath = SourcePath.encode("utf-8")
    Ensure = Ensure.encode("utf-8")
    Type = Type.encode("utf-8")
    Force = Force.encode("utf-8")
    Contents = Contents.encode("utf-8")
    Checksum = Checksum.encode("utf-8")
    Recurse = Recurse.encode("utf-8")
    Links = Links.encode("utf-8")
    Owner = Owner.encode("utf-8")
    Group = Group.encode("utf-8")
    Mode = Mode.encode("utf-8")
    ModifiedDate = ModifiedDate.encode("utf-8")

    return [retval, DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode, ModifiedDate]


############################################################
### Begin user defined DSC functions
############################################################

@contextmanager
def opened_w_error(filename, mode="r"):
    """
    This context ensures the file is closed.
    """
    try:
        f = codecs.open(filename, encoding='utf-8' , mode=mode)
    except IOError, err:
        yield None, err
    else:
        try:
            yield f, None
        finally:
            f.close()

def ReadFile(path):
    """
    Safely attempt to read a file,
    ensuring file is always closed at exit.
    Return the data and the exception object.
    The data is None if an error occurred.
    The error is None if the data was read.
    Log results to stderr.
    """
    d=None
    error=None
    with opened_w_error(path,'rb') as (F,error):
        if error:
            print("Exception opening file " + path + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr )
        else:
            d=F.read()
    return d,error

def WriteFile(path,contents):
    """
    Safely attempt to write data to a file,
    replacing the existing file or creating it and
    ensuring file is always closed at exit.
    Return the exception object.
    The error is None if the data was written.
    Log results to stderr.
    """
    error=None
    with opened_w_error(path,'wb+') as (F,error):
        if error:
            print("Exception opening file " + path + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
        else:
            F.write(contents)
    return error

def LStatFile(path):
    """
    LStat the file.  Do not follow the symlink.
    """
    d=None
    error=None
    try:
        d=os.lstat(path)
    except OSError, error:
         print("Exception lstating file " + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    except IOError, error:
         print("Exception lstating file " + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    return d

def StatFile(path):
    """
    Stat the file, following the symlink.
    """
    d=None
    error=None
    try:
        d=os.stat(path)
    except OSError, error:
         print("Exception stating file " + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    except IOError, error:
         print("Exception stating file " + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    return d

def Chown(path,owner,group):
    error=None
    try:
        os.chown(path,owner,group)
    except OSError, error:
         print("Exception changing ownership of file " + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    except IOError, error:
         print("Exception changing ownership of file " + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    return error

def Chmod(path,mode):
    error=None
    if type(mode) == str:
        mode=int(mode,8)
    try:
        os.chmod(path,mode)
    except OSError, error:
         print("Exception  changing mode of file " + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    except IOError, error:
         print("Exception  changing mode of file " + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    return error

def LChown(path,owner,group):
    error=None
    try:
        os.lchown(path,owner,group)
    except OSError, error:
         print("Exception changing ownership of file " + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    except IOError, error:
         print("Exception changing ownership of file " + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    return error

def LChmod(path,mode):
    error=None
    try:
        os.lchmod(path,mode)
    except OSError, error:
         print("Exception  changing mode of file " + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    except IOError, error:
         print("Exception  changing mode of file " + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    return error

def ListDir(path):
    d=None
    error=None
    try:
        d=os.listdir(path)
    except OSError, error:
         print("Exception listing dir" + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    except IOError, error:
         print("Exception listing dir" + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    return d

def Symlink(spath,dpath):
    error=None
    try:
        os.symlink(os.readlink(spath), dpath)
    except OSError, error:
        print("Exception creating symlink from " + spath  + ' to ' + dpath + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    except IOError, error:
        print("Exception creating symlink from " + spath  + ' to ' + dpath + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    return error
    
def MakeDirs(path):
    error=None
    try:
        os.makedirs(path)
    except OSError, error:
         print("Exception making dir" + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    except IOError, error:
         print("Exception making dir" + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    return error

def RemoveFile(path):
    error=None
    try:
        os.remove(path)
    except OSError, error:
         print("Exception removing file" + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    except IOError, error:
         print("Exception removing file" + path  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    return error

def CopyFile(spath,dpath):
    error=None
    try:
        shutil.copyfile(spath,dpath)
    except OSError, error:
         print("Exception removing tree" + spath  + ' to ' + dpath + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    except IOError, error:
         print("Exception removing tree" + spath  + ' to ' + dpath + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    return error

def CompareFiles(DestinationPath, SourcePath, Checksum):
    """
    Reading and computing the hash here is done in a block-by-block manner, 
    in case the file is quite large.
    """
    if Checksum == "md5":
        src_error = None
        dest_error = None
        src_hash = md5const()
        dest_hash = md5const()
        src_block ='loopme'
        dest_block ='loopme'
        with opened_w_error(SourcePath,'r') as (src_file,src_error):
            if src_error:
                print("Exception opening source file " + SourcePath  + " Error Code: " + str(src_error.errno) +
                      " Error: " + src_error.message + src_error.strerror,file=sys.stderr)
                return -1
            with opened_w_error(DestinationPath,'r') as (dest_file,dest_error):
                if dest_error:
                    print("Exception opening destination file " + DestinationPath + " Error Code: " + str(dest_error.errno) +
                          " Error: " + dest_error.message + dest_error.strerror,file=sys.stderr)
                    return -1
                while src_block != '' and dest_block != '':
                    src_block=src_file.read(BLOCK_SIZE)
                    dest_block=dest_file.read(BLOCK_SIZE)
                    src_hash.update(src_block)
                    dest_hash.update(dest_block)
                    if src_hash.hexdigest() != dest_hash.hexdigest():
                        return -1  
        if src_hash.hexdigest() == dest_hash.hexdigest():
            return 0  
    elif Checksum == "ctime":
        stat_dest = StatFile(DestinationPath)
        stat_src = StatFile(SourcePath)
        if stat_src.st_ctime > stat_dest.st_ctime:
            # Source is newer than Destination
            return -1
        else:
            return 0
    elif Checksum == "mtime":
        stat_dest = StatFile(DestinationPath)
        stat_src = StatFile(SourcePath)
        if stat_src.st_mtime > stat_dest.st_mtime:
            # Source is newer than Destination
            return -1
        else:
            return 0

def RemoveTree(path):
    error=None
    try:
        shutil.rmtree(path)
    except OSError, error:
        print("Exception removing folder " + path + " Error Code: "
              + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    except IOError, error:
        print("Exception removing folder " + path + " Error Code: "
              + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
    return error
    
def RemovePath(path):
    error=None
    if os.path.islink(path) or os.path.isfile(path):
        RemoveFile(path)
    elif os.path.isdir(path):
        RemoveTree(path)
    else:
        print("Error: Unknown file type for file: " + path,file=sys.stderr)
    return error
        
def TestOwnerGroupMode(DestinationPath, SourcePath, fc):
    stat_info = LStatFile(DestinationPath)

    if SourcePath:
        stat_info_src = LStatFile(SourcePath)

    if fc.Owner:
        try:
            Specified_Owner_ID = pwd.getpwnam(fc.Owner)[2]
        except KeyError, error:
             print("Exception obtaining gid from group name " + fc.Group  + " Error: " + error.message,file=sys.stderr)
             return False
        if Specified_Owner_ID != pwd.getpwuid(stat_info.st_uid)[2]:
            return False
    elif SourcePath:
        # Owner wasn't specified, if SourcePath is specified then check that the Owners match
        if pwd.getpwuid(stat_info.st_uid)[2] != pwd.getpwuid(stat_info_src.st_uid)[2]:
            return False

    if fc.Group:
        try:
            Specified_Group_ID = grp.getgrnam(fc.Group)[2]
        except KeyError, error:
             print("Exception obtaining gid from group name " + fc.Group  + " Error: " + error.message,file=sys.stderr)
             return False
        if Specified_Group_ID != grp.getgrgid(stat_info.st_gid)[2]:
            return False
    elif SourcePath:
        # Group wasn't specified, if SourcePath is specified then check that the Groups match
        if grp.getgrgid(stat_info.st_gid)[2] != grp.getgrgid(stat_info_src.st_gid)[2]:
            return False
    # Mode is irrelevant to symlinks
    if not os.path.islink(DestinationPath):
        if fc.Mode:
            if str(oct(stat_info.st_mode))[-3:] != fc.Mode:
                return False
        elif SourcePath:
            # Mode wasn't specified, if SourcePath is specified then check that the Modes match
            if str(oct(stat_info.st_mode))[-3:] != str(oct(stat_info_src.st_mode))[-3:]:
                return False
    return True

def ConvertLongModeToNumeric(Mode):
    u_r = Mode[0]
    u_w = Mode[1]
    u_x = Mode[2]
    g_r = Mode[3]
    g_w = Mode[4]
    g_x = Mode[5]
    o_r = Mode[6]
    o_w = Mode[7]
    o_x = Mode[8]
    first_digit = 0
    second_digit = 0
    third_digit = 0
    if u_r == "r":
        first_digit += 4
    elif u_r == "-":
        pass
    else:
        raise Exception("Error: Invalid character for character 0 in Mode")

    if u_w == "w":
        first_digit += 2
    elif u_w == "-":
        pass
    else:
        raise Exception("Error: Invalid character for character 1 in Mode")

    if u_x == "x":
        first_digit += 1
    elif u_x == "-":
        pass
    else:
        raise Exception("Error: Invalid character for character 2 in Mode")

    if g_r == "r":
        second_digit += 4
    elif g_r == "-":
        pass
    else:
        raise Exception("Error: Invalid character for character 3 in Mode")

    if g_w == "w":
        second_digit += 2
    elif g_w == "-":
        pass
    else:
        raise Exception("Error: Invalid character for character 4 in Mode")

    if g_x == "x":
        second_digit += 1
    elif g_x == "-":
        pass
    else:
        raise Exception("Error: Invalid character for character 5 in Mode")

    if o_r == "r":
        third_digit += 4
    elif o_r == "-":
        pass
    else:
        raise Exception("Error: Invalid character for character 6 in Mode")

    if o_w == "w":
        third_digit += 2
    elif o_w == "-":
        pass
    else:
        raise Exception("Error: Invalid character for character 7 in Mode")

    if o_x == "x":
        third_digit += 1
    elif o_x == "-":
        pass
    else:
        raise Exception("Error: Invalid character for character 8 in Mode")

    return str(first_digit) + str(second_digit) + str(third_digit)

def SetOwnerGroupMode(DestinationPath, SourcePath, fc):
    stat_info = LStatFile(DestinationPath)
    if stat_info == None :
        return False
    
    if SourcePath:
        stat_info_src = LStatFile(SourcePath)
        if stat_info_src == None:
            return False
    
    if fc.Owner:
        Specified_Owner_ID = pwd.getpwnam(fc.Owner)[2]
        if Specified_Owner_ID != pwd.getpwuid(stat_info.st_uid)[2]:
            print("Changing owner of " + DestinationPath + " to " + str(Specified_Owner_ID))
            if LChown(DestinationPath, Specified_Owner_ID, -1) != None :
                return False

    elif SourcePath:
        src_uid = pwd.getpwuid(stat_info_src.st_uid)[2]
        if pwd.getpwuid(stat_info.st_uid)[2] != src_uid:
            print("Changing owner of " + DestinationPath + " to " + str(src_uid))
            if LChown(DestinationPath, Specified_Owner_ID, -1) != None :
                return False

    if fc.Group:
        Specified_Group_ID = grp.getgrnam(fc.Group)[2]
        if Specified_Group_ID != grp.getgrgid(stat_info.st_gid)[2]:
            print("Changing group of " + DestinationPath + " to " + str(Specified_Group_ID))
            if LChown(DestinationPath, -1, Specified_Group_ID) != None :
                return False


    elif SourcePath:
        src_gid = grp.getgrgid(stat_info_src.st_gid)[2]
        if grp.getgrgid(stat_info.st_gid)[2] != src_gid:
            print("Changing group of " + DestinationPath + " to " + str(src_gid))
            if LChown(DestinationPath,src_gid , -1) != None :
                return False

    # Mode is irrelevant to symlinks
    if not os.path.islink(DestinationPath):
        if fc.Mode:
            if str(oct(stat_info.st_mode))[-3:] != fc.Mode:
                print("Changing mode of " + DestinationPath + " to " + fc.Mode)
                if Chmod(DestinationPath, fc.Mode) != None :
                    return False
        elif SourcePath:
            src_mode = str(oct(stat_info_src.st_mode))[-3:]
            if str(oct(stat_info.st_mode))[-3:] != src_mode:
                print("Changing mode of " + DestinationPath + " to " + src_mode)
                if Chmod(DestinationPath, src_mode) != None :
                    return False
    return True
    
def SetDirectoryRecursive(DestinationPath, SourcePath, fc):
    if not os.path.exists(DestinationPath):
        MakeDirs(DestinationPath)
    if SetOwnerGroupMode(DestinationPath, SourcePath, fc) == False:
        return False
    if fc.Recurse == "false":
        return True
    Destination_subfiles = ListDir(DestinationPath)
    if Destination_subfiles == None:
        return False
    if not SourcePath:
        # Enforce Owner/Group/Mode specified
        for f in Destination_subfiles:
            f_destpath = os.path.join(DestinationPath, f)
            if not os.path.islink(f_destpath):
                if os.path.isfile(f_destpath):
                    if SetOwnerGroupMode(f_destpath, "", fc) == False :
                        return False
                elif os.path.isdir(f_destpath):
                    if SetDirectoryRecursive(f_destpath, "", fc) == False :
                        return False
        return True

    Source_subfiles = ListDir(SourcePath)

    # For all files in SourcePath's directory, ensure they exist with proper contents and stat in DestionationPath's directory 
    for f in Source_subfiles:
        f_srcpath = os.path.join(SourcePath, f)
        f_destpath = os.path.join(DestinationPath, f)

        if os.path.islink(f_srcpath):
            if TestLink(f_destpath, f_srcpath, fc) == False:
                if SetLink(f_destpath, f_srcpath, fc) == False:
                    return False
        elif os.path.isfile(f_srcpath):
            if TestFile(f_destpath, f_srcpath, fc) == False:
                if SetFile(f_destpath, f_srcpath, fc) == False:
                    return False
        elif os.path.isdir(f_srcpath):
            if SetDirectoryRecursive(f_destpath, f_srcpath, fc) == False:
                return False
        
    return True
      
def SetFile(DestinationPath, SourcePath, fc):
    error=None
    if os.path.exists(DestinationPath) and (os.path.islink(DestinationPath) or os.path.isdir(DestinationPath)):
        if fc.Force == "true":
            RemovePath(DestinationPath)
        else:
            print("Error: " + DestinationPath + " is not a file; cannot overwrite without the 'Force' option being true")
            return False

    if SourcePath:
        should_copy_file = False
        if fc.Checksum == "ctime" or fc.Checksum == "mtime":
            if os.path.isfile(DestinationPath):
                if CompareFiles(DestinationPath, SourcePath,  fc.Checksum) == -1:
                    should_copy_file = True
            else:
                should_copy_file = True
        else:
            # Just copy the file if this is a resource intensive file comparison
            should_copy_file = True

        if should_copy_file:
            if CopyFile(SourcePath, DestinationPath) == False :
                return False;
            
    elif fc.Contents:
        if WriteFile(DestinationPath, fc.Contents) != None:
            print("Error: Unable to write file at " + DestinationPath)
            return False
    else:
        # Create a file with nothing in it
        try:
            open(DestinationPath, 'a').close()
        except OSError, error:
            print("Exception creating file " + DestinationPath  + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)
        except IOError, error:
            print("Exception creating file " + DestinationPath + " Error Code: " + str(error.errno) + " Error: " + error.message + error.strerror,file=sys.stderr)

    SetOwnerGroupMode(DestinationPath, SourcePath, fc)

    return True
         
def SetDirectory(DestinationPath, SourcePath, fc):
    if os.path.exists(DestinationPath) and not os.path.isdir(DestinationPath):
        if fc.Force == "true":
            RemovePath(DestinationPath)
        else:
            return False

    return SetDirectoryRecursive(DestinationPath, SourcePath, fc)

def SetLink(DestinationPath, SourcePath, fc):
    if not SourcePath:
        print("Error: Need a source path in order to create a new symbolic link.")
        return False

    if os.path.exists(DestinationPath):
        if os.path.islink(DestinationPath) or fc.Force == "true":
            RemovePath(DestinationPath)
        else:
            print("Error: Unable to overwrite currently existing file at " + DestinationPath + " without the Force option being true.")
            return False

    if os.path.islink(SourcePath):
        if fc.Links == "follow":
            if os.path.isfile(SourcePath):
                SetFile(DestinationPath, os.path.realpath(SourcePath), fc)
            elif os.path.isdir(SourcePath):
                SetDirectoryRecursive(DestinationPath, os.path.realpath(SourcePath), fc)
        elif fc.Links == "manage":
            Symlink(os.readlink(SourcePath), DestinationPath)
            
        elif fc.Links == "ignore":
            # Ignore all symlinks
            return True
    else:
        Symlink(SourcePath, DestinationPath)

    SetOwnerGroupMode(DestinationPath, SourcePath, fc)

    return True

def Set(DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode):
    fc = FileContext(Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode)

    if not DestinationPath:
        return [-1]

    if fc.Ensure == "present":
        if fc.Type == "file":
            if SetFile(DestinationPath, SourcePath, fc) == False:
                return [-1]
        elif fc.Type == "directory":
            if SetDirectory(DestinationPath, SourcePath, fc) == False:
                return [-1]
        elif fc.Type == "link":
            if SetLink(DestinationPath, SourcePath, fc) == False:
                return [-1]

    elif fc.Ensure == "absent":
        RemovePath(DestinationPath)
        return [0]

    return [0]

def TestDirectory(DestinationPath, SourcePath, fc):
    if not os.path.exists(DestinationPath) or not os.path.isdir(DestinationPath):
        return False

    if TestOwnerGroupMode(DestinationPath, SourcePath, fc) == False:
        return False

    if fc.Recurse == "false":
        return True

    Destination_subfiles = ListDir(DestinationPath)
    if Destination_subfiles == None:
        return False

    if not SourcePath:
        # Enforce Owner/Group/Mode specified
        for f in Destination_subfiles:
            f_destpath = os.path.join(DestinationPath, f)
            if not os.path.islink(f_destpath):
                if os.path.isfile(f_destpath):
                    if TestOwnerGroupMode(f_destpath, "", fc) == False:
                        return False
                elif os.path.isdir(f_destpath):
                    if TestDirectory(f_destpath, "", fc) == False:
                        return False
        return True

    Source_subfiles = ListDir(SourcePath)
    if Source_subfiles == None:
        return False

    for f in Source_subfiles:
        if f not in Destination_subfiles:
            print("File: " + f + " does not exist in: " + SourcePath)
            return False

        f_destpath = os.path.join(DestinationPath, f)
        f_srcpath = os.path.join(SourcePath, f)

        if os.path.islink(f_srcpath):
            if TestLink(f_destpath, f_srcpath, fc) == False:
                return False
        elif os.path.isfile(f_srcpath):
            if TestFile(f_destpath, f_srcpath, fc) == False:
                return False
        elif os.path.isdir(f_srcpath):
            if TestDirectory(f_destpath, f_srcpath, fc) == False:
                return False

    return True

def TestFile(DestinationPath, SourcePath, fc):
    if not os.path.exists(DestinationPath) or not os.path.isfile(DestinationPath) or os.path.islink(DestinationPath):
        return False

    if TestOwnerGroupMode(DestinationPath, SourcePath, fc) == False:
        return False

    if SourcePath:
        if not os.path.isfile(SourcePath):
            return False

        if os.path.islink(SourcePath):
            if fc.Links == "follow":
                if os.path.isdir(os.path.realpath(SourcePath)):
                    print("Error: Expecting a file, but source link points to directory")
                    return False
            else:
                if not os.path.islink(DestinationPath):
                    return False
                if os.readlink(DestinationPath) != os.readlink(SourcePath):
                    return False

        elif CompareFiles(DestinationPath, SourcePath,  fc.Checksum) == -1:
            return False

    elif fc.Contents:
        dest_file = ReadFile(DestinationPath)
        if fc.Contents != dest_file:
            return False

    return True

def TestLink(DestinationPath, SourcePath, fc):
    if SourcePath:
        if os.path.islink(SourcePath):
            if fc.Links == "follow":
                if os.path.isdir(SourcePath):
                    if TestDirectory(DestinationPath, os.path.realpath(SourcePath), fc) == False:
                        return False
                elif os.path.isfile(SourcePath):
                    if TestFile(DestinationPath, os.path.realpath(SourcePath), fc) == False:
                        return False
            elif fc.Links == "manage":
                if not os.path.islink(DestinationPath):
                    return False

                if os.readlink(DestinationPath) != os.readlink(SourcePath):
                    return False
            elif fc.Links == "ignore":
                return True
        else:
            if os.readlink(DestinationPath) != SourcePath:
                return False

    if TestOwnerGroupMode(DestinationPath, SourcePath, fc) == False:
        return False

    return True

def Test(DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode):
    fc = FileContext(Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode)

    if not DestinationPath:
        return [-1]

    if fc.Ensure == "present":
        if fc.Type == "file":
            if TestFile(DestinationPath, SourcePath, fc) == False:
                return [-1]
        elif fc.Type == "directory":
            if TestDirectory(DestinationPath, SourcePath, fc) == False:
                return [-1]
        elif fc.Type == "link":
            if TestLink(DestinationPath, SourcePath, fc) == False:
                return [-1]
    elif fc.Ensure == "absent":
        if os.path.exists(DestinationPath):
            return [-1]

        return [0]

    return [0]

def Get(DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode):
    if not DestinationPath:
        Ensure = "Absent"
        SourcePath = Type = Force = Contents = Checksum = Recurse = Links = Owner = Group = Mode = ModifiedDate = ""
        return [-1, DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode, ModifiedDate]

    if not os.path.exists(DestinationPath):
        Ensure = "Absent"
        SourcePath = Type = Force = Contents = Checksum = Recurse = Links = Owner = Group = Mode = ModifiedDate = ""
        return [0, DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode, ModifiedDate]

    Contents = ""
    Checksum = ""
    Force = ""
    Recurse = ""
    Links = ""

    stat_info = os.lstat(DestinationPath)

    Owner = pwd.getpwuid(stat_info.st_uid)[0]
    Group = grp.getgrgid(stat_info.st_gid)[0]
    Mode = str(oct(stat_info.st_mode))[-3:]
    if os.path.islink(DestinationPath):
        Type = "link"
    elif os.path.isfile(DestinationPath):
        Type = "file"
    elif os.path.isdir(DestinationPath):
        Type = "directory"
        
    ModifiedDate = str(int(stat_info.st_mtime))

    return [0, DestinationPath, SourcePath, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode, ModifiedDate]

class FileContext:
    def __init__(self, Ensure, Type, Force, Contents, Checksum, Recurse, Links, Owner, Group, Mode):
        if not Checksum:
            Checksum = "md5"
        if not Recurse:
            Recurse = "false"
        if not Force:
            Force = "false"
        if not Type:
            Type = "file"
        if not Ensure:
            Ensure = "present"
        if not Links:
            Links = "manage"
    
        self.Ensure = Ensure.lower()
        self.Type = Type.lower()
        self.Force = Force.lower()
        self.Contents = Contents
        self.Checksum = Checksum.lower()
        self.Recurse = Recurse.lower()
        self.Links = Links.lower()
        self.Owner = Owner
        self.Group = Group

        error=None

        if Mode:
            if len(Mode) == 9:
                try:
                    Mode = ConvertLongModeToNumeric(Mode)
                except Exception, error:
                    print("Exception in ConvertLongModeToNumeric on " + Mode  + " Error: " + error.message,file=sys.stderr)    
            elif len(Mode) == 3:
                # Already in proper format
                pass
            else:
                print("Error: Invalid Mode: " + Mode)
                Mode = ""

        self.Mode = Mode

import unittest

class LinuxFileTestCases(unittest.TestCase):
    """
    Test cases for LinuxFile
    """
    def setUp(self):
        """
        Setup test resources
        """
        os.system('rm -rf /tmp/*pp*')

    def tearDown(self):
        """
        Remove test resources.
        """
        os.system('rm -rf /tmp/*pp*')

    def noop(self,arg2):
        """
        Set a method to noop() to prevent its operation.
        """
        pass

    def testSetFileAbsent(self):
        assert Set("/tmp/1.pp", "", "Absent", "File", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Absent", "File", "", "", "md5", "", "", "", "", "") should return [0]'

    def testSetFileAbsentError(self):
        assert Set("/tp/1.pp", "", "Absent", "File", "", "", "md5", "", "", "", "", "")==[0],'Set("/tp/1.pp", "", "Absent", "File", "", "", "md5", "", "", "", "", "") should return [0]'

    def testSetFileData(self):
        assert Set("/tmp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "") should return [0]'
        d,e=ReadFile('/tmp/1.pp')
        assert d=="These are the contents of 1.pp","File contents mismatch:"+d

    def testSetFileDataError(self):
        assert Set("/tp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "")==[-1],'Set("/tp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "") should return [-1]'

    def testSetFileNoData(self):
        assert Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "") should return [0]'
        d,e=ReadFile('/tmp/1.pp')
        assert len(d)==0,"The contents of 1.pp should be empty.  File contents mismatch:"+d

    def testTestCompareFilesMD5Same(self):
        assert Set("/tmp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "") should return [0]'
        assert Set("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "") should return [0]'
        assert Test("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "")==[0],'Test("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "") should return [0]'
        
    def testTestCompareFilesMD5Different(self):
        assert Set("/tmp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "") should return [0]'
        assert Set("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "") should return [0]'
        assert Test("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "")==[0],'Test("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "") should return [0]'
        
    def testTestCompareFilesMD5Error(self):
        assert Test("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "")==[-1],'Test("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "") should return [-1]'

    def testSetFileCopy(self):
        assert Set("/tmp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "") should return [0]'
        assert Set("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "") should return [0]'
        d,e=ReadFile('/tmp/12.pp')
        assert d=="These are the contents of 1.pp","File contents mismatch:"+d

#     def testSetFileCopyError(self):
#         assert Set("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "")==[-1],'Set("/tmp/12.pp", "/tmp/1.pp", "", "", "", "", "md5", "", "", "", "", "") should return [-1]'

    def testSetDirectoryPresent(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        assert os.path.isdir('/tmp/pp') == True,'Directory /tmp/pp is missing.'

    def testSetDirectoryAbsent(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        assert Set("/tmp/pp", "", "Absent", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Absent", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        assert os.path.isdir('/tmp/pp') == False,'Directory /tmp/pp is present.'

    def testSetDirectoryAbsentError(self):
        assert Set("/tmp/pp", "", "Absent", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Absent", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'

    def testSetCopyDirectoryToNew(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        assert os.path.isdir('/tmp/pp') == True,'Directory /tmp/pp is missing.'
        assert Set("/tmp/ppp", "/tmp/pp", "Present", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        assert os.path.isdir('/tmp/ppp') == True,'Directory /tmp/ppp is missing.'
        
#     def testSetCopyDirectoryToNewError(self):
#         assert Set("/tmp/ppp", "/tmp/pp", "Present", "Directory", "", "", "md5", "", "", "", "", "")==[-1],'Set("/tmp/ppp", "/tmp/pp", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [-1]'
#         assert os.path.isdir('/tmp/ppp') == False,'Directory /tmp/ppp should be missing.'
        
    def testSetCopyDirectoryToExistingForce(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        assert os.path.isdir('/tmp/pp') == True,'Directory /tmp/pp is missing.'
        assert Set("/tmp/pp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "") should return [0]'
        d,e=ReadFile('/tmp/pp/1.pp')
        assert d=="These are the contents of 1.pp","File contents mismatch:"+d
        assert Set("/tmp/ppp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        assert os.path.isdir('/tmp/ppp') == True,'Directory /tmp/ppp is missing.'
        assert Set("/tmp/ppp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "")==[0],'Set("/tmp/ppp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "") should return [0]'
        d,e=ReadFile('/tmp/ppp/1.pp')
        assert d=="These are the contents of 1.pp","File contents mismatch:"+d
        assert Set("/tmp/ppp", "/tmp/pp", "Present", "Directory", "Force", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'

    def testSetModeRecursive(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        assert Set("/tmp/pp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "") should return [0]'
        assert Set("/tmp/pp/12.pp", "", "Present", "File", "", "These are the contents of 12.pp", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp/12.pp", "", "Present", "File", "", "These are the contents of 12.pp", "md5", "", "", "", "", "") should return [0]'
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "755")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "755") should return [0]'
        assert (StatFile('/tmp/pp/1.pp').st_mode & 0755 ) == 0755 and (StatFile('/tmp/pp/12.pp').st_mode & 0755) == 0755,'Mode of /tmp/pp/1.pp and /tmp/pp/12.pp should be 755'

    def testSetOwnerRecursive(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        assert Set("/tmp/pp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp/1.pp", "", "Present", "File", "", "These are the contents of 1.pp", "md5", "", "", "", "", "") should return [0]'
        assert Set("/tmp/pp/12.pp", "", "Present", "File", "", "These are the contents of 12.pp", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp/12.pp", "", "Present", "File", "", "These are the contents of 12.pp", "md5", "", "", "", "", "") should return [0]'
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "mail", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "mail", "") should return [0]'
        assert StatFile('/tmp/pp/1.pp').st_gid == grp.getgrnam('mail')[2]  and StatFile('/tmp/pp/12.pp').st_gid == grp.getgrnam('mail')[2] ,'Group of /tmp/pp/1.pp and /tmp/pp/12.pp should be mail'

    def testTestNoDestPathError(self):
        assert Test("", "", "Present", "File", "", "", "md5", "", "", "", "", "")==[-1],'Test("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "") should return [-1]'

    def testTestFilePresentError(self):
        assert Test("/tp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "")==[-1],'Test("/tp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "") should return [-1]'

    def testTestFilePresent(self):
        assert Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "") should return [0]'
        assert Test("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "")==[0],'Test("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "") should return [0]'

    def testTestFileAbsentError(self):
        assert Test("/tp/1.pp", "", "Absent", "File", "", "", "md5", "", "", "", "", "")==[0],'Test("/tp/1.pp", "", "Absent", "File", "", "", "md5", "", "", "", "", "") should return [0]'

    def testTestFileAbsent(self):
        assert Test("/tp/1.pp", "", "Absent", "File", "", "", "md5", "", "", "", "", "")==[0],'Test("/tp/1.pp", "", "Absent", "File", "", "", "md5", "", "", "", "", "") should return [0]'

    def testTestDirectoryRecurseCheckOwnerError(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "") should return [0]'
        assert Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "") should return [0]'
        assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "udos", "", "")==[-1],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "udos", "", "") should return [-1]'

    def testTestDirectoryRecurseCheckGroupError(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "mail", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "mail", "") should return [0]'
        assert Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "") should return [0]'
        assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "udos", "")==[-1],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "udos", "") should return [-1]'

    def testTestDirectoryRecurseCheckModeError(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "755")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "755") should return [0]'
        assert Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "755")==[0],'Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "755") should return [0]'
        assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "744")==[-1],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "744") should return [-1]'

    def testTestDirectoryRecurseCheckOwner(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "") should return [0]'
        assert Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "") should return [0]'
        me =  pwd.getpwuid(os.getuid()).pw_name
        assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", me, "", "")==[0],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "'+me+'", "", "") should return [0]'

    def testTestDirectoryRecurseCheckGroup(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "mail", "") should return [0]'
        assert Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "") should return [0]'
        me = grp.getgrgid(os.getgid()).gr_name
        assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", me, "")==[0],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "'+me+'", "", "") should return [0]'

    def testTestDirectoryRecurseCheckMode(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "755")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "755") should return [0]'
        assert Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "755")==[0],'Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "755") should return [0]'
        assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "755")==[0],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "True", "", "", "", "755") should return [0]'

    def testGetNoDestPathError(self):
        assert Get("", "", "Present", "File", "", "", "md5", "", "", "", "", "")[0]==-1,'Get("", "", "Present", "File", "", "", "md5", "", "", "", "", "") should return [-1]'

    def testGetFilePresent(self):
        assert Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "")[0]==0,'Set("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "") should return [0]'
        assert Get("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "")[0]==0,'Get("/tmp/1.pp", "", "Present", "File", "", "", "md5", "", "", "", "", "") should return [0]'

    def testGetDirectoryPresent(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "")[0]==0,'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "","", "")==[0],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        assert Get("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "")[0]==0,'Get("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'

    def testTestDirectoryCheckOwnerError(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "udos", "", "")==[-1],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "udos", "", "") should return [-1]'

    def testTestDirectoryCheckGroupError(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "mail", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "mail", "") should return [0]'
        assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "udos", "")==[-1],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "udos", "") should return [-1]'

#     def testTestDirectoryCheckModeError(self):
#         assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "776")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "755") should return [0]'
#         assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "744")==[-1],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "744") should return [-1]'

    def testTestDirectoryCheckOwner(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "") should return [0]'
        me =  pwd.getpwuid(os.getuid()).pw_name
        assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", me, "", "")==[0],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "'+me+'", "", "") should return [0]'

    def testTestDirectoryCheckGroup(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "mail", "") should return [0]'
        me = grp.getgrgid(os.getgid()).gr_name
        assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", me, "")==[0],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "'+me+'", "", "") should return [0]'

    def testTestDirectoryCheckMode(self):
        assert Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "776")==[0],'Set("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "776") should return [0]'
        assert Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "776")==[0],'Test("/tmp/pp", "", "Present", "Directory", "", "", "md5", "", "", "", "", "776") should return [0]'

if __name__ == '__main__':
    s=unittest.TestLoader().loadTestsFromTestCase(LinuxFileTestCases)
    unittest.TextTestRunner(verbosity=2).run(s)
