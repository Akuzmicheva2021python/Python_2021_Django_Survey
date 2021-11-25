# from .models import *
from django.db import connection

menu_nav2 = [
    {'title': 'СРМ пользователи', 'url_name': 'crmpersonals_list', 'groupid': 1},
    {'title': 'СРМ менеджеры', 'url_name': 'crmpersonals_list', 'groupid': 2},
]


def my_custom_sql(self, groupid):
    with connection.cursor() as cursor:
        rez = \
            cursor.execute("INSERT INTO auth_user_groups (user_id, group_id) VALUES (%s,%s)",
                           [self.id, groupid])
    return rez


def my_groupid_users_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM auth_group WHERE name=%s", ['CRM_users'])
        row = cursor.fetchone()
        rez = row[0]
    return rez


def my_groupid_staffs_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM auth_group WHERE name=%s", ['CRM_staffs'])
        row = cursor.fetchone()
        rez = row[0]

    return rez


class DataMixin:
    def get_groupid_context(self,gr):
        if gr == 1:
            groupid1 = my_groupid_users_sql()
        elif gr == 2:
            groupid1 = my_groupid_staffs_sql()
        else:
            groupid1 = 0
        return groupid1
