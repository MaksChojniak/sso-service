from urllib.parse import urlsplit

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


class RedirectURIListField(forms.Field):
    default_error_messages = {
        'invalid_list': 'Provide redirect_uris as a list of URL strings.',
        'invalid_uri': 'Each redirect URI must be a valid HTTPS URL.',
        'fragment': 'Redirect URIs must not contain a fragment.',
    }

    def to_python(self, value):
        if value in self.empty_values:
            return []
        if not isinstance(value, list):
            raise ValidationError(self.error_messages['invalid_list'], code='invalid_list')
        return value

    def validate(self, value):
        super().validate(value)
        local_hosts = {'localhost', '127.0.0.1', '::1'}
        for uri in value:
            if not isinstance(uri, str):
                raise ValidationError(self.error_messages['invalid_list'], code='invalid_list')
            parsed_uri = urlsplit(uri)
            if parsed_uri.fragment:
                raise ValidationError(self.error_messages['fragment'], code='fragment')
            if parsed_uri.scheme == 'http' and parsed_uri.hostname in local_hosts:
                if not parsed_uri.netloc:
                    raise ValidationError(self.error_messages['invalid_uri'], code='invalid_uri')
                continue
            try:
                URLValidator(schemes=['https'])(uri)
            except ValidationError as exc:
                raise ValidationError(self.error_messages['invalid_uri'], code='invalid_uri') from exc


class ServiceURLField(forms.URLField):
    default_validators = [URLValidator(schemes=['http', 'https'])]


class ClientApplicationCreateForm(forms.Form):
    name = forms.CharField(max_length=100)
    service_url = ServiceURLField(max_length=500)
    redirect_uris = RedirectURIListField()

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not name:
            raise forms.ValidationError('Name cannot be blank.')
        return name


class ClientApplicationUpdateForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    service_url = ServiceURLField(max_length=500, required=False)
    redirect_uris = RedirectURIListField(required=False)
    is_active = forms.BooleanField(required=False)

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if 'name' in self.data and not name:
            raise forms.ValidationError('Name cannot be blank.')
        return name

    def clean(self):
        cleaned_data = super().clean()
        supplied_fields = set(self.data) & set(self.fields)
        if not supplied_fields:
            raise forms.ValidationError('Provide at least one field to update.')
        if 'redirect_uris' in supplied_fields and not cleaned_data.get('redirect_uris'):
            self.add_error('redirect_uris', 'Provide at least one redirect URI.')
        return cleaned_data