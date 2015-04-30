package com.youku.api.gamestatis.model;


import java.util.ArrayList;
import java.util.HashMap;

import org.apache.http.Header;
import org.apache.http.message.BasicHeader;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.content.Context;
import android.util.Log;

import com.loopj.android.http.JsonHttpResponseHandler;
import com.loopj.android.http.RequestParams;
import com.youku.api.gamestatis.util.JsontoHash;


public class SummaryStatsModel extends BaseModel {
	
	
    String Path = "basic/getdata";
	
	
	public SummaryStatsModel(Context context){
		super(context);
	}
	
    public void get(final HttpCallBackHandler callbackhandler) {
    	
    	String url =  String.format("http://%s/%s",  Host, Path);
    	Log.d("URL", url);
    	RequestParams params = new RequestParams();
    	
    	HashMap<String, String> paramMap = new HashMap<String, String>();
    	String en = encrypt(url , paramMap);
    	
    	Header[] headers = {
    		     new BasicHeader("Content-type", "application/json")
    		    ,new BasicHeader("Accept", "application/json")
    		    ,new BasicHeader("User-Agent", UserAgent)
    		    ,new BasicHeader("AP-Key", en)
    	};
    	
        client.get(this.context , url , headers , params , new JsonHttpResponseHandler() {
        	
        	@Override
			public void onFailure(Throwable error, String content)
			{
        		if(error!=null && content!=null) {
        			Log.e("Error HTTP" , "onFailure error : " + error.toString() + "content : " + content);
        		}
				callbackhandler.onFailure(error,content);
			}
        	
        	@Override
			public void onFailure(Throwable error, JSONObject obj)
			{
        		if(error!=null && obj!=null) {
					Log.e("Error HTTP" , "onFailure error : " + error.toString() + "content : " + obj.toString());
        		}
				callbackhandler.onFailure(error, obj);
			}
        	
			
            @Override
            public void onSuccess(JSONObject document) {
               JSONArray dataJsonArray = null;
               
               HashMap<String, Object> datas = null;
                try {
				    datas = (HashMap<String, Object>) JsontoHash.jsonToMap(document);
				} catch (JSONException e1) {
					// 	TODO Auto-generated catch block
					e1.printStackTrace();
				}
               
               Log.d("Data Index",datas.toString());
        	   callbackhandler.onSuccess(datas);
        	   
            }
        });
        
    }
    
}
