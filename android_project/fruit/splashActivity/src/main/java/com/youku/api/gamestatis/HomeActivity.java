package com.youku.api.gamestatis;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Timer;

import org.json.JSONException;
import org.json.JSONObject;


import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

import android.view.KeyEvent;
import android.view.LayoutInflater;

import android.view.View;
import android.view.Window;
import android.widget.AdapterView;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.Toast;
import android.widget.AdapterView.OnItemClickListener;


import com.android.intro.custorm.imageview.SampleApplication;
import com.youku.api.gamestatis.adapter.HomeIndexAdapter;
import com.youku.api.gamestatis.base.BaseActivity;
import com.youku.api.gamestatis.model.HttpCallBackHandler;
import com.youku.api.gamestatis.model.LoginModel;
import com.youku.api.gamestatis.model.SummaryStatsModel;

import de.keyboardsurfer.android.widget.crouton.Crouton;
import de.keyboardsurfer.android.widget.crouton.Style;
import com.yalantis.phoenix.PullToRefreshView;

public class HomeActivity  extends BaseActivity {

	
	  
	    private long clickTime = 0;

        private ProgressBar mProgressBar;
		private Context mContext;
		private Timer timer = new Timer();
		private ListView dataListView;

        private PullToRefreshView  mPullToRefreshView;

	    /**
	     * Called when the activity is first created.
	     */
	    @Override
	    public void onCreate(Bundle savedInstanceState) {
	        super.onCreate(savedInstanceState);
	        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
	        
	        
	        
	        mContext = this;
	        setContentView(R.layout.home);
	        
	        setUpViews();
	        
		}
	    
	    @Override
	    public void onPostCreate(Bundle savedInstanceState) {
			super.onPostCreate(savedInstanceState);
			request();
	    }
	    
	    @Override
	    public void onResume(){
	    	super.onResume();
	    	
	    	//dataListView.invalidate();
	    }
	    
	    
	    private void request(){
	    	SummaryStatsModel commonStats = new SummaryStatsModel(this);
			commonStats.get(new HttpCallBackHandler() {
				
				@Override
				public void onSuccess(HashMap<String, Object> result) {
					onHttpResponseCallback(result);
					mProgressBar.setVisibility(View.INVISIBLE);
				}
				
				@Override
				public void onFailure(Throwable error, String content){
					mProgressBar.setVisibility(View.INVISIBLE);
					if(error!=null) {
						Crouton.makeText(HomeActivity.this,   error.getMessage(), Style.CONFIRM).show();
	        		}
					if(content!=null){
						Crouton.makeText(HomeActivity.this,   content.toString(), Style.CONFIRM).show();
					}
				}
				
				@Override
				public void onFailure(Throwable error, JSONObject obj){
					mProgressBar.setVisibility(View.INVISIBLE);				
					if(error!=null) {
						String msg = error.getMessage();
						if(msg==null){
							msg = "读取接口错误";
						}
						Crouton.makeText(HomeActivity.this,  msg, Style.CONFIRM).show();
	        		}
					if(obj!=null){
						Crouton.makeText(HomeActivity.this,   obj.toString(), Style.CONFIRM).show();
					}
				}
			});
	    }

		private void setUpViews() {


			mProgressBar = (ProgressBar) this.findViewById(R.id.ajax_loading);
			mProgressBar.setVisibility(View.VISIBLE);

            mPullToRefreshView = (PullToRefreshView) findViewById(R.id.pull_to_refresh);
            mPullToRefreshView.setOnRefreshListener(new PullToRefreshView.OnRefreshListener() {
                @Override
                public void onRefresh() {
                    mPullToRefreshView.postDelayed(new Runnable() {
                        @Override
                        public void run() {
                            mPullToRefreshView.setRefreshing(false);
                            request();
                        }
                    }, 1000 * 1);
                }
            });

			 
			dataListView = (ListView) this.findViewById(R.id.dataListView);
			dataListView.addHeaderView(LayoutInflater.from(this).inflate(R.layout.home_table_header, null), null, false);
			
		
		}

		public void onHttpResponseCallback(HashMap<String, Object> result) {

			/* message home*/
			
			String msg = String.valueOf( result.get("msg"));
			if((msg !=null && msg.length()==0) || msg ==null ){
				msg = "欢迎回来,向右滑动展示菜单";
			}
			Crouton.makeText(HomeActivity.this, msg, Style.CONFIRM).show();
			
			
			/*Set List View*/
			
			HomeIndexAdapter adapter = new HomeIndexAdapter(this , (ArrayList<HashMap<String,Object>>)result.get("data"));
			dataListView.setAdapter(adapter);
			
			EditText dateText = (EditText)this.findViewById(R.id.dateText);
			dateText.setText(String.valueOf(result.get("date")));
			
			
			
			dataListView.setOnItemClickListener(new OnItemClickListener(){
				@Override
				public void onItemClick(AdapterView<?> parent, View view,
						int position, long id) {
					HashMap<String,Object> data = (HashMap<String, Object>) parent.getItemAtPosition(position);
					String item_id = String.valueOf(data.get("id"));
					HomeActivity act = (HomeActivity)parent.getContext();
					act.setProduct(item_id);
					
					Intent intent = new Intent(HomeActivity.this, BaseStatisActivity.class);
					HomeActivity.this.startActivity(intent);
					overridePendingTransition(R.anim.anim_slide_in_bottom,R.anim.anim_slide_out_top);
					
				}
			});
		}
	   
	    
	    @Override  
	    public boolean onKeyDown(int keyCode, KeyEvent event) {  
	        if (keyCode == KeyEvent.KEYCODE_BACK) {  
	            exit();  
	        }  
	        return true;
	        //return super.onKeyDown(keyCode, event);  
	    }  
	      
	    private void exit() {  
	        if ((System.currentTimeMillis() - clickTime) > 3000) {  
	            Toast.makeText(getApplicationContext(), "再按一次后退键退出",   Toast.LENGTH_SHORT).show();  
	            clickTime = System.currentTimeMillis();  
	        } else {  
	            this.finish();
	        }
	    }
	    
	    @Override
	    public void onDestroy(){
	    	super.onDestroy();
	    	Crouton.cancelAllCroutons();
	    }
}
