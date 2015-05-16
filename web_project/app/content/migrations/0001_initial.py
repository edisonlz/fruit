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
            ('state', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_delete', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'\u6807\u9898', max_length=100)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('iner_count', self.gf('django.db.models.fields.IntegerField')(default=12)),
            ('box_type', self.gf('django.db.models.fields.IntegerField')(default=1, db_index=True)),
        ))
        db.send_create_signal('content', ['Box'])

        # Adding model 'ItemCategory'
        db.create_table(u'content_itemcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_delete', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'\u6807\u9898', max_length=100)),
        ))
        db.send_create_signal('content', ['ItemCategory'])

        # Adding model 'ItemPromote'
        db.create_table(u'content_itempromote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_delete', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'\u6807\u9898', max_length=100)),
            ('promote_rate', self.gf('django.db.models.fields.FloatField')()),
            ('promote_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('content', ['ItemPromote'])

        # Adding model 'Item'
        db.create_table(u'content_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'\u6807\u9898', max_length=100)),
            ('categroy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.ItemCategory'])),
            ('promote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.ItemPromote'], null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('stock_price', self.gf('django.db.models.fields.FloatField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_delete', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('content', ['Item'])

        # Adding model 'BoxItem'
        db.create_table(u'content_boxitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('box', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Box'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Item'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('is_delete', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('content', ['BoxItem'])

        # Adding model 'City'
        db.create_table(u'content_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_delete', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('city_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('manager', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('content', ['City'])

        # Adding model 'ShoppingAddress'
        db.create_table(u'content_shoppingaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_delete', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.City'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('manager', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('onlinetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('content', ['ShoppingAddress'])


    def backwards(self, orm):
        # Deleting model 'Box'
        db.delete_table(u'content_box')

        # Deleting model 'ItemCategory'
        db.delete_table(u'content_itemcategory')

        # Deleting model 'ItemPromote'
        db.delete_table(u'content_itempromote')

        # Deleting model 'Item'
        db.delete_table(u'content_item')

        # Deleting model 'BoxItem'
        db.delete_table(u'content_boxitem')

        # Deleting model 'City'
        db.delete_table(u'content_city')

        # Deleting model 'ShoppingAddress'
        db.delete_table(u'content_shoppingaddress')


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
        'content.boxitem': {
            'Meta': {'object_name': 'BoxItem'},
            'box': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Box']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_delete': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Item']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
        },
        'content.city': {
            'Meta': {'object_name': 'City'},
            'city_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'manager': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'content.item': {
            'Meta': {'object_name': 'Item'},
            'categroy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.ItemCategory']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'promote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.ItemPromote']", 'null': 'True', 'blank': 'True'}),
            'stock_price': ('django.db.models.fields.FloatField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'\\u6807\\u9898'", 'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'content.itemcategory': {
            'Meta': {'object_name': 'ItemCategory'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2', 'db_index': 'True'}),
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
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'\\u6807\\u9898'", 'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'content.shoppingaddress': {
            'Meta': {'object_name': 'ShoppingAddress'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.City']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'manager': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'onlinetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['content']