package com.youku.api.gamestatis.model;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import android.content.Context;
import android.util.Log;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.BaseJsonHttpResponseHandler;
import com.loopj.android.http.JsonHttpResponseHandler;
import com.loopj.android.http.PersistentCookieStore;
import com.loopj.android.http.RequestParams;

import org.apache.http.Header;
import org.apache.http.cookie.Cookie;
import org.apache.http.entity.StringEntity;
import org.apache.http.message.BasicHeader;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;


public class LoginModel extends BaseModel {
	
	
    String Path = "user/login";
    
    public static final int ErrorCodeLoginFail = 100;
    public static final int ErrorCodeCookieExpire = 101;
    public static final int ErrorCodeNotLogin = 102;
	
	public LoginModel(Context context){
		super(context);
	}
	
	public boolean is_login(){
		List cookies = this.myCookieStore.getCookies();
		for(int i=0;i<cookies.size();i++){
			Cookie cookie = (Cookie)cookies.get(i);
			Log.d("Cookie Name",cookie.getName());
			if(cookie.getName().indexOf("user_id")>=0){
				Log.d("Cookie login",cookie.getValue());
				return true;
			}
		}
		return false;
	}
	
	public void logout(){
		this.myCookieStore.clear();
	}
	 
    public void dologin(String username, String password ,final HttpCallBackHandler callbackhandler) {
    	
    	String loginUrl =  String.format("http://%s/%s",  Host, Path);
    	Log.d("URL", loginUrl);
    	
    	
    	HashMap<String, String> paramMap = new HashMap<String, String>();
    	paramMap.put("key", "value");
    	paramMap.put("username", username);
    	paramMap.put("password", password);
    	
    	String en = encrypt(loginUrl , paramMap);
    	
    	RequestParams params = new RequestParams(paramMap);
    	
    	Header[] headers = {
    		     new BasicHeader("Content-type", "application/json")
    		    ,new BasicHeader("Accept", "application/json")
    		    ,new BasicHeader("User-Agent", UserAgent)
    		    ,new BasicHeader("AP-Key", en)
    	};
    	
    	
    	Log.d("Param login",params.toString());
    	
        client.post( loginUrl,  params ,  new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(JSONObject document) {
               try {
            	   
            	   Boolean success  = document.getBoolean("status");
            	   int error_code = 0;
            	   if(!success){
            		   error_code  = document.getInt("error_code");
            		   Throwable e = new Throwable();
            		   callbackhandler.onFailure(e, document);
            	   }
            	   else{
            		   callbackhandler.onSuccess(success,error_code);
            	   }
               } catch (JSONException e) {
            	   e.printStackTrace();
               }
            }
            
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
        });
    }
    
}