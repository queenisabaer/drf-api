from django.db import IntegrityError
from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model
    The create method handles the unique constraint on 'owner' and 'post'
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'created_at', 'owner', 'post']
    
    def create(self, validated_data):
        try:
            # try  to return the newly created like by calling the create method with the validated_data.
            # is on the model serializer so we have to call super()
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible dublicate'
            })