from lxml import etree
from rest_framework import serializers
from django.contrib.auth import get_user_model
from unidecode import unidecode
from django.template.defaultfilters import slugify

from kernel.xml.models import Import, ImportLogItem
from kernel.book.models import Task, Page

UserModel = get_user_model()


PAGES = 'pages'
TASKS = 'tasks'


class XmlTask:

    def __init__(self, elem, context, parent_id=None):
        self.id = elem.get('id')
        self.data = dict()

        for child in elem.getchildren():
            self.data[child.tag] = child.text.strip() if child.text else None

        self.data['page'] = self.__get_page(parent_id)
        self.data['author'] = self.__get_author(elem, context)
        self.data['body'] = self.__get_body(elem)
        self.data['slug'] = self.__get_slug(elem)
        self.data['tests'] = self.__get_tests(elem)

        self.save()

    def __get_test(self, elem):
        test = dict()
        for child in elem.getchildren():
            test[child.tag] = child.text
        return test

    def __get_tests(self, elem):
        tests = list()
        xml_tests = elem.find('tests')
        if xml_tests is not None:
            children = xml_tests.getchildren()
            if children:
                for child in children:
                    tests.append(self.__get_test(child))
        return tests

    def __get_slug(self, elem):
        xml_slug = elem.findtext('slug')
        if xml_slug and xml_slug.strip():
            return xml_slug
        else:
            # TODO искать в базе слаг и изменять в случае если такой уже есть
            return slugify(unidecode(elem.findtext("title")))

    def __get_body(self, elem):
        xml_body = elem.find('body')
        body = list()
        children = xml_body.getchildren()
        if children:
            for child in children:
                body.append({
                    "type": child.get("type", "text"),
                    "content": child.text.strip()}
                )
        else:
            body.append({
                "type": "text",
                "content": xml_body.text.strip()
            })
        return body

    def __get_author(self, elem, context):
        xml_author = elem.find('author')
        if xml_author is not None and xml_author.get("id"):
            try:
                return UserModel.objects.get(id=xml_author.get("id"))
            except:
                pass
                # TODO error
        else:
            return context["request"].user

    def __get_page(self, page_id):
        if page_id:
            try:
                return Page.objects.get(id=page_id)
            except:
                pass
                # TODO error
        else:
            return None

    def save(self):
        if self.id:
            try:
                Task.objects.get(id=self.id).update(**self.data)
            except Exception as e:
                print('\nERROR: %s\n' % e)
                # TODO error
                pass
        else:
            try:
                Task.objects.create(**self.data)
            except Exception as e:
                    print('\nERROR: %s\n' % e)
                    # TODO error
                    pass

class XmlPage:

    def __init__(self, elem, context, parent_id=None):
        self.id = elem.get('id')
        self.data = dict()

        for child in elem.getchildren():
            if child.tag not in [TASKS, PAGES]:
                self.data[child.tag] = child.text.strip() if child.text else None

        self.data['parent'] = self.__get_parent(parent_id)
        self.data['author'] = self.__get_author(elem, context)
        self.data['body'] = self.__get_body(elem)
        self.data['slug'] = self.__get_slug(elem)

        self.save()
        self.save_tasks(elem, context)
        self.save_child_pages(elem, context)

    def save_child_pages(self, elem, context):
        pages = elem.find(PAGES)
        if pages is not None:
            children = pages.getchildren()
            if children is not None:
                for child in children:
                    XmlPage(child, context, parent_id=self.id)

    def save_tasks(self, elem, context):
        tasks = elem.find(TASKS)
        if tasks is not None:
            children = tasks.getchildren()
            if children is not None:
                for child in children:
                    XmlTask(child, context, parent_id=self.id)

    def __get_slug(self, elem):
        xml_slug = elem.findtext('slug')
        if xml_slug and xml_slug.strip():
            return xml_slug
        else:
            # TODO искать в базе слаг и изменять в случае если такой уже есть
            return slugify(unidecode(elem.findtext("title")))

    def __get_body(self, elem):
        xml_body = elem.find('body')
        body = list()
        children = xml_body.getchildren()
        if children:
            for child in children:
                body.append({
                    "type": child.get("type", "text"),
                    "content": child.text.strip()}
                )
        else:
            body.append({
                "type": "text",
                "content": xml_body.text.strip()
            })
        return body

    def __get_author(self, elem, context):
        xml_author = elem.find('author')
        if xml_author and xml_author.get("id"):
            try:
                return UserModel.objects.get(id=xml_author.get("id"))
            except:
                pass
                # TODO error
        else:
            return context["request"].user

    def __get_parent(self, page_id):
        if page_id:
            try:
                return Page.objects.get(id=page_id)
            except:
                pass
                # TODO error
        else:
            return None

    def save(self):
        if self.id:
            try:
                Page.objects.get(id=self.id).update(**self.data)
            except Exception as e:
                print('\nERROR: %s\n' % e)
                # TODO error
                pass
        else:
            try:
                self.id = Page.objects.create(**self.data).id
            except Exception as e:
                print('\nERROR: %s\n' % e)
                # TODO error
                pass


class ImportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Import
        fields = ['file']

    def _import(self):
        tree = etree.parse(self.validated_data["file"])
        root = tree.getroot()
        if root.tag == TASKS:
            for child in root.getchildren():
                XmlTask(child, self.context, parent_id=None)
                child.clear()

        elif root.tag == PAGES:
            for child in root.getchildren():
                XmlPage(child, self.context, parent_id=None)
                child.clear()
        else:
            pass
            # TODO Error

    def validate_author(self):
        return self.context["request"].user

    def create(self, validated_data):
        self._import()
        return super(ImportSerializer, self).create(validated_data)

