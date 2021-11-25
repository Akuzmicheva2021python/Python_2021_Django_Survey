from django.core.mail import send_mail
from django.forms import ModelForm, ModelChoiceField, CharField, PasswordInput, Form, \
    EmailField, EmailInput
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import (
    password_validation,
)
from .models import Projects, HandbookObjects, SprDolgn, \
                    VObjects, TypeStreet, ObjectsPersonals, \
                    Addresses, VObjectsAddress, \
                    OneObjectsPersonals, CRMPersonals
# from django.contrib.auth.models import User
from adjsite.settings.basesettings import EMAIL_HOST_USER


class HandbookObjectsForm(ModelForm):
    class Meta:
        model = HandbookObjects
        fields = '__all__'
        labels = {
            'ObjectName': _('Наименование'),
        }


class SprDolgnForm(ModelForm):
    class Meta:
        model = SprDolgn
        fields = '__all__'

        labels = {
            'DolgnName': _('Наименование'),
            'InsertDate': _('Дата создания'),
        }


class ProjectsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ProjectName'].widget.attrs.update({'class': 'form-control'})
        self.fields['ProjectDesc'].widget.attrs.update(rows=3)
        self.fields['ArhivDate'].widget.attrs.update({'format': '%Y-%m-%d %H:%M'})
        self.fields['ArhivDate'].help_text = "Укажите дату в формате гггг-мм-дд чч:мм ."

    def clean_pocketname(self):
        val = self.cleaned_data['PocketName']
        if len(val) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return val

    class Meta:
        model = Projects
        fields = '__all__'
        labels = {
            'ProjectName': _('Название проекта  '),
            'ProjectDesc': _('Описание '),
            'isActive': _('Активный '),
            'LastUpdate': _('Дата изменения '),
            'RemoteVisit': _('Удаленные визиты'),
            'VizitTime': _('Время визитов '),
            'NoGeo': _('Гео-локация'),
            'ArhivDate': _('Дата блокировки '),
            'PocketName': _('Имя пакета '),
            'VersionNumber': _('Номер версии '),
            'PocketSize': _('Размер пакета'),
            'WEB': 'WEB',
        }
        # help_texts = {
        #     'ProjectName': _('Имя проекта может содержать только буквы.'),
        # }
        error_messages = {
            'ProjectName': {'max_length': _("Длина поля превышает 150 знаков."), },
            'PocketName': {'max_length': _("Длина поля превышает 50 знаков."), },
        }


class VObjectsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'] = ModelChoiceField(
                    queryset=HandbookObjects.objects.values_list('ObjectName', flat=True,),
                    empty_label="...",
                    to_field_name='ObjectName',
                    label=_('Категория '),)
        self.fields['AddressID'] = ModelChoiceField(
            queryset=Addresses.objects.values_list('AddressID', flat=True),
            to_field_name='AddressID',
        )

    class Meta:
        model = VObjects
        fields = '__all__'
        labels = {
            'title': _('Наименование объекта'),
            'full_title': _('Полное наименовае объекта'),
            'categories': _('Категория'),
            'StatusID': _('Статус'),
            'AddressID': _('Адрес'),
            'personals': _('Персонал'),
            'InsertDate': _('Дата изменения'),
        }


class VObjectsAddressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'] = ModelChoiceField(
                    queryset=HandbookObjects.objects.values_list('ObjectName', flat=True,),
                    empty_label="...",
                    to_field_name='ObjectName',
                    label=_('Категория '),)

    class Meta:
        model = VObjectsAddress
        fields = '__all__'
        labels = {
            'title': _('Наименование объекта'),
            'full_title': _('Полное наименовае объекта'),
            'categories': _('Категория'),
            'StatusID': _('Статус'),
            'AddressID': _('Адрес'),
            'InsertDate': _('Дата изменения'),
        }


class TypeStreetForm(ModelForm):
    class Meta:
        model = TypeStreet
        fields = '__all__'
        labels = {
            'ObjectName': _('Наименование'),
        }


