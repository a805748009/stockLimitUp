import os
import sys

if sys.platform == 'linux':
    __local_xtquant_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.libs')
    __xtquant_home_dir = os.path.join('/home', '.xtquant')
    try:
        os.makedirs(__xtquant_home_dir, exist_ok=True)
    except:
        pass

    __xtquant_lib_dir = os.path.join(__xtquant_home_dir, f'.libs{sys.version_info.major}.{sys.version_info.minor}')
    __do_symlink = not os.path.exists(__xtquant_lib_dir)
    if not __do_symlink \
        and not os.path.samefile(__local_xtquant_dir, os.path.realpath(__xtquant_lib_dir)):
        __do_symlink = True
        try:
            if os.path.isfile(__xtquant_lib_dir):
                os.remove(__xtquant_lib_dir)
            if os.path.islink(__xtquant_lib_dir):
                os.unlink(__xtquant_lib_dir)
            if os.path.isdir(__xtquant_lib_dir):
                import shutil
                shutil.rmtree(__xtquant_lib_dir) 
        except:
            pass
            
            
    if __do_symlink:
        try:
            os.symlink(__local_xtquant_dir, __xtquant_lib_dir, target_is_directory=True)
        except:
            import traceback
            traceback.print_exc()
            pass

