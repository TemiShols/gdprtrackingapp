import pyhindsight
from pyhindsight.analysis import AnalysisSession
import logging
import os
import webbrowser
import subprocess

os.system("taskkill /f /im chrome.exe")
analysis_session = AnalysisSession()

#   cache_dir1 = 'C:\\Users\\tpsol\\AppData\\Local\\Google\\Chrome\\User Data\\'
cache_dir = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                         "Google", "Chrome", "User Data", )
analysis_session.input_path = cache_dir
analysis_session.cache_path = os.path.join(cache_dir, 'Cache\Cache_Data')
analysis_session.browser_type = 'Chrome'
analysis_session.no_copy = True
analysis_session.timezone = None

logging.basicConfig(filename=analysis_session.log_path, level=logging.FATAL,
                    format='%(asctime)s.%(msecs).03d | %(levelname).01s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
run_status = analysis_session.run()

for p in analysis_session.parsed_artifacts:
    if isinstance(p, pyhindsight.browsers.webbrowser.WebBrowser.SessionStorageItem):
        print('This is SessionStorageItem....origin: {}, Key: {}, Value: {},'.format(p.origin, p.value, p.key))
    if isinstance(p, pyhindsight.browsers.webbrowser.WebBrowser.LoginItem):
        print('This is LoginItem....Name: {}, value: {}, count:{}, Interpret: {}'.format(p.name, p.value, p.count, p.interpretation))
    if isinstance(p, pyhindsight.browsers.webbrowser.WebBrowser.LocalStorageItem):
        print('This is LocalStorageItem....origin: {}, Key: {}, Value: {},'.format(p.origin, p.value, p.key))
    if isinstance(p, pyhindsight.browsers.webbrowser.WebBrowser.FileSystemItem):
        print('This is FileSystemItem....origin: {}, Key: {}, Value: {},'.format(p.origin, p.value, p.key))
    if isinstance(p, pyhindsight.browsers.chrome.Chrome.URLItem):
        print('Url: {}, Location: {}'.format(p.url, p.title))
    if isinstance(p, pyhindsight.browsers.webbrowser.WebBrowser.CookieItem):
        print('Url: {}, Value: {}, Path: {}, Priority: {}'.format(p.name, p.value, p.path, p.priority))