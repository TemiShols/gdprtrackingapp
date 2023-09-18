from rest_framework import serializers
from .models import Chrome, Download, Cookie, History, LoginItem, LocalStorage


class ChromeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    downloads = serializers.StringRelatedField(many=True)
    cookies = serializers.StringRelatedField(many=True)
    history = serializers.StringRelatedField(many=True)
    logins =  serializers.StringRelatedField(many=True)
    storages = serializers.StringRelatedField(many=True)

    class Meta:
        model = Chrome
        fields = ('pc_username', 'user', 'downloads', 'cookies', 'history', 'logins', 'storages')

    def get_username(self):
        return self.request.user.email


class SendChromeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chrome
        fields = ('pc_username', 'user_id')
        # extra_fields = ('downloads')


class CookieSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_username')

    class Meta:
        model = Cookie
        fields = ('creation_time', 'name', 'value', 'path', 'priority',)
        # extra_fields = ('cookies')

    def get_username(self):
        return self.request.user.get_full_name()


class DownloadSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_username')

    class Meta:
        model = Download
        fields = '__all__'
        # extra_fields = ('downloads')

    def get_username(self):
        return self.request.user.get_full_name()


class HistorySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_username')

    class Meta:
        model = History
        fields = '__all__'
        # extra_fields = ('history')

    def get_username(self):
        return self.request.user.get_full_name()


class DirectoryPathSerializer(serializers.Serializer):
    path = serializers.CharField(max_length=255)
