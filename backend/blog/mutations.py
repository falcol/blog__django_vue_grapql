import graphene
import graphql_jwt
from blog import models, types
from graphene_file_upload.scalars import Upload

# Mutation sends data to the database


# Customize the ObtainJSONWebToken behavior to include the user info
class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(types.UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class CreateUser(graphene.Mutation):
    user = graphene.Field(types.UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = models.User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class UpdateUserProfile(graphene.Mutation):
    user = graphene.Field(types.UserType)

    class Arguments:
        user_id = graphene.ID(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        avatar = Upload(required=False)
        bio = graphene.String(required=False)
        location = graphene.String(required=False)
        website = graphene.String(required=False)

    def mutate(
        self,
        info,
        user_id,
        first_name="",
        last_name="",
        avatar="",
        bio="",
        location="",
        website="",
    ):
        user = models.User.objects.get(pk=user_id)

        user.first_name = first_name
        user.last_name = last_name
        user.avatar = avatar
        user.bio = bio
        user.location = location
        user.website = website

        user.save()

        return UpdateUserProfile(user=user)


class CreatePost(graphene.Mutation):
    post = graphene.Field(types.PostType)

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        featured_image = Upload(required=False)
        is_published = graphene.Boolean(required=False)
        is_featured = graphene.Boolean(required=False)
        category_id = graphene.ID(required=True)
        tag_ids = graphene.List(graphene.ID, required=False)

    def mutate(
        self,
        info,
        title,
        content,
        featured_image,
        is_published,
        is_featured,
        category_id,
        tag_ids,
    ):
        post = models.Post(
            title=title,
            content=content,
            featured_image=featured_image,
            is_published=is_published,
            is_featured=is_featured,
            category_id=category_id,
        )
        post.save()

        for tag_id in tag_ids:
            post.tags.add(tag_id)

        post.save()

        return CreatePost(post=post)


class CreateCategory(graphene.Mutation):
    category = graphene.Field(types.CategoryType)

    class Arguments:
        name = graphene.String(required=True)
        slug = graphene.String(required=True)
        description = graphene.String(required=True)

    def mutate(self, info, name, slug, description):
        category = models.Category(
            name=name,
            slug=slug,
            description=description,
        )
        category.save()

        return CreateCategory(category=category)


class CreateComment(graphene.Mutation):
    comment = graphene.Field(types.CommentType)

    class Arguments:
        content = graphene.String(required=True)
        user_id = graphene.ID(required=True)
        post_id = graphene.ID(required=True)

    @graphql_jwt.decorators.login_required
    def mutate(self, info, content, user_id, post_id):
        comment = models.Comment(
            content=content,
            user_id=user_id,
            post_id=post_id,
        )
        comment.save()

        return CreateComment(comment=comment)


class UpdatePostLike(graphene.Mutation):
    post = graphene.Field(types.PostType)

    class Arguments:
        post_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)

    def mutate(self, info, post_id, user_id):
        post = models.Post.objects.get(pk=post_id)

        if post.likes.filter(pk=user_id).exists():
            post.likes.remove(user_id)
        else:
            post.likes.add(user_id)

        post.save()

        return UpdatePostLike(post=post)


class UpdateCommentLike(graphene.Mutation):
    comment = graphene.Field(types.CommentType)

    class Arguments:
        comment_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)

    def mutate(self, info, comment_id, user_id):
        comment = models.Comment.objects.get(pk=comment_id)

        if comment.likes.filter(pk=user_id).exists():
            comment.likes.remove(user_id)
        else:
            comment.likes.add(user_id)

        comment.save()

        return UpdateCommentLike(comment=comment)


class Mutation(graphene.ObjectType):
    # Tokens
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_user = CreateUser.Field()
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()

    update_post_like = UpdatePostLike.Field()
    update_comment_like = UpdateCommentLike.Field()
    update_user_profile = UpdateUserProfile.Field()