class ObjectsPersonalsForm(ModelForm):
    class Meta:
        model = ObjectsPersonals
        fields = '__all__'
        labels = {
            'PersFam': _('Фамилия'),
            'PersName': _('Имя'),
            'PersLName': _('Отчество'),
            'PersPhone': _('Телефон'),
            'PersEmail': _('Адрес Е-почты'),
            'Comments': _('Комментарий'),
            'StatusID': _('Статус'),
            'InsertDate': _('Дата изменения'),
        }


class OneObjectsPersonalsForm(ModelForm):
    class Meta:
        model = OneObjectsPersonals
        fields = '__all__'
        labels = {
            'PersFam': _('Фамилия'),
            'PersName': _('Имя'),
            'PersLName': _('Отчество'),
            'PersPhone': _('Телефон'),
            'PersEmail': _('Адрес Е-почты'),
            'Comments': _('Комментарий'),
            'StatusID': _('Статус'),
            'InsertDate': _('Дата изменения'),
        }


class AddressesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['typestreet'] = \
            ModelChoiceField(queryset=TypeStreet.objects.values_list('TypeStreet', flat=True),
                             empty_label="...",
                             to_field_name='TypeStreet',
                             label=_('Тип улицы '),
                             )

    class Meta:
        model = Addresses
        fields = '__all__'
        labels = {
            'Region': _('Регион'),
            'SubRegion': _('Под-Регион'),
            'city': _('Город (Населенный пункт)'),
            'Raion': _('Район'),
            'street': _('Улица'),
            'typestreet': _('Тип улицы'),
            'house': _('Дом'),
            'latitude': _('Широта'),
            'longitude': _('Долгота'),
            'Gis2Address': _('Адрес - строка'),
            'InsertDate': _('Дата изменения'),
        }


class CRMPersonalsForm(ModelForm):
    class Meta:
        model = CRMPersonals
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'is_active',
                  'last_login', 'date_joined',
                  ]
        labels = {
            'username': _('Логин'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'email': _('Адрес Е-почты'),
            'is_active': _('Активен'),
            'last_login': _('Дата входа в систему'),
            'date_joined': _('Дата регистрации'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_login'].widget.attrs['readonly'] = True
        self.fields['date_joined'].widget.attrs['readonly'] = True


class CRMPersonalsCreationForm(ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _('Пароли не совпадают.'),
    }
    password1 = CharField(
        label=_("Пароль"),
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = CharField(
        label=_("Повтор пароля"),
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = CRMPersonals
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user1 = super().save(commit=False)
        user1.set_password(self.cleaned_data["password1"])
        if commit:
            user1.save()
        return user1


class CRMPersonalsPassChangeForm(Form):
    """
    Форма изменения пароля для пользователя менеджером или админом
    """

    error_messages = {
        'password_mismatch': _('Пароли не совпадают.'),
    }
    # required_css_class = 'required'
    password1 = CharField(
        label=_("Password"),
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'autofocus': True}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = CharField(
        label=_("Password (again)"),
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Введите пароль повторно для проверки."),
    )
    email1 = EmailField(
        label=_("Адрес email (для отправки)"),
        required=False,
        widget=EmailInput(attrs={'autocomplete': 'email'}),
        help_text=_("Укажите адрес, если требуется отправка по e-mail. "
                    "Для отказа от отправки сделайте значение пустым. "),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(password2, self.user)
        return password2

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        password = self.cleaned_data["password1"]
        email_end = self.cleaned_data["email1"]
        if email_end:
            subject = 'Предупреждение об изменении данных пользователя'
            message = f'Вам был изменен пароль входа в систему : {password}'
            from_email = EMAIL_HOST_USER
            recipient_list = [email_end]
            try:
                v_email = send_mail(subject, message, from_email, recipient_list,)
            except:
                return 0
        else:
            v_email = 0
        return v_email

    def save(self, commit=True):
        """Save the new password."""
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

    @property
    def changed_data(self):
        data = super().changed_data
        for name in self.fields:
            if name not in data:
                return []
        return ['password']
