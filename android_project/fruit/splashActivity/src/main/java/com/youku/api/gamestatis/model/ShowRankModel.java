package com.youku.api.gamestatis.model;

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

public class ShowRankModel extends BaseModel {
	
	
    String Path = "content/show/getdata";
	
	
	public ShowRankModel(Context context){
		super(context);
	}
	
    public void get(String product,int platform,int device,String channel,String date,final HttpCallBackHandler callbackhandler) {
    	
    	String url =  String.format("http://%s/%s",  Host, Path);
    	Log.d("URL", url);
    	
    	HashMap<String, String> paramMap = new HashMap<String, String>();
    			
    	paramMap.put("product", product);
    	paramMap.put("device", String.valueOf(device));
    	paramMap.put("os", String.valueOf(platform));
    	paramMap.put("channel", String.valueOf(channel));
    	if(date!=null){
    		paramMap.put("day", String.valueOf(date));
    	}
    	
    	String en = encrypt(url , paramMap);
    	RequestParams params = new RequestParams(paramMap);
    	
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
