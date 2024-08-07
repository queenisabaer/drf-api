from rest_framework import serializers
from .models import Post
from likes.models import Like

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

    # to validate a field in a model use the rest framework’s field level validation methods.
    # They’re called: validate_fieldName
    def validate_image(self, value):
        # check if the file size is bigger than two megabytes
        # The default file size unit is a byte. If  we multiply it by 1024, we’ll get kilobytes.
        # Multiplied again by 1024, get megabytes. multiply by 2 = 2 MB
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'image size is larger than 2 MB!'
            )
        # limit the image width to 4096 pixels 
        if value.image.width > 4096 :
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        if value.image.height > 4096 :
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        return value


    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'image_filter', 
            'like_id', 'comments_count', 'likes_count'
        ]