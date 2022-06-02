import random

from django.core.management.base import BaseCommand

from main.models import User, Post
from main.factories import (
    UserFactory,
    PostFactory,
)


class Command(BaseCommand):
    help = "Populate DB with a few Users and Posts for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            nargs="?",
            default=25,
            type=int,
            help="Count of Post to be created, default 25",
        )

    def handle(self, *args, **options):
        count = options["count"]

        # мы добавим count сообщений, но прочих объектов в базе должно быть >= half
        half = max(10, count // 2)

        for model, model_factory, target_count in (
            (User, UserFactory, half),
            (Post, PostFactory, count),
        ):
            current_count = model.objects.count()
            if current_count < target_count:
                model_factory.create_batch(target_count - current_count)

        user_count = User.objects.count()

        for post in Post.objects.all():
            target_likes_count = min(
                random.randint(1, 10), user_count - post.unlikes_count
            )
            delta = target_likes_count - post.likes_count
            if delta > 0:
                post.likes.add(
                    *random.sample(
                        list(
                            User.objects.exclude(liked_posts=post).exclude(
                                unliked_posts=post
                            )
                        ),
                        delta,
                    )
                )
            target_unlikes_count = min(
                random.randint(1, 3), user_count - post.likes_count
            )
            delta = target_unlikes_count - post.unlikes_count
            if delta > 0:
                post.unlikes.add(
                    *random.sample(
                        list(
                            User.objects.exclude(liked_posts=post).exclude(
                                unliked_posts=post
                            )
                        ),
                        delta,
                    )
                )
