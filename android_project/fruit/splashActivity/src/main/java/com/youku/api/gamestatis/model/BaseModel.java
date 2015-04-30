package com.youku.api.gamestatis.model;

import java.io.IOException;
import java.security.KeyManagementException;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.UnrecoverableKeyException;
import java.security.cert.CertificateException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;

import com.github.mikephil.charting.data.Entry;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.MySSLSocketFactory;
import com.loopj.android.http.PersistentCookieStore;
import com.loopj.android.http.RequestParams;
import com.youku.api.gamestatis.util.AESHelper;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Base64;
import android.util.Log;

public class BaseModel {

	String Host = "10.100.14.78:18000";
	//String Host = "10.10.202.33:11000";
	
	String UserAgent = "GameStatis;1.0;API";
	Context context;
	SharedPreferences sp;
	String CookieKey = "CookieKey";
	
	
	protected AsyncHttpClient client = new AsyncHttpClient();
	public PersistentCookieStore myCookieStore;
	
	private String it=null;
	
	static {
	      System.loadLibrary("myjni"); // "myjni.dll" in Windows, "libmyjni.so" in Unixes
	}

	public native String helloGay(String s);
	public native String toJi(Context context);
	
	public BaseModel(Context context){
		this.context = context;
		this.sp = this.context.getSharedPreferences("Game_SP_CD", this.context.MODE_PRIVATE);
		myCookieStore = new PersistentCookieStore(context);
    	client.setCookieStore(myCookieStore);
    	client.setTimeout(15000); //15s
    	
    	try {
			this.ssl();
		} catch (KeyManagementException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (UnrecoverableKeyException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (NoSuchAlgorithmException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (KeyStoreException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (CertificateException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
    	
    	String a = toJi(context);
    	
    	MessageDigest md5;
		try {
			md5 = MessageDigest.getInstance("SHA-256");
			md5.update(a.getBytes());  
	        byte[] m = md5.digest();
	        String s = Base64.encodeToString(m, Base64.DEFAULT);
	    	//Log.d("sign",s);
	    	it = helloGay(s);
	    	Log.d("it", it);
		} catch (NoSuchAlgorithmException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    	
//		String encrypt = AESHelper.encrypt(it,"rick");
//    	Log.d("encrypt",encrypt);
//    	String decrypt = AESHelper.decrypt(it,encrypt);
//    	Log.d("decrypt",decrypt);
	}
	
	protected String encrypt(String url,HashMap<String, String> params){
		String encrypt = AESHelper.encrypt(it,"rick");
		
		List<String> list=new ArrayList<String>(params.keySet());
		
        Collections.sort(list, new Comparator<String>(){//按key值字符串比较从小到大  
           @Override  
           public int compare(String o1,String o2) {    
               return o1.compareTo(o2);  
           }});  
         
        StringBuffer re= new StringBuffer();
		for (String key : list) {
			re.append(String.format("%s=%s", key,params.get(key)));
		}
		
		return AESHelper.encrypt(it,url+re.toString());
	}
	
	
	protected void ssl() throws KeyManagementException, UnrecoverableKeyException, NoSuchAlgorithmException, KeyStoreException, CertificateException, IOException{
		KeyStore trustStore = KeyStore.getInstance(KeyStore.getDefaultType());
		//InputStream in = context.getResources().openRawResource(R.raw.mykeystore);
		//trusted.load(in, "mysecret".toCharArray());
		trustStore.load(null, null);
		MySSLSocketFactory socketFactory = new MySSLSocketFactory(trustStore);
		socketFactory.setHostnameVerifier(MySSLSocketFactory.STRICT_HOSTNAME_VERIFIER);
		//client.setSSLSocketFactory(socketFactory);
	}
	
}
