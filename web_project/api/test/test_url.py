#coding=utf-8
import unittest
import os, sys
import urllib2
import json
from urls import datas
import logging
import json_delta

class TestUrl(object):
    """
    测试 url
    """

    def read(self, url):
        logging.error("[read url] %s" % url)
        return json.loads(urllib2.urlopen(url).read())

    def diff(self, key, value, old_data):

        if not key or not value or not old_data:
            return

        if type(value) == list:

            left_data = value[0]
            right_data = old_data.get(key, [])

            if not right_data:
                print "key diff:%s" % key
                return

            if type(right_data) != list:
                return

            right_data = right_data[0]

            if type(right_data) not in (dict,list):
                return
            overlap_results, left_only, right_only = json_delta.compute_keysets(left_data, right_data)

            print "*" * 20
            print "[overlap] %s:", overlap_results
            print "[left_only] %s:", left_only
            print "[right_only] %s:", right_only
            print
            print

            if type(left_data) == dict:
                for _key, _value in left_data.iteritems():
                    if type(_value) == dict:
                        self.diff(_key, _value, right_data.get(_key))
                    elif type(_value) == list:
                        self.diff(_key, _value, right_data)
                        

        elif type(value) == dict:

            left_data  = value
            right_data = old_data
            overlap_results, left_only, right_only = json_delta.compute_keysets(left_data, right_data)

            print "*" * 20
            print "[overlap] %s:", overlap_results
            print "[new_only] %s:", left_only
            print "[old_only] %s:", right_only
            print
            print
            
            for _key, _value in value.iteritems():
                if type(_value) == dict:
                    self.diff(_key, _value, right_data.get(_key))
                elif type(_value) == list:
                    self.diff(_key, _value, right_data)



    def run(self):
        print "[start]..."

        for d in datas:
            new_data = self.read(d.get("new"))
            old_data = self.read(d.get("old"))

            #for test
            #old_data["results"][0]["contents"]["results"][0]["a"] = 1
            #old_data["results"][0]["contents"]["results"][0]["b"] = 1

            overlap_results, left_only, right_only = json_delta.compute_keysets(new_data, old_data)

            print "*" * 20
            print "[overlap] %s:", overlap_results
            print "[new_only] %s:", left_only
            print "[old_only] %s:", right_only
            print
            print



            if type(new_data) == dict:
                for key, value in new_data.iteritems():
                    if type(value) == list:
                        self.diff(key, value, old_data)
                    elif type(value) == dict:
                        for _key, _value in value.iteritems():
                            self.diff(_key, _value, old_data.get(key))

                            
        print "[end]..."

if __name__ == "__main__":


    tu = TestUrl()
    tu.run()



