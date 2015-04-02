from dash.orgs.views import OrgObjPermsMixin, OrgPermsMixin
from dash.utils import get_obj_cacheable
from django import forms
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from smartmin.views import SmartCRUDL, SmartReadView, SmartListView, SmartCreateView
from tracpro.contacts.models import Contact
from tracpro.unsolicited.models import Unsolicited, Reply

__author__ = 'awesome'


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        exclude = ('reply_by', 'status')
        widgets = {'reply_to': forms.HiddenInput()}


class UnsolicitedCRUDL(SmartCRUDL):
    model = Unsolicited
    actions = ('read', 'list', 'by_contact')

    class Read(OrgObjPermsMixin, SmartReadView):
        def derive_fields(self):
            return ['contact__name', 'contact__urn', 'status', 'text', 'created_on', 'delivered_on']

        def get_queryset(self):
            queryset = super(UnsolicitedCRUDL.Read, self).get_queryset()
            return queryset.filter(org=self.request.org, is_active=True,
                                   region__in=self.request.user.get_regions(self.request.org))

    class List(OrgPermsMixin, SmartListView):
        default_order = ('contact__name',)
        search_fields = ('contact__name__icontains', 'contact__urn__icontains', 'text__icontains')
        template_name = 'unsolicited/unsolicited_list.haml'

        def derive_fields(self):
            return ['contact.name', 'contact.urn', 'text', 'created_on', 'delivered_on', 'reply']

        def lookup_field_value(self, context, obj, field):
            if field.lower().endswith('urn'):
                return obj.contact.urn.split(":")[1]
            if field == 'reply':
                replies = ""
                if obj.replies.exists():
                    replies = '<p>%d replies to this query or feedback already exist</p>' % obj.replies.count()
                return '%s<form id="reply-%d" action="%s" method="post" class="reply-form">%s<p><button type="submit"' \
                       ' class="button button-info">Send</button></p></form>' % (
                        replies, obj.pk, "/reply/send/", ReplyForm(initial={'reply_to': obj.pk}).as_p())
            return super(UnsolicitedCRUDL.List, self).lookup_field_value(context, obj, field)

        def derive_queryset(self, **kwargs):
            queryset = super(UnsolicitedCRUDL.List, self).derive_queryset(**kwargs)
            queryset = queryset.filter(org=self.request.org)
            if self.request.region:
                queryset = queryset.filter(contact__region=self.request.region)
            return queryset

        def lookup_field_link(self, context, field, obj):
            if field == 'reply':
                return "#"
            return super(UnsolicitedCRUDL.List, self).lookup_field_link(context, field, obj)

    class ByContact(OrgPermsMixin, SmartListView):
        fields = ('text', 'created_on', 'reply')
        link_fields = []

        @classmethod
        def derive_url_pattern(cls, path, action):
            return r'^%s/%s/(?P<contact>\d+)/$' % (path, action)

        def derive_contact(self):
            def fetch():
                return Contact.objects.get(pk=self.kwargs['contact'], org=self.request.org)

            return get_obj_cacheable(self, '_contact', fetch)

        def derive_queryset(self, **kwargs):
            return self.derive_contact().unsolicited_messages.all()

        def get_context_data(self, **kwargs):
            context = super(UnsolicitedCRUDL.ByContact, self).get_context_data(**kwargs)
            context['contact'] = self.derive_contact()
            return context

        def lookup_field_link(self, context, field, obj):
            return super(UnsolicitedCRUDL.ByContact, self).lookup_field_link(context, field, obj)

        def lookup_field_value(self, context, obj, field):
            if field == 'reply':
                replies = ""
                if obj.replies.exists():
                    replies = '<p>%d replies to this query or feedback already exist</p>' % obj.replies.count()
                return '%s<form id="reply-%d" action="%s" method="post" class="reply-form">%s<p><button type="submit"' \
                       ' class="button button-info">Send</button></p></form>' % (
                        replies, obj.pk, "/reply/send/", ReplyForm(initial={'reply_to': obj.pk}).as_p())
            return super(UnsolicitedCRUDL.ByContact, self).lookup_field_value(context, obj, field)


class ReplyCRUDL(SmartCRUDL):
    model = Reply
    actions = ('send',)

    class Send(OrgPermsMixin, SmartCreateView):
        def post(self, request, *args, **kwargs):
            _form = ReplyForm(request.POST)
            if _form.is_valid():
                reply = _form.save(commit=False)
                reply.reply_by = request.user
                reply.save()
                return JsonResponse(reply.to_json())
            print "Invalid Form"
            return JsonResponse(_form.errors)

        @csrf_exempt
        def dispatch(self, request, *args, **kwargs):
            return super(ReplyCRUDL.Send, self).dispatch(request, *args, **kwargs)