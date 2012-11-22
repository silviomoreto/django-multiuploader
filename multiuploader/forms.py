from django import forms
from django.conf import settings
from utils import formatFileExtensions
from django.utils.html import mark_safe
from django.template.loader import render_to_string
from django.core.validators import validate_integer
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

class MultiuploadWidget(forms.MultipleHiddenInput):
    def __init__(self, attrs={}):
        super(MultiuploadWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        widget_ = super(MultiuploadWidget, self).render(name, value, attrs)
        output = '<div id="hidden_container" style="display:none;">%s</div>'%widget_
        return mark_safe(output)

class MultiuploaderField(forms.MultiValueField):
    widget = MultiuploadWidget()
    def formfield(self, **kwargs):
        kwargs['widget'] = MultiuploadWidget
        return super(MultiuploaderField, self).formfield(**kwargs)
        
    def validate(self,values):
        super(MultiuploaderField,self).validate(values)
    
    def clean(self, values):
        super(MultiuploaderField,self).clean(values)

        """Check if value consists only of valid integers."""
        
        ret = []
        if values:
            for id in values:
                validate_integer(id)
                ret.append(id)
        
        return ret
        
    def compress(self,value):
        if value!=None:
            return [i for i in value]


class MultiUploadFormWidget(forms.FileInput):
    template = 'multiuploader/widget.html'
    def __init__(self, attrs={}):
        if not "multiple" in attrs:
            attrs["multiple"] = True
            
        super(MultiUploadFormWidget, self).__init__(attrs)
        
       
    def render(self, name, value, attrs=None):
        max_usize = getattr(settings,"MAX_UPLOAD_SIZE")
        filetypes = formatFileExtensions(getattr(settings,"ALLOWED_FILE_TYPES"))
        
        maxFileNumber = getattr(settings,"MAX_FILE_NUMBER") 
        
        widget_ = super(MultiUploadFormWidget, self).render(name, value, attrs)
        output = render_to_string(self.template, {
                                                  'field': widget_,
                                                  'field_name':name,
                                                  'maxFileSize':max_usize,
                                                  'fileTypes': filetypes,
                                                  'maxFileNumber':maxFileNumber
                                                 })
        
        return mark_safe(output)
        
class MultiUploadForm(forms.Form):
    file = forms.FileField(widget=MultiUploadFormWidget)
    
    def clean_file(self):
        
        content = self.cleaned_data[u'file']
        content_type = content.content_type.split('/')[0]
                
        ctypes = getattr(settings, "CONTENT_TYPES")
        max_usize = getattr(settings,"MAX_UPLOAD_SIZE")
        
        if content_type in ctypes:
            if content._size > max_usize:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(max_usize), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))
        
        return content
    
