import json
import os


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.posts = []
        self.unique_tags = set()
        self.load_posts(file_path)

    def load_posts(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"{file_path} not found. Please create data/processed_posts.json in your GitHub repo."
            )

        with open(file_path, encoding="utf-8") as f:
            self.posts = json.load(f)

        for post in self.posts:
            tags = post.get("tags", [])
            for tag in tags:
                self.unique_tags.add(tag)

    def get_tags(self):
        return sorted(list(self.unique_tags))

    def get_filtered_posts(self, length, language, tag):
        filtered_posts = []

        for post in self.posts:
            if (
                post.get("length") == length
                and post.get("language") == language
                and tag in post.get("tags", [])
            ):
                filtered_posts.append(post)

        return filtered_posts
