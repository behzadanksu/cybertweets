from math import ceil


def process_relevance(relevance):
    """
    Helper function to check for relevance in a string. In this case, if string is "relevant" return True,
    else if "irrelevant" return False, else return the string back.

    :param relevance: string
    :return: boolean if "relevant" or "irrelevant" and string if not equal to either
    """
    if relevance == 'relevant':
        return True
    elif relevance == 'irrelevant':
        return False
    else:
        return relevance


def make_filter(ttype, relevance, annotation):
    """
    Helper function to make the MongoDB operation. It accepts threat type, relevance, and relevance annotation
    :param ttype: string threat type
    :param relevance: boolean whether is relevant or not
    :param annotation: string with relevance information that includes "business"
    :return: dict() that represents the MongoDB filter
    """
    if ttype != 'all':
        if relevance != 'all':
            if annotation != 'all':
                if annotation == 'none':
                    return {'type': ttype, 'relevant': relevance, 'annotation': {'$exists': False}}
                return {'type': ttype, 'relevant': relevance, 'annotation': annotation}
            else:
                return {'type': ttype, 'relevant': relevance}
        else:
            if annotation != 'all':
                if annotation == 'none':
                    return {'type': ttype, 'annotation': {'$exists': False}}
                return {'type': ttype, 'annotation': annotation}
            else:
                return {'type': ttype}
    else:
        if relevance != 'all':
            if annotation != 'all':
                if annotation == 'none':
                    return {'relevant': relevance, 'annotation': {'$exists': False}}
                return {'relevant': relevance, 'annotation': annotation}
            else:
                return {'relevant': relevance}
        else:
            if annotation != 'all':
                if annotation == 'none':
                    return {'annotation': {'$exists': False}}
                return {'annotation': annotation}
            else:
                return {}


class Pagination(object):
    """
    Pagination:

    This class is used to perform the pagination in the web application
    """

    def __init__(self, page, limit_per_page, total_count):
        """
        Default constructor for the class
        :param page: initial page
        :param limit_per_page: limit per page
        :param total_count: total amount of items
        """
        self.page = page
        self.limit_per_page = limit_per_page
        self.total_count = total_count

    @property
    def pages(self):
        """
        Computes the amount of pages needed to show all items
        :return: int()
        """
        return int(ceil(self.total_count / float(self.limit_per_page)))

    @property
    def offset(self):
        """
        Computes the offset for the query needed
        :return: int()
        """
        return self.limit_per_page * (self.page - 1)

    @property
    def has_prev(self):
        """
        checks whether there are possible previous pages
        :return: boolean()
        """
        return self.page > 1

    @property
    def has_next(self):
        """
        Checks whether there are possible next pages
        :return: boolean()
        """
        return self.page < self.pages

    @property
    def prev_url(self):
        """
        Constructs the url for the previous page
        :return: string()
        """
        if self.has_prev:
            return "/tweets/page/" + str(self.page - 1)
        else:
            return None

    @property
    def next_url(self):
        """
        Constructs the url for the next page
        :return: string()
        """
        if self.has_next:
            return "/tweets/page/" + str(self.page + 1)
        else:
            return None

    @property
    def ellipsis(self):
        """
        Constructs the ellipsis dictionary to construct the ellipsis in the UI
        :return: dict()
        """
        return {"url": "", "value": "...", "current": False}

    @property
    def pages_url(self):
        """
        Constructs the dictionary for the pages in the pagination component in the UI
        :return: dict()
        """
        pages = []
        if self.pages <= 11:
            for i in range(1, self.pages + 1):
                page = {"url": "/tweets/page/{}".format(i), "value": i, "current": False}
                if i == self.page:
                    page['current'] = True
                pages.append(page)
        else:
            if self.page < 7:
                for i in range(1, 9):
                    page = {"url": "/tweets/page/{}".format(i), "value": i, "current": False}
                    if i == self.page:
                        page['current'] = True
                    pages.append(page)
                pages.append(self.ellipsis)
                for i in range(self.pages - 1, self.pages + 1):
                    pages.append({"url": "/tweets/page/{}".format(i), "value": i, "current": False})
            elif self.pages - self.page < 6:
                for i in range(1, 3):
                    pages.append({"url": "/tweets/page/{}".format(i), "value": i, "current": False})
                pages.append(self.ellipsis)
                for i in range(self.pages - 7, self.pages + 1):
                    page = {"url": "/tweets/page/{}".format(i), "value": i, "current": False}
                    if i == self.page:
                        page['current'] = True
                    pages.append(page)
            else:
                for i in range(1, 3):
                    pages.append({"url": "/tweets/page/{}".format(i), "value": i, "current": False})
                pages.append(self.ellipsis)
                for i in range(self.page - 2, self.page + 3):
                    if i == self.page:
                        pages.append({"url": "/tweets/page/{}".format(i), "value": i, "current": True})
                    else:
                        pages.append({"url": "/tweets/page/{}".format(i), "value": i, "current": False})
                pages.append(self.ellipsis)
                for i in range(self.pages - 1, self.pages + 1):
                    pages.append({"url": "/tweets/page/{}".format(i), "value": i, "current": False})
        return pages

    @property
    def key_pages(self):
        """
        This method creates 4 pre-programmed pages for easy to navigate to the middle of the dataset.

        These are hard-coded, so if the limit per page changes, these might not be in the middle anymore
        or might be out of bounds.

        :return: list(dict())
        """
        page1 = {"url": "/tweets/page/1", "value": 1, "current": False}
        if 1 == self.page:
            page1['current'] = True
        page72 = {"url": "/tweets/page/72", "value": 72, "current": False}
        if 72 == self.page:
            page72['current'] = True
        page143 = {"url": "/tweets/page/143", "value": 143, "current": False}
        if 143 == self.page:
            page143['current'] = True
        page214 = {"url": "/tweets/page/214", "value": 214, "current": False}
        if 214 == self.page:
            page214['current'] = True
        return [page1, page72, page143, page214]

