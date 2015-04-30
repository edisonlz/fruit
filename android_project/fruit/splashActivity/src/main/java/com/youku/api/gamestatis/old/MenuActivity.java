package com.youku.api.gamestatis.old;

import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentTransaction;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.android.intro.custorm.imageview.SampleApplication;
import com.special.ResideMenu.ResideMenu;
import com.special.ResideMenu.ResideMenuItem;
import com.youku.api.gamestatis.LoginActivity;
import com.youku.api.gamestatis.R;
import com.youku.api.gamestatis.R.drawable;
import com.youku.api.gamestatis.R.id;
import com.youku.api.gamestatis.R.layout;
import com.youku.api.gamestatis.model.LoginModel;

public class MenuActivity extends FragmentActivity implements View.OnClickListener{

    private ResideMenu resideMenu;
    private MenuActivity mContext;
    private ResideMenuItem itemHome;
    private ResideMenuItem itemBaseStatis;
    private ResideMenuItem itemLogout;
    private SampleApplication app;
        
    private long clickTime = 0;
    
    private String product_id = null; 

    /**
     * Called when the activity is first created.
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.main);
        mContext = this;
        setUpMenu();
        changeFragment(new HomeFragment());
    }
    
    
    public void setProduct(String product_id){
    	this.product_id = product_id; 
    }
    
    public String getProduct(){
    	return this.product_id; 
    }

    private void setUpMenu() {

        // attach to current activity;
        resideMenu = new ResideMenu(this);
        resideMenu.setBackground(R.drawable.menu_background);
        resideMenu.attachToActivity(this);
        resideMenu.setMenuListener(menuListener);

        // create menu items;
        itemHome     = new ResideMenuItem(this, R.drawable.icon_home,     "概要统计");
        itemBaseStatis     = new ResideMenuItem(this, R.drawable.icon_profile,     "基础统计");
        //        itemCategory = new ResideMenuItem(this, R.drawable.icon_calendar, "SDK用户");
        itemLogout = new ResideMenuItem(this, R.drawable.icon_settings, "注销");

        itemHome.setOnClickListener(this);
        itemBaseStatis.setOnClickListener(this);
        itemLogout.setOnClickListener(this);
       

        resideMenu.addMenuItem(itemHome, ResideMenu.DIRECTION_LEFT);
        resideMenu.addMenuItem(itemBaseStatis, ResideMenu.DIRECTION_LEFT);
        resideMenu.addMenuItem(itemLogout, ResideMenu.DIRECTION_RIGHT);
        

        findViewById(R.id.title_bar_menu).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                resideMenu.openMenu(ResideMenu.DIRECTION_LEFT);
            }
        });
    }

    @Override
    public boolean dispatchTouchEvent(MotionEvent ev) {
        return resideMenu.onInterceptTouchEvent(ev) || super.dispatchTouchEvent(ev);
    }

    @Override
    public void onClick(View view) {

        if (view == itemHome){
            changeFragment(new HomeFragment());
        }else if (view == itemBaseStatis){
            changeFragment(new BaseStatisFragment());
        }
        else if (view == itemLogout){
        	do_logout();
        	Intent intent = new Intent(this, LoginActivity.class);
	        this.startActivity(intent);
	        LoginModel loginModel = new LoginModel(this);
	        loginModel.logout();
	        this.finish();
        }
        resideMenu.closeMenu();
    }
    
    
    private void do_logout(){
    	
    }

    private ResideMenu.OnMenuListener menuListener = new ResideMenu.OnMenuListener() {
        @Override
        public void openMenu() {
            //Toast.makeText(mContext, "Menu is opened!", Toast.LENGTH_SHORT).show();
        }

        @Override
        public void closeMenu() {
            //Toast.makeText(mContext, "Menu is closed!", Toast.LENGTH_SHORT).show();
        }
    };

     public void changeFragment(Fragment targetFragment){
        resideMenu.clearIgnoredViewList();
        getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.main_fragment, targetFragment, "fragment")
                .setTransitionStyle(FragmentTransaction.TRANSIT_FRAGMENT_FADE)
                .commit();
    }

    // What good method is to access resideMenu
    public ResideMenu getResideMenu(){
        return resideMenu;
    }
    
    
    @Override  
    public boolean onKeyDown(int keyCode, KeyEvent event) {  
        if (keyCode == KeyEvent.KEYCODE_BACK) {  
            exit();  
            return true;  
        }  
        return super.onKeyDown(keyCode, event);  
    }  
      
    private void exit() {  
        if ((System.currentTimeMillis() - clickTime) > 2000) {  
            Toast.makeText(getApplicationContext(), "再按一次后退键退出",   Toast.LENGTH_SHORT).show();  
            clickTime = System.currentTimeMillis();  
        } else {  
            this.finish();  
        }  
    }
}