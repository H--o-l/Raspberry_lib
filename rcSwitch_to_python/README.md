# RC switch from python
## Dependencies
- [rcswitch-pi](https://github.com/r10r/rcswitch-pi)

## Installation
- Adapt *include_dirs* and *sources* in *setupRcSwitch.py* with your rcswitch-pi folder.

### For python 2
- `sudo apt-get install -y python-dev`
- `sudo rm -r build/`
- `sudo python setupRcSwitch.py install` 

### For python 3.4
- `sudo apt-get install -y python3-dev`
- `sudo rm -r build/`
- `sudo python3 setupRcSwitch.py install` 
