package com.youku.api.gamestatis.base;


import java.util.ArrayList;
import java.util.HashMap;

import android.os.Bundle;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.app.ListFragment;
import android.util.Log;
import android.view.KeyEvent;

import com.android.intro.custorm.imageview.SampleApplication;
import com.jeremyfeinstein.slidingmenu.lib.SlidingMenu;
import com.jeremyfeinstein.slidingmenu.lib.app.SlidingFragmentActivity;
import com.youku.api.gamestatis.R;
import com.youku.api.gamestatis.R.dimen;
import com.youku.api.gamestatis.R.drawable;
import com.youku.api.gamestatis.R.id;
import com.youku.api.gamestatis.R.layout;

import de.keyboardsurfer.android.widget.crouton.Crouton;

public class BaseActivity extends SlidingFragmentActivity {


	protected ListFragment mFrag;
	private String product_id = null;
	private SampleApplication app;
	
	public HashMap<String,Integer> deivceMap =new HashMap<String,Integer>();
	public HashMap<String,Integer> platformMap =new HashMap<String,Integer>();
	
	public String[] deivceList;
	public String[] platformList;
	public SlidingMenu sm;
	
	
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		
		app = (SampleApplication) getApplication();
		
		// set the Behind View
		setBehindContentView(R.layout.menu_frame);
		
		if (savedInstanceState == null) {
			FragmentTransaction t = this.getSupportFragmentManager().beginTransaction();
			mFrag = new MenuFragment();
			t.replace(R.id.menu_frame, mFrag);
			t.commit();
		} else {
			mFrag = (ListFragment)this.getSupportFragmentManager().findFragmentById(R.id.menu_frame);
		}

		sm = getSlidingMenu();
		sm.setShadowWidthRes(R.dimen.shadow_width);
		sm.setShadowDrawable(R.drawable.shadow);
		sm.setBehindOffsetRes(R.dimen.slidingmenu_offset);
		sm.setFadeDegree(0.35f);
		sm.setTouchModeAbove(SlidingMenu.TOUCHMODE_FULLSCREEN);
		
		this.deivceMap.put("全部", -1);
		this.deivceMap.put("phone", 1);
		this.deivceMap.put("pad", 2);
		
		deivceList = new String[]{"全部","phone","pad"};
		
		
		
		this.platformMap.put("全部",-1);
		this.platformMap.put("android",61);
		this.platformMap.put("ios",52);
		this.platformMap.put("wp",59);
		platformList = new String[]{"全部","android","ios","wp"};

	}
	
	public void setProduct(String product_id){
		Persistence ps = app.getPersistence();
		ps.set("product", product_id);
    }
    
    public String getProduct(){
    	Persistence ps = app.getPersistence();
    	return ps.get("product");
    }
    
    public void deleteProduct(){
    	Persistence ps = app.getPersistence();
    	ps.delete("product");
    }
    
    
    @Override
    public void onBackPressed() {
        super.onBackPressed();
        //overridePendingTransition(R.anim.move_left_in_activity, R.anim.move_right_out_activity);
    }
    
    @Override  
    public boolean onKeyDown(int keyCode, KeyEvent event) {  
        if (keyCode == KeyEvent.KEYCODE_BACK) {  
        	this.finish();
        	overridePendingTransition(R.anim.move_left_in_activity, R.anim.move_right_out_activity);
            return false;  
        }
        return super.onKeyDown(keyCode, event);  
    }
    
    @Override
	public void onDestroy(){
	    	super.onDestroy();
	    	Crouton.cancelAllCroutons();
	}
}
