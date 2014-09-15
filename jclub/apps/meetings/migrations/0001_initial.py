# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'meetings_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'meetings', ['Category'])

        # Adding model 'TimeSlot'
        db.create_table(u'meetings_timeslot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'meetings', ['TimeSlot'])

        # Adding model 'Meeting'
        db.create_table(u'meetings_meeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('presenter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timeslot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meetings.TimeSlot'], unique=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('publication_reference', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('publication_url', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'meetings', ['Meeting'])

        # Adding M2M table for field publication_category on 'Meeting'
        m2m_table_name = db.shorten_name(u'meetings_meeting_publication_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meeting', models.ForeignKey(orm[u'meetings.meeting'], null=False)),
            ('category', models.ForeignKey(orm[u'meetings.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['meeting_id', 'category_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'meetings_category')

        # Deleting model 'TimeSlot'
        db.delete_table(u'meetings_timeslot')

        # Deleting model 'Meeting'
        db.delete_table(u'meetings_meeting')

        # Removing M2M table for field publication_category on 'Meeting'
        db.delete_table(db.shorten_name(u'meetings_meeting_publication_category'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'meetings.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'meetings.meeting': {
            'Meta': {'object_name': 'Meeting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'presenter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'publication_category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['meetings.Category']", 'symmetrical': 'False'}),
            'publication_reference': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'publication_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'timeslot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meetings.TimeSlot']", 'unique': 'True'})
        },
        u'meetings.timeslot': {
            'Meta': {'object_name': 'TimeSlot'},
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['meetings']