package com.youku.api.gamestatis;



import org.json.JSONException;
import org.json.JSONObject;

import com.android.intro.custorm.imageview.SampleApplication;
import com.youku.api.gamestatis.base.Persistence;
import com.youku.api.gamestatis.model.HttpCallBackHandler;
import com.youku.api.gamestatis.model.LoginModel;

import de.keyboardsurfer.android.widget.crouton.Crouton;
import de.keyboardsurfer.android.widget.crouton.Style;


import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;



public class LoginActivity  extends Activity {


	protected ProgressBar mProgressBar;
	private SampleApplication app;
	private static int loginFailTimes = 1;
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.login);
        
        app = (SampleApplication) getApplication();
        
        mProgressBar = (ProgressBar) this.findViewById(R.id.ajax_loading);
		mProgressBar.setVisibility(View.INVISIBLE);
        
		Button loginbtn = (Button)this.findViewById(R.id.loginbtn);

        loginbtn.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(final View v) {
				
				EditText usernameEdit = (EditText) LoginActivity.this.findViewById(R.id.username);
		        EditText passwordEdit = (EditText) LoginActivity.this.findViewById(R.id.password);
				
				final String username = usernameEdit.getText().toString();
		        String password  = passwordEdit.getText().toString();
		        if(username.length() == 0){
		        	Crouton.makeText(LoginActivity.this,  "Error Username null!", Style.CONFIRM).show();
		        	return;
		        }
		        
		        if(password.length()==0) {
		        	Crouton.makeText(LoginActivity.this,  "Error Password null!", Style.CONFIRM).show();
		        	return;
		        }
		        
		        v.setEnabled(false);
				mProgressBar.setVisibility(View.VISIBLE);
		        
				LoginModel loginModel = new LoginModel(LoginActivity.this);
				
				loginModel.dologin(username, password, new HttpCallBackHandler() {
					
					@Override
					public void onFailure(Throwable error, String content){
						/*if(error!=null && false){
							Toast.makeText(LoginActivity.this, error.getMessage() ,Toast.LENGTH_SHORT).show();
						}*/
						if(content!=null){
							String msg;
							if(loginFailTimes>2){
								msg= String.format("(警告如果试错多次会导致账号冻结):%s", content);
							}else{
								msg= content;
							}
							Toast.makeText(LoginActivity.this,msg ,Toast.LENGTH_SHORT).show();
						}
						//Toast.makeText(LoginActivity.this, error.getMessage() + content ,Toast.LENGTH_SHORT).show();
						Crouton.makeText(LoginActivity.this,  error.getMessage() + content, Style.ALERT).show();
						mProgressBar.setVisibility(View.INVISIBLE);
						v.setEnabled(true);
						loginFailTimes++;
					}
					
					@Override
					public void onFailure(Throwable error, JSONObject obj){
						/*if(error!=null && false){
							Toast.makeText(LoginActivity.this, error.getMessage() ,Toast.LENGTH_SHORT).show();
						}*/
						if(obj!=null){
							try {
								
								String msg="";
								if(loginFailTimes>2){
									msg="(警告如果试错多次会导致账号冻结15分钟)-";
								}
								
								if(obj.getInt("error_code")==100){
									msg += "用户密码错";
								}else{
									msg +=  obj.toString();
								}
								//Toast.makeText(LoginActivity.this, msg ,Toast.LENGTH_SHORT).show();
								Crouton.makeText(LoginActivity.this, msg, Style.ALERT).show();
								loginFailTimes++;
							} catch (JSONException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							}
						}else{
							Crouton.makeText(LoginActivity.this, error.getMessage(), Style.ALERT).show();
						}
						
						
						mProgressBar.setVisibility(View.INVISIBLE);
						v.setEnabled(true);
					}
					
					@Override
					public void onSuccess(Boolean success,Integer error_code) {
						if(!success){
							
							String msg;
							if(loginFailTimes>2){
								msg= String.format("(警告如果试错多次会导致账号冻结)login fail:%s", error_code);
							}else{
								msg= String.format("login fail:%s,%s", error_code,loginFailTimes);
							}
							Toast.makeText(LoginActivity.this,msg ,Toast.LENGTH_SHORT).show();
							
							v.setEnabled(true);
							loginFailTimes++;
							return;
							
						}
						
						loginFailTimes = 0;
						
						LoginActivity.this.setUsername(username);
						mProgressBar.setVisibility(View.INVISIBLE);
						Intent intent = new Intent(LoginActivity.this, HomeActivity.class);
						LoginActivity.this.startActivity(intent);
						overridePendingTransition(R.anim.anim_slide_in_bottom,R.anim.anim_slide_out_top);
						LoginActivity.this.finish();
					}
				});
			}
        });
    }
    
    public void setUsername(String username){
    	Persistence ps = app.getPersistence();
		ps.set("username", username);
    }
    
    
    @Override
    public void onDestroy(){
    	super.onDestroy();
    	Crouton.cancelAllCroutons();
    }
}