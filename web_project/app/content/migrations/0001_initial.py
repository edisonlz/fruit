# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Box'
        db.create_table(u'content_box', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'\u6807\u9898', max_length=100)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2, db_index=True)),
            ('iner_count', self.gf('django.db.models.fields.IntegerField')(default=12)),
            ('box_type', self.gf('django.db.models.fields.IntegerField')(default=1, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_delete', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('content', ['Box'])

        # Adding model 'ItemCategory'
        db.create_table(u'content_itemcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'\u6807\u9898', max_length=100)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_delete', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('content', ['ItemCategory'])

        # Adding model 'ItemPromote'
        db.create_table(u'content_itempromote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'\u6807\u9898', max_length=100)),
            ('promote_rate', self.gf('django.db.models.fields.FloatField')()),
            ('promote_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_delete', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('content', ['ItemPromote'])


    def backwards(self, orm):
        # Deleting model 'Box'
        db.delete_table(u'content_box')

        # Deleting model 'ItemCategory'
        db.delete_table(u'content_itemcategory')

        # Deleting model 'ItemPromote'
        db.delete_table(u'content_itempromote')


    models = {
        'content.box': {
            'Meta': {'object_name': 'Box'},
            'box_type': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iner_count': ('django.db.models.fields.IntegerField', [], {'default': '12'}),
            'is_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'\\u6807\\u9898'", 'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'content.itemcategory': {
            'Meta': {'object_name': 'ItemCategory'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'\\u6807\\u9898'", 'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'content.itempromote': {
            'Meta': {'object_name': 'ItemPromote'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'promote_rate': ('django.db.models.fields.FloatField', [], {}),
            'promote_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'\\u6807\\u9898'", 'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['content']