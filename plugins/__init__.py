import sys
import os.path

__all__=open('plugins/activeplugins.txt').read().split('\n')

pluginlibs = os.path.dirname(os.path.abspath(__file__))
sys.path.append(pluginlibs)