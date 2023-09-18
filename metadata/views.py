from rest_framework import status
import pyhindsight
from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response
from .models import Chrome, Cookie, Download, History, LoginItem, LocalStorage
import platform
from authentication.models import CustomUser
from pyhindsight.analysis import AnalysisSession
import logging
import os
import subprocess
from .serializer import ChromeSerializer, SendChromeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView


@api_view(['POST'])
@permission_classes([HasAPIKey,])
def analyze_chrome(request):
    #   username = request.data.get('pc_username')
    #   user_id = request.data.get('user_id')
    serializer = SendChromeSerializer(data=request.data)
    if serializer.is_valid() and platform.system() == 'Windows':
        username = serializer.data.get('pc_username')
        user_id = request.user.pk

        #   the below code coverts the input of the path to python path
        input_path = r'C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Default'
        chrome_data_path = input_path.replace('<YourUsername>', username)
        chrome_data_path = chrome_data_path.replace('\\', '\\\\')
        path_for_analysis_log = r'C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data'
        cache_dir = path_for_analysis_log.replace('<YourUsername>', username)
        cache_dir = cache_dir.replace('\\', '\\\\')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=400)

        if process_exists('chrome.exe'):
            os.system("taskkill /f /im chrome.exe")

            analysis_session = AnalysisSession()

            #   cache_dir = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
            #  "Google", "Chrome", "User Data", )

            new_cache_dir = os.path.join(cache_dir, "Default")
            analysis_session.input_path = cache_dir
            analysis_session.cache_path = os.path.join(cache_dir, 'Cache\Cache_Data')

            analysis_session.browser_type = 'Chrome'
            analysis_session.no_copy = True
            analysis_session.timezone = None

            log_path = os.path.join(cache_dir, 'analysis.log')

            # Configure logging
            logging.basicConfig(filename=log_path, level=logging.FATAL,
                                format='%(asctime)s.%(msecs).03d | %(levelname).01s | %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')

            analysis_session.run()

            chrome = Chrome.objects.create(user=user, pc_username=username)

            # Process and save data into related models
            for p in analysis_session.parsed_artifacts:
                if isinstance(p, pyhindsight.browsers.webbrowser.WebBrowser.CookieItem):
                    #   cookie = Cookie.objects.create(creation_time=p.timestamp_desc, user=request.user, name=p.name,
                    #                                value=p.value,
                    #                                path=p.path, priority=p.priority)
                    cookies = Cookie.objects.bulk_create([Cookie(user=request.user, name=p.name,
                                                                 value=p.value,
                                                                 path=p.path, priority=p.priority)])
                    for cookie in cookies:
                        chrome.cookies.add(cookie)
                if isinstance(p, pyhindsight.browsers.webbrowser.WebBrowser.LoginItem):
                    logins = LoginItem.objects.bulk_create(
                        [LoginItem(creation_time=p.date_created, user=request.user, name=p.name,
                                   value=p.value,
                                   count=p.count, interpretation=p.interpretation)])
                    for login in logins:
                        chrome.logins.add(login)
                if isinstance(p, pyhindsight.browsers.chrome.Chrome.DownloadItem):
                    downloads = Download.objects.bulk_create(
                        [Download(user=request.user,
                                  download_id=p.download_id, download_url=p.url,
                                  download_target_path=p.target_path,
                                  download_danger_type=p.danger_type)])
                    for download in downloads:
                        chrome.downloads.add(download)
                if isinstance(p, pyhindsight.browsers.webbrowser.WebBrowser.LocalStorageItem):
                    storages = LocalStorage.objects.bulk_create([LocalStorage(user=request.user,
                                                                              origin=p.origin, key=p.key,
                                                                              value=p.value,
                                                                              source_path=p.source_path)])
                    for storage in storages:
                        chrome.storages.add(storage)
                if isinstance(p, pyhindsight.browsers.chrome.Chrome.URLItem):
                    histories = History.objects.bulk_create([History(user=request.user,
                                                                     title=p.title, url=p.url,
                                                                     visit_time=p.visit_time,
                                                                     visit_source=p.visit_source,
                                                                     visit_duration=p.visit_duration)])
                    for history in histories:
                        chrome.history.add(history)

            data = ChromeSerializer(chrome)

            return Response(data.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There are two reasons for this error either chrome is presently not running or '
                                      'you do not have chrome installed. Kindly ensure chrome is running'},
                            status=status.HTTP_204_NO_CONTENT)
    elif serializer.is_valid() and platform.system == 'Mac':
        username = serializer.data.get('pc_username')
        user_id = serializer.data.get('user_id')

        #   the below code coverts the input of the path to python path
        input_path = r'<YourUsername>/Library/Application Support/Google/Chrome/Default'
        chrome_data_path = input_path.replace('<YourUsername>', username)
        chrome_data_path = chrome_data_path.replace('\\', '\\\\')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=400)

        if process_exists('chrome.exe'):
            os.system("taskkill /f /im chrome.exe")

            analysis_session = AnalysisSession()

            #   cache_dir = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
            #  "Google", "Chrome", "User Data", )

            cache_dir = os.path.join(chrome_data_path, "Default")
            analysis_session.input_path = cache_dir
            analysis_session.cache_path = os.path.join(cache_dir, 'Cache\Cache_Data')

            analysis_session.browser_type = 'Chrome'
            analysis_session.no_copy = True
            analysis_session.timezone = None

            log_path = os.path.join(cache_dir, 'analysis.log')

            # Configure logging
            logging.basicConfig(filename=log_path, level=logging.FATAL,
                                format='%(asctime)s.%(msecs).03d | %(levelname).01s | %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')

            analysis_session.run()

            chrome = Chrome.objects.create(user=user, pc_username=username)

            # Process and save data into related models
            for p in analysis_session.parsed_artifacts:
                if isinstance(p, pyhindsight.browsers.webbrowser.WebBrowser.CookieItem):
                    cookie = Cookie.objects.create(creation_time=p.timestamp_desc, user=request.user, name=p.name,
                                                   value=p.value,
                                                   path=p.path, priority=p.priority)

                    chrome.cookies.add(cookie)
                if isinstance(p, pyhindsight.browsers.webbrowser.WebBrowser.LoginItem):
                    login_item = LoginItem.objects.create(creation_time=p.date_created, user=request.user, name=p.name,
                                                          value=p.value,
                                                          count=p.count, interpretation=p.interpretation)
                    chrome.logins.add(login_item)
                if isinstance(p, pyhindsight.browsers.chrome.Chrome.DownloadItem):
                    download = Download.objects.create(start_time=p.date_created, user=request.user,
                                                       download_id=p.download_id, url=p.url,
                                                       download_target_path=p.target_path,
                                                       aownload_danger_type=p.danger_type)
                    chrome.downloads.add(download)
                if isinstance(p, pyhindsight.browsers.webbrowser.WebBrowser.LocalStorageItem):
                    storage = LocalStorage.objects.create(user=request.user,
                                                          origin=p.origin, key=p.key,
                                                          value=p.value,
                                                          source_path=p.source_path)
                    chrome.storages.add(storage)
                if isinstance(p, pyhindsight.browsers.chrome.Chrome.URLItem):
                    history = History.objects.create(user=request.user,
                                                     title=p.title, url=p.url,
                                                     visit_time=p.visit_time,
                                                     visit_source=p.visit_source,
                                                     visit_duration=p.visit_duration)
                    chrome.history.add(history)

                return Response(chrome, status=200)



    else:
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def process_exists(process_name):
    procs = str(subprocess.check_output('tasklist'))
    return process_name in procs


class GetChromeView(RetrieveAPIView):
    queryset = Chrome.objects.all()
    serializer_class = ChromeSerializer
    authentication_classes = ()
    permission_classes = ()
    search_fields = ('date', 'user', 'pc_username', )
    pagination_class = PageNumberPagination

    #   def get(self, *args, **kwargs):
    #       user_id = kwargs['user_id']
        #return JsonResponse(data=list(Chrome.objects.filter(name='Frozen', market=market).select_related('market', 'merchant', 'category').values()), safe=False)
    #       user = CustomUser.objects.get(id=user_id)
    #       chrome = Chrome.objects.filter(user=user).select_related('user',)
    #       chrome = ChromeSerializer(chrome)
    #       return Response(chrome, status=status.HTTP_200_OK)
