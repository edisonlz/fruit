package com.youku.api.gamestatis.base;

import android.content.Context;
import android.content.SharedPreferences;
import android.text.TextUtils;
import android.util.Log;

import org.apache.http.client.CookieStore;
import org.apache.http.cookie.Cookie;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.ConcurrentHashMap;


public class Persistence {


	    private final ConcurrentHashMap<String, String> cookies;
	    private final SharedPreferences cookiePrefs;
	    private static final String SAVE_PREFS = "CookiePrefsFile";
	    private static final String NAME_STORE = "save_names";
	    private static final String NAME_PREFIX = "this_is_game_";
	    private static final int limit_count=100;

	    /**
	     * Construct a persistent cookie store.
	     *
	     * @param context Context to attach cookie store to
	     */
	    public Persistence(Context context) {
	        cookiePrefs = context.getSharedPreferences(SAVE_PREFS, 0);
	        cookies = new ConcurrentHashMap<String, String>();

	        // Load any previously stored cookies into the store
	        String storedNames = cookiePrefs.getString(NAME_STORE, null);
	        if (storedNames != null) {
	            String[] cookieNames = TextUtils.split(storedNames, ",");
	            for (String name : cookieNames) {
	                String data = cookiePrefs.getString(NAME_PREFIX + name, null);
	                    if (data != null) {
	                        cookies.put(name, data);
	                    }
	            }
	        }
	    }

	    public void set(String key,String value) {
	        
	        String name = key;
	        
	        cookies.put(key, value);
	        int now_count = cookies.keySet().size();
	        // Save cookie into persistent store
	        SharedPreferences.Editor prefsWriter = cookiePrefs.edit();
	        prefsWriter.putString(NAME_STORE, TextUtils.join(",", cookies.keySet()));
	        prefsWriter.putString(NAME_PREFIX + name, value);
	        prefsWriter.putInt("NowCount", now_count);
	        prefsWriter.commit();
	        
	        if(now_count>limit_count){
	        	clear();
	        }
	        
	    }
	    
	    public String get(String key){
	    	 return cookies.get(key);
	    }
	    
	    
	    public void clear() {
	        // Clear cookies from persistent store
	        SharedPreferences.Editor prefsWriter = cookiePrefs.edit();
	        for (String name : cookies.keySet()) {
	            prefsWriter.remove(NAME_PREFIX + name);
	        }
	        prefsWriter.remove(NAME_STORE);
	        prefsWriter.commit();

	        // Clear cookies from local store
	        cookies.clear();
	    }

	   
	    /**
	     * Non-standard helper method, to delete cookie
	     *
	     * @param cookie cookie to be removed
	     */
	    public void delete(String key) {
	        cookies.remove(key);
	        SharedPreferences.Editor prefsWriter = cookiePrefs.edit();
	        prefsWriter.remove(NAME_PREFIX + key);
	        prefsWriter.commit();
	    }

}
