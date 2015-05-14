from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.template import defaultfilters
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Category(models.Model):

	idcategory = models.AutoField(primary_key=True)
	name = models.CharField(max_length=80)
	position = models.IntegerField(blank=True, default=0)
	hidden = models.BooleanField(
		blank=False, null=False, default=False,
		help_text=_('If checked, this category will be visible only for staff')
	)

	class Meta(object):
		ordering = ['position']
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')

	def __str__(self):
		return self.name


@python_2_unicode_compatible
class Forum(models.Model):

	idforum = models.AutoField(primary_key=True)
	category = models.ForeignKey(
		Category, related_name='forums', 
		verbose_name=_('Category')
	)
	parent = models.ForeignKey(
		'self', related_name='child_forums', verbose_name=_('Parent forum'),
		blank=True, null=True
	)
	name = models.CharField(_('Name'), max_length=80)
	position = models.IntegerField(_('Position'), blank=True, default=0)
	description = models.TextField(_('Description'), blank=True)
	moderators = models.ForeignKey(
		User, blank=True, null=True, 
		verbose_name=_('Moderators')
	)
	date = models.DateTimeField(_('Date'), blank=True, null=True)
	topics_count = models.IntegerField(_('Topics count'), blank=True, default=0)
	hidden = models.BooleanField(
		_('Hidden'), blank=False, null=False, default=False
	)

	class Meta(object):
		ordering = ['category', 'position']
		verbose_name = _('Forum')
		verbose_name_plural = _('Forums')

	def __str__(self):
		return self.name


def generate_path(instance, filename):
	folder = "forum_" + str(instance.forum_id) + "_topic_" + str(instance.idtopic)
	return os.path.join("forum", folder, filename)


@python_2_unicode_compatible
class Topic(models.Model):

	idtopic = models.AutoField(primary_key=True)
	forum = models.ForeignKey(
		Forum, related_name='topic', verbose_name=_('Forum')
	)
	user = models.ForeignKey(User, related_name='Topic', verbose_name=_('User'))
	slug = models.SlugField(max_length=100)
	title = models.CharField(_('Title'), max_length=80)
	date = models.DateTimeField(_('Date'), blank=True, db_index=True)
	description = models.TextField(_('Description'), blank=True)
	attachment = models.FileField(
		_('File'), blank=True, null=True, upload_to=generate_path
	)

	class Meta(object):
		ordering = ['date']
		verbose_name = _('Topic')
		verbose_name_plural = _('Topics')

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.idtopic:
			self.slug = defaultfilters.slugify(self.title)
		super(Topic, self).save(*args, **kwargs)

@python_2_unicode_compatible
class Comment(models.Model):

	idcomment = models.AutoField(primary_key=True)
	topic = models.ForeignKey(
		Topic, related_name='comments', verbose_name=_('Topic')
	)
	user = models.ForeignKey(
		User, related_name='comments', verbose_name=_('User')
	)
	date = models.DateTimeField(_('Date'), blank=True, db_index=True)
	description = models.TextField(_('Description'), blank=True)

	class Meta(object):
		ordering = ['date']
		verbose_name = _('Comment')
		verbose_name_plural = _('Comments')

	def __str__(self):
		return self.date
