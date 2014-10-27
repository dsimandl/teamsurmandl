# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'location_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('map_center_longitude', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('map_center_latitude', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('pin_longitude', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('pin_latitude', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='location', to=orm['profiles.SurmandlUser'])),
            ('current_location', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'location', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'location_location')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'location.location': {
            'Meta': {'object_name': 'Location'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'location'", 'to': u"orm['profiles.SurmandlUser']"}),
            'current_location': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'map_center_latitude': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'map_center_longitude': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pin_latitude': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pin_longitude': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'profiles.surmandluser': {
            'Meta': {'object_name': 'SurmandlUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['location']