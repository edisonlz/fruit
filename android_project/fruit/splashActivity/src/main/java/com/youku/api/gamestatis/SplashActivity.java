package com.youku.api.gamestatis;

import java.util.List;

import com.youku.api.gamestatis.model.LoginModel;
import com.youku.api.gamestatis.util.NetWorkUtil;
import com.youku.api.gamestatis.util.ShortCut;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.PixelFormat;
import android.graphics.drawable.BitmapDrawable;
import android.os.Bundle;
import android.os.Handler;
import android.view.Window;
import android.view.WindowManager;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;

public class SplashActivity  extends Activity {

    //�ӳ�3�� 
    private static final long SPLASH_DELAY_MILLIS = 3000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.welcome);
        
        Animation aniAlpha = AnimationUtils.loadAnimation( getApplicationContext(), R.drawable.alpha);
        ImageView showtime = (ImageView)this.findViewById(R.id.backimg);
        showtime.startAnimation(aniAlpha); 
        

//        if(!ShortCut.hasShortcut(this, R.string.app_name)){
//        	ShortCut.createShortcut(this, R.string.app_name, R.id.icon);
//        }
        
        if(!NetWorkUtil.CheckNetworkState(this)){
			return;
		}
        
        new Handler().postDelayed(new Runnable() {
            public void run() {
                goHome();
            }
        }, SPLASH_DELAY_MILLIS);
    }

    private void goHome() {
    	LoginModel login = new LoginModel(this);
    	
    	if(login.is_login()) {
	        //Intent intent = new Intent(SplashActivity.this, MenuActivity.class);
    		Intent intent = new Intent(SplashActivity.this, HomeActivity.class);
	        SplashActivity.this.startActivity(intent);
	        SplashActivity.this.finish();
	        overridePendingTransition(R.anim.anim_slide_in_top,R.anim.anim_slide_out_bottom);
    	}else {
    		Intent intent = new Intent(SplashActivity.this, LoginActivity.class);
	        SplashActivity.this.startActivity(intent);
	        SplashActivity.this.finish();
	        overridePendingTransition(R.anim.anim_slide_in_top,R.anim.anim_slide_out_bottom);
    	}
    	
    }
}
