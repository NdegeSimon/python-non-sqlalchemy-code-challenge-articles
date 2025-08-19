class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise TypeError("Author must be of type Author")
        if not isinstance(magazine, Magazine):
            raise TypeError("Magazine must be of type Magazine")
        if not isinstance(title, str):
            raise TypeError("Title must be of type str")
        if not 5 <= len(title) <= 50:
            raise ValueError("Title must be between 5 and 50 characters")
        self._author = author
        self._magazine = magazine
        self._title = title
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise TypeError("Author must be of type Author")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise TypeError("Magazine must be of type Magazine")
        self._magazine = value

    def __setattr__(self, key, value):
        if key == '_title' and hasattr(self, '_title'):
            raise AttributeError("Cannot modify title after instantiation")
        super().__setattr__(key, value)


class Author:
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Names must be of type str")
        if len(name) == 0:
            raise ValueError("Names must be longer than 0 characters")
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    def __setattr__(self, key, value):
        if key == '_name' and hasattr(self, '_name'):
            raise AttributeError("Cannot modify name after instantiation")
        super().__setattr__(key, value)

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list(set(article.magazine for article in self.articles()))

    def add_article(self, magazine, title):
        if not isinstance(magazine, Magazine):
            raise TypeError("Magazine must be of type Magazine")
        if not isinstance(title, str) or not 5 <= len(title) <= 50:
            raise ValueError("Title must be a string between 5 and 50 characters")
        article = Article(self, magazine, title)
        self._articles.append(article)
        return article

    def topic_areas(self):
        if not self.articles():
            return None
        return list(set(article.magazine.category for article in self.articles()))


class Magazine:
    all = []

    def __init__(self, name, category):
        self.name = name
        self.category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be of type str")
        if not 2 <= len(value) <= 16:
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list(set(article.author for article in self.articles()))

    def article_titles(self):
        articles = self.articles()
        if not articles:
            return None
        return [article.title for article in articles]

    def contributing_authors(self):
        from collections import Counter
        author_counts = Counter(article.author for article in self.articles())
        return [author for author, count in author_counts.items() if count > 2] or None

    @classmethod
    def top_publisher(cls):
        if not cls.all or not Article.all:
            return None
        return max(cls.all, key=lambda mag: len(mag.articles()), default=None)