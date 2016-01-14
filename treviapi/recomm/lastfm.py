# -*- coding: utf-8 -*-

from pprint import pprint
import urllib
import urllib2
import inspect
import json


class LastFM:
    def __init__(self):
        print "init LastFM"
        self.API_URL = "http://ws.audioscrobbler.com/2.0/"
        self.API_KEY = "57ee3318536b23ee81d6b27e36997cde"

    def get_recomm(self, data):
        # recommend by track
        rdata = self.get_similar_tracks("track.getsimilar", {
             "track": str(data["track"].encode('utf-8')),
             "artist": str(data["artist"].encode('utf-8')),
             "limit": data["limit"]})
        rvalue = []
        if len(rdata) != 1 or len(rdata["similartracks"]["track"]) == 0:
            return rvalue
        else:
            for artist in rdata["similartracks"]["track"]:
                rvalue.append({"artist": artist["artist"]["name"], "track": artist["name"]})
            return rvalue

    def get_search(self, data):
        rdata = self.get_similar_tracks("track.search", {
             "track": str(data["track"].encode('utf-8')),
             "limit": data["limit"]})
        return rdata

    def send_request(self, args, **kwargs):
        # Request specific args
        kwargs.update(args)
        # Global args
        kwargs.update({
            "api_key": self.API_KEY,
            "format": "json"
        })
        try:
            # Create an API Request
            url = self.API_URL + "?" + urllib.urlencode(kwargs)
            # Send Request and Collect it
            data = urllib2.urlopen(url)
            # Print it
            response_data = json.load(data)
            # Close connection
            data.close()
            return response_data
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]

    def get_top_artists(self, method, dict):
        # find the key
        args = {
            "method": method,
            "limit": 3
        }
        for key in dict.keys():
            args[key] = dict[key]

        response_data = self.send_request(args)
        return reponse_data

    def get_similar_tracks(self, method, dict):
        args = {
            "method": method,
            "limit": dict["limit"]
        }
        for key in dict.keys():
            args[key] = dict[key]

        response_data = self.send_request(args)
        return response_data

    def get_similar_artists(self, method, dict):
        args = {
            "method": method,
            "limit": 3
        }
        for key in dict.keys():
            args[key] = dict[key]

        response_data = self.send_request(args)
        return reponse_data
