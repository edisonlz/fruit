/*******************************************************************************
 * Copyright (c) 2013 Chris Banes.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/

package com.android.intro.custorm.imageview;

import android.app.Activity;
import android.app.Application;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Environment;
import android.util.Log;

import java.io.File;

import com.youku.api.gamestatis.base.Persistence;
import com.youku.api.gamestatis.util.ShortCut;

import uk.co.senab.bitmapcache.BitmapLruCache;

public class SampleApplication extends Application {

    private BitmapLruCache mCache;
    private Integer diskCacheMaxSize = 20 * 1024 * 1024; //20M;
    private boolean has_external_store = false;
    
    private Persistence persist;
    
    @Override
    public void onCreate() {
        super.onCreate();

        File cacheLocation;

        if (Environment.MEDIA_MOUNTED.equals(Environment.getExternalStorageState())) {
            cacheLocation = new File(
                    Environment.getExternalStorageDirectory() + "/StatisPF_Android-BitmapCache");
            has_external_store = true;
        } else {
            cacheLocation = new File(getFilesDir() + "/StatisPF_Android-BitmapCache");
        }
        cacheLocation.mkdirs();

        BitmapLruCache.Builder builder = new BitmapLruCache.Builder(this);
        builder.setMemoryCacheEnabled(true).setMemoryCacheMaxSizeUsingHeapSize();
        builder.setDiskCacheEnabled(true).setDiskCacheLocation(cacheLocation);
        if(has_external_store){
        	diskCacheMaxSize = 100 * 1024 * 1024;//100M
        }
        builder.setDiskCacheMaxSize(diskCacheMaxSize);

        mCache = builder.build();
        
        persist = new Persistence(this);
        
        doHttpCache();
    }
    
    public void doHttpCache(){
    	final long httpCacheSize = 10 * 1024 * 1024; // 10 MiB
        final File httpCacheDir = new File(getCacheDir(), "http");
        try {
            Class.forName("android.net.http.HttpResponseCache")
                .getMethod("install", File.class, long.class)
                .invoke(null, httpCacheDir, httpCacheSize);
            Log.d("init","http cache ok");
        } catch (Exception httpResponseCacheNotAvailable) {
        	Log.d("init","android.net.http.HttpResponseCache not available, probably because we're running on a pre-ICS version of Android. Using com.integralblue.httpresponsecache.HttpHttpResponseCache.");
            try{
                com.integralblue.httpresponsecache.HttpResponseCache.install(httpCacheDir, httpCacheSize);
            }catch(Exception e){
               Log.e("init","Failed to set up com.integralblue.httpresponsecache.HttpResponseCache");
            }
        }
    }

    public BitmapLruCache getBitmapCache() {
        return mCache;
    }
    
    public Persistence getPersistence() {
        return persist;
    }

    public static SampleApplication getApplication(Context context) {
        return (SampleApplication) context.getApplicationContext();
    }

}
