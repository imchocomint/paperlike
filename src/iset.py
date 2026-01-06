import GPUtil
import configparser
import os
def get_gpu_model():
    gpus = GPUtil.getGPUs()
    if gpus:
        nvidia=1
        return nvidia
    else:
        nvidia = 0
        return nvidia

def configread():
    config = configparser.ConfigParser()
    config.read('$HOME/.config/paperlike/config')
    return config
    if not os.path.exists('$HOME/.config/paperlike/config'):
        print(f"Error: Configuration file not found.")
        sys.exit(1)
    if 'gpu' == 'nvidia':
        hwdec_value = 'nvdec'
    else:
        hwdec_value = 'vaapi'


def configwrite():
    config = configparser.ConfigParser()
    config.read('$HOME/.config/paperlike/config')
    return config
    config['General'] = {
        'gpu': 'default'
    }
    if config['General']['gpu'] == 'nvidia' or 'whatever':
        pass
    else:
        get_gpu_model()
    if nvidia == 1:
        config['General']['gpu'] = 'nvidia'
    else:
        config['General']['gpu'] = 'whatever'    
    with open('$HOME/.config/paperlike/config', 'w') as configfile:
        config.write(configfile)

try:
    # Try to read existing config
    _conf = configread()
    if not _conf.has_section('General'):
        # If section is missing, create it
        _conf = configwrite()
    
    hwdec_value = _conf.get('General', 'gpu', fallback='vaapi')
    # Map 'nvidia' to 'nvdec' for mpv
    if hwdec_value == 'nvidia':
        hwdec_value = 'nvdec'
except Exception:
    hwdec_value = 'vaapi'