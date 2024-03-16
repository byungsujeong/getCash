from rest_framework import serializers
from .models import CashHistory

from users import serializers as user_serializers
from questions import serializers as question_serializers



class CashHistorySerializer(serializers.ModelSerializer):

    # user = user_serializers.UserSerializer(many=False)
    # question = question_serializers.QuestionSerializer(many=False)

    class Meta:
        model = CashHistory
        fields = '__all__'
        read_only_fields = ("id",)


class ReadOnlyCashHistorySerializer(serializers.ModelSerializer):

    question = question_serializers.QuestionSerializer(many=False)

    class Meta:
        model = CashHistory
        fields = '__all__'
        read_only_fields = ("id",)